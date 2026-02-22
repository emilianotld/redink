#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

import logging
from typing import Dict, List
from redink.modules.headers.fingerprint import fingerprint_banner_service, fingerprint_service

logger = logging.getLogger(__name__)

DEFAULT_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 6379, 8080]

def scan_services(host: str, ports: List[int] = DEFAULT_PORTS, timeout: float = 5.0) -> List[Dict]:
    """
    Scan a host for open ports and fingerprint services.

    Args:
        host (str): The target host to scan.
        ports (List[int]): A list of ports to scan.
        timeout (float): Timeout for each connection attempt.

    Returns:
        List[Dict]: A list of dictionaries containing service details for each open port.
    """
    results = []

    for port in ports:
        try:
            logger.info(f"Scanning {host}:{port}...")
            # Attempt to fingerprint the service using banner grabbing
            banner_details = fingerprint_banner_service(host, port, timeout)
            if banner_details:
                logger.info(f"Banner found on {host}:{port}: {banner_details.get('banner')}")

            # Attempt to fingerprint the service using HTTP headers (if applicable)
            if port in [80, 443, 8080]:  # Common HTTP/HTTPS ports
                service_details = fingerprint_service(host, port, timeout)
                banner_details.update(service_details)

            # Add the details to the results if any fingerprinting succeeded
            if banner_details:
                results.append({"port": port, "details": banner_details})
        except Exception as e:
            logger.warning(f"Failed to scan {host}:{port}: {e}")

    return results

if __name__ == "__main__":
    # Example usage
    target_host = "example.com"
    scanned_services = scan_services(target_host)
    for service in scanned_services:
        print(f"Port {service['port']}: {service['details']}")