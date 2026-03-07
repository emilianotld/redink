#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

import yaml
from pathlib import Path

def _load_yaml_file(file_path: str) -> dict:
    """
    Loads a YAML file and returns its contents as a dictionary.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        dict: The contents of the YAML file.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If the file is not a valid YAML file.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {file_path}")

    with open(path, "r") as f:
        return yaml.safe_load(f)

def load_default_config() -> dict:
    """
    Loads the default configuration from 'defaults.yaml'.

    Returns:
        dict: The default configuration.
    """
    raw = _load_yaml_file(Path(__file__).parent / "defaults.yaml")

    services = raw.get("services", {})
    raw["services"] = {int(port): service for port, service in services.items()}

    raw["default_ports"] = [int(p) for p in raw.get("default_ports", [])]
    return raw

def load_port_config() -> dict:
    """
    Loads the port configuration from 'ports.yaml'.

    Returns:
        dict: The port configuration.
    """
    raw = _load_yaml_file(Path(__file__).parent / "ports.yaml")
    raw["common_risky_ports"] = [int(p) for p in raw.get("common_risky_ports", [])]
    return raw

def load_header_config() -> dict:
    """
    Loads the header configuration from 'defaults.yaml'.

    Returns:
        dict: The header configuration.
    """
    raw = _load_yaml_file(Path(__file__).parent / "defaults.yaml")
    raw["REQUIRED_SECURITY_HEADERS"] = raw.get("REQUIRED_SECURITY_HEADERS", [])
    return raw

def load_risk_config() -> dict:
    """
    Loads the risk configuration from 'risk-ranges.yaml'.

    Returns:
        dict: The risk configuration.
    """
    raw = _load_yaml_file(Path(__file__).parent / "risk-ranges.yaml")
    raw["loss_usd"] = raw.get("loss_usd", [])
    return raw

def load_scoring_config() -> dict:
    """
    Loads the scoring configuration from 'defaults.yaml'.

    Returns:
        dict: The scoring configuration.
    """
    return _load_yaml_file(Path(__file__).parent / "defaults.yaml")

def read_DEFAULT_PORTS() -> list:
    """
    Reads the default ports from the default configuration.

    Returns:
        list: A list of default ports.
    """
    return load_default_config().get("default_ports", [])

def read_COMMON_RISKY_PORTS() -> list:
    """
    Reads the common risky ports from the port configuration.

    Returns:
        list: A list of common risky ports.
    """
    return load_port_config().get("common_risky_ports", [])

def read_SENSITIVE_PORTS() -> dict:
    """
    Reads the sensitive ports from the port configuration.

    Returns:
        dict: A dictionary of sensitive ports.
    """
    return load_port_config().get("sensitive_ports", {})