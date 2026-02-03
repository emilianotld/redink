#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
import yaml
from pathlib import Path

def load_default_config():
    path = Path(__file__).parent / "defaults.yaml"
    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    services = raw.get("services", {})
    raw["services"] = {
        int(port): service
        for port, service in services.items()
    }

    raw["default_ports"] = [
        int(p) for p in raw.get("default_ports", [])
    ]

    return raw

def load_port_config():
    path = Path(__file__).parent / "ports.yaml"
    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    raw["common_risky_ports"] = [
        int(p) for p in raw.get("common_risky_ports", [])
    ]
    return raw

def load_header_config():
    path = Path(__file__).parent / "defaults.yaml"
    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    raw["REQUIRED_SECURITY_HEADERS"] = [
        p for p in raw.get("REQUIRED_SECURITY_HEADERS", [])
    ]
    return raw

def load_risk_config():
    path = Path(__file__).parent / "risk-ranges.yaml"
    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    raw["loss_usd"] = [
        p for p in raw.get("loss_usd", [])
    ]
    return raw

def load_scoring_config():
    path = Path(__file__).parent / "defaults.yaml"
    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    return raw

def load_sensitive_ports_config():
    path = Path(__file__).parent / "ports.yaml"
    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    return raw

def read_DEFAULT_PORTS():
    CONFIG = load_default_config()
    DEFAULT_PORTS = CONFIG["default_ports"]
    return DEFAULT_PORTS

def read_COMMON_RISKY_PORTS():
    CONFIG = load_port_config()
    COMMON_RISKY_PORTS = CONFIG["common_risky_ports"]
    return COMMON_RISKY_PORTS

def read_SENSITIVE_PORTS():
    CONFIG = load_sensitive_ports_config()
    SENSITIVE_PORTS = CONFIG.get("sensitive_ports", {})
    return SENSITIVE_PORTS