#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
import pytest
from unittest.mock import patch, MagicMock
from redink.modules.headers.fingerprint import fingerprint_http_service, fingerprint_services

def test_fingerprint_http_service_success():
    """
    Test fingerprint_http_service with a successful HTTP response.
    """
    host = "example.com"
    port = 80
    timeout = 2.0

    # Mock the response of requests.Session().get
    mock_response = MagicMock()
    mock_response.headers = {
        "Server": "Apache",
        "Content-Security-Policy": "default-src 'self'",
        "X-Frame-Options": "DENY",
        "Strict-Transport-Security": "max-age=31536000"
    }
    mock_response.status_code = 200

    with patch("requests.Session.get", return_value=mock_response):
        result = fingerprint_http_service(host, port, timeout)
        assert result["server"] == "Apache"
        assert result["status_code"] == 200
        assert "Content-Security-Policy" in result["security_headers"]
        assert "X-Frame-Options" in result["security_headers"]
        assert "Strict-Transport-Security" in result["security_headers"]

def test_fingerprint_http_service_failure():
    """
    Test fingerprint_http_service when an HTTP request fails.
    """
    host = "example.com"
    port = 80
    timeout = 2.0

    with patch("requests.Session.get", side_effect=Exception("HTTP request failed")):
        with pytest.raises(Exception, match="HTTP fingerprinting failed for http://example.com:80"):
            fingerprint_http_service(host, port, timeout)

def test_fingerprint_services():
    """
    Test fingerprint_services with multiple open ports.
    """
    host = "example.com"
    open_ports = [{"port": 80}, {"port": 443}]

    # Mock the fingerprint_http_service function
    with patch("redink.modules.headers.fingerprint.fingerprint_http_service") as mock_http_service:
        mock_http_service.side_effect = [
            {"server": "Apache", "status_code": 200, "security_headers": {}},
            {"server": "Nginx", "status_code": 200, "security_headers": {}}
        ]

        result = fingerprint_services(host, open_ports)
        assert len(result) == 2
        assert result[0]["details"]["server"] == "Apache"
        assert result[1]["details"]["server"] == "Nginx"


def test_fingerprint_services_no_ports():
    """
    Test fingerprint_services with no open ports.
    """
    target = "example.com"
    open_ports = []
    
    result = fingerprint_services(target, open_ports)
    assert len(result) == 2
    assert result[0]["details"]["server"] == "Apache"
    assert result[1]["details"]["server"] == "Nginx"

def test_fingerprint_services_invalid_target():
    """
    Test fingerprint_services with an invalid target.
    """
    target = ""
    open_ports = [{'port': 80, 'status': 'open'}, {'port': 443, 'status': 'open'}]
    
    with pytest.raises(ValueError):
        result =  fingerprint_services(target, open_ports)
        assert len(result) == 2
        assert result[0]["details"]["server"] == "Apache"
        assert result[1]["details"]["server"] == "Nginx"

def test_fingerprint_services_error_handling():
    """
    Test fingerprint_services handles errors during fingerprinting.
    """
    target = "example.com"
    open_ports = [{'port': 80, 'status': 'open'}, {'port': 443, 'status': 'open'}]
    
    with patch("redink.modules.headers.fingerprint.fingerprint_service", side_effect=Exception("Fingerprinting error")):
        with pytest.raises(Exception, match="Fingerprinting error"):
            fingerprint_services(target, open_ports)