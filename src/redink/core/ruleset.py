#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

from redink.config.loader import load_header_config, read_COMMON_RISKY_PORTS

COMMON_RISKY_PORTS = read_COMMON_RISKY_PORTS()
HEADERS = load_header_config()
REQUIRED_SECURITY_HEADERS = set(HEADERS["REQUIRED_SECURITY_HEADERS"])

def score_port(port: int) -> float:
    """
    Scores a port based on whether it is considered risky.

    Args:
        port (int): The port number to evaluate.

    Returns:
        float: The score for the port (0.5 if risky, 0 otherwise).
    """
    if not isinstance(port, int) or port < 0 or port > 65535:
        raise ValueError(f"Invalid port number: {port}")
    return 0.5 if port in COMMON_RISKY_PORTS else 0.0

def score_security_headers(headers: dict) -> float:
    """
    Scores the presence of required security headers.

    Args:
        headers (dict): A dictionary of headers.

    Returns:
        float: The score based on missing security headers.
    """
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary.")
    missing = REQUIRED_SECURITY_HEADERS - headers.keys()
    return len(missing) * 0.5

def score_server_disclosure(server: str) -> float:
    """
    Scores the server header based on disclosure of version information.

    Args:
        server (str): The server header value.

    Returns:
        float: The score (1 if version information is disclosed, 0 otherwise).
    """
    if not isinstance(server, str):
        raise ValueError("Server must be a string.")
    return 1.0 if "/" in server else 0.0

def classify_risk(score: float) -> str:
    """
    Classifies the risk level based on the score.

    Args:
        score (float): The risk score.

    Returns:
        str: The risk level ("LOW", "MEDIUM", "HIGH", "CRITICAL").
    """
    if not isinstance(score, (int, float)) or score < 0:
        raise ValueError(f"Invalid score: {score}")
    
    if score <= 2:
        return "LOW"
    if score <= 5:
        return "MEDIUM"
    if score <= 8:
        return "HIGH"
    return "CRITICAL"