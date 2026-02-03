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
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
from redink.config.loader import load_default_config

def fingerprint_service(host: str, port: int, timeout: float = 2.0) -> Dict:
    """
     Identify the likely service running on a port.
    """
    ports_config = load_default_config()
    PORT_SERVICE_MAP = ports_config["services"]
    service = PORT_SERVICE_MAP.get(port, "UNKNOWN")
    details = {}

    if service in ("HTTP", "HTTP-ALT", "HTTPS"):
        try:
            scheme = "https" if port == 443 else "http"
            url = f"{scheme}://{host}:{port}"

            response = requests.get(url, timeout=timeout, verify=False)

            details["server"] = response.headers.get("Server", "unknown")
            details["status_code"] = response.status_code
            details["security_headers"] = {
                h: response.headers.get(h)
                for h in ("Content-Security-Policy", "X-Frame-Options", "Strict-Transport-Security")
                if h in response.headers
            }

        except requests.RequestException:
            details["http_access"] = "failed"

    else:
        # basic banner
        try:
            with socket.create_connection((host, port), timeout=timeout) as sock:
                sock.settimeout(timeout)
                banner = sock.recv(1024).decode(errors="ignore").strip()
                if banner:
                    details["banner"] = banner
        except (socket.timeout, OSError):
            pass

    return {
        "port": port,
        "service": service.lower(),
        "details": details
    }

def fingerprint_services(
    host: str,
    open_ports: List[Dict]
) -> List[Dict]:
    """
    Fingerprinting of every open ports detected.
    """
    results = []
    logger = logging.getLogger("redink")
    logger.info("Executing fingerprint...")
    logger.debug(f"hostname={host}, open ports={len(open_ports)}")
    for entry in open_ports:
        port = entry["port"]
        result = fingerprint_service(host, port)
        results.append(result)

    return results
