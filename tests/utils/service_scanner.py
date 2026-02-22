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
import pytest
from unittest.mock import patch
from redink.modules.headers.fingerprint import fingerprint_banner_service, fingerprint_service
from service_scanner import scan_services

@pytest.fixture
def mock_fingerprint_banner_service():
    with patch("redink.modules.headers.fingerprint.fingerprint_banner_service") as mock:
        yield mock

@pytest.fixture
def mock_fingerprint_service():
    with patch("redink.modules.headers.fingerprint.fingerprint_service") as mock:
        yield mock

def test_scan_services_with_mocked_fingerprints(mock_fingerprint_banner_service, mock_fingerprint_service):
    # Configure the mock services to return predefined results
    mock_fingerprint_banner_service.return_value = {"banner": "Mock Banner"}
    mock_fingerprint_service.return_value = {"headers": {"Server": "Mock Server"}}

    # Example host and ports for testing
    host = "example.com"
    ports = [80, 443]
    results = scan_services(host, ports)

    # Validate the results
    assert len(results) == 2
    assert results[0]["port"] == 80
    assert results[0]["details"]["banner"] == "Mock Banner"
    assert results[1]["details"]["headers"]["Server"] == "Mock Server"


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
    import argparse

    parser = argparse.ArgumentParser(description="Service Scanner for Fingerprinting")
    parser.add_argument("host", help="Target host to scan")
    parser.add_argument(
        "--ports", nargs="+", type=int, default=DEFAULT_PORTS,
        help="List of ports to scan (default: common ports)"
    )
    parser.add_argument(
        "--timeout", type=float, default=5.0,
        help="Timeout for each connection attempt (default: 5.0 seconds)"
    )
    args = parser.parse_args()

    scanned_services = scan_services(args.host, args.ports, args.timeout)
    for service in scanned_services:
        print(f"Port {service['port']}: {service['details']}")