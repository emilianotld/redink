#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

import logging
import socket
from typing import List, Dict
import urllib3
import requests
from redink.config.loader import load_default_config
from redink.core.exceptions import InvalidConfigurationError, RedInkError
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger("redink")

# Constants
DEFAULT_TIMEOUT = 2.0

def validate_host_and_port(host: str, port: int) -> bool:
    """Validate the host and port."""
    try:
        socket.gethostbyname(host)
        if not (1 <= port <= 65535):
            raise ValueError("Port must be in range 1-65535")
        return True
    except InvalidConfigurationError as e:
        logger.error(f"Invalid host or port: {e}")
        return False

def fingerprint_http_service(host: str, port: int, timeout: float) -> Dict:
    """Fingerprint HTTP/HTTPS services."""
    details = {}
    scheme = "https" if port == 443 else "http"
    url = f"{scheme}://{host}:{port}"

    try:
        with requests.Session() as session:
            response = session.get(url, timeout=timeout, verify=False)
            details["server"] = response.headers.get("Server", "unknown")
            details["status_code"] = response.status_code
            details["security_headers"] = {
                h: response.headers.get(h)
                for h in ("Content-Security-Policy", "X-Frame-Options", "Strict-Transport-Security")
                if h in response.headers
            }
    except requests.RequestException as e:
        logger.warning(f"HTTP request failed for {url}: {e}")
        raise RedInkError(f"HTTP fingerprinting failed for {url}") from e

    return details

def fingerprint_banner_service(host: str, port: int, timeout: float) -> Dict:
    """Fingerprint services using banner grabbing."""
    details = {}
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            banner = sock.recv(1024).decode(errors="ignore").strip()
            if banner:
                details["banner"] = banner
    except (socket.timeout, OSError) as e:
        logger.warning(f"Banner grabbing failed for {host}:{port}: {e}")
    return details

def fingerprint_service(host: str, port: int, timeout: float = DEFAULT_TIMEOUT) -> Dict:
    """
    Identify the likely service running on a port.

    :param host: The target host.
    :param port: The target port.
    :param timeout: Timeout for the operation.
    :raises InvalidConfigurationError: If the host or port is invalid.
    :raises RedInkError: If fingerprinting fails.
    :return: A dictionary with the fingerprint details.
    """
    if not validate_host_and_port(host, port):
        return {"port": port, "service": "invalid", "details": {}}

    ports_config = load_default_config()
    PORT_SERVICE_MAP = ports_config["services"]
    service = PORT_SERVICE_MAP.get(port, "UNKNOWN").lower()
    details = {}

    if service in ("http", "http-alt", "https"):
        details = fingerprint_http_service(host, port, timeout)
    else:
        details = fingerprint_banner_service(host, port, timeout)

    return {
        "port": port,
        "service": service,
        "details": details
    }


def fingerprint_services(host: str, open_ports: List[Dict]) -> List[Dict]:
    """
    Fingerprinting of every open port detected.
    """
    results = []
    logger.info("Executing fingerprint...")
    logger.debug(f"hostname={host}, open ports={len(open_ports)}")
    for entry in open_ports:
        port = entry["port"]
        result = fingerprint_service(host, port)
        results.append(result)

    return results

    