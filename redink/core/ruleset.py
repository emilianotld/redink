#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

from redink.config.loader import load_header_config
from redink.config.loader import read_COMMON_RISKY_PORTS

def score_port(port: int) -> int:
    COMMON_RISKY_PORTS = read_COMMON_RISKY_PORTS()
    return 0.5 if port in COMMON_RISKY_PORTS else 0

def score_security_headers(headers: dict) -> int:
    HEADERS = load_header_config()
    REQUIRED_SECURITY_HEADERS = HEADERS["REQUIRED_SECURITY_HEADERS"]
    missing = REQUIRED_SECURITY_HEADERS - headers.keys()
    return len(missing) * 0.5

def score_server_disclosure(server: str) -> int:
    return 1 if "/" in server else 0

def classify_risk(score: int) -> str:
    if score <= 2:
        return "LOW"
    if score <= 5:
        return "MEDIUM"
    if score <= 8:
        return "HIGH"
    return "CRITICAL"
