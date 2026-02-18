#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
import pytest
from redink.config.loader import load_default_config, load_port_config, _load_yaml_file

def test_load_default_config():
    """
    Test load_default_config to ensure it loads the default configuration correctly.
    """
    config = load_default_config()
    assert isinstance(config, dict), "Default config should be a dictionary"
    assert "services" in config, "Default config should contain 'services'"
    assert "default_ports" in config, "Default config should contain 'default_ports'"
    assert isinstance(config["default_ports"], list), "'default_ports' should be a list"

def test_load_port_config():
    """
    Test load_port_config to ensure it loads the port configuration correctly.
    """
    config = load_port_config()
    assert isinstance(config, dict), "Port config should be a dictionary"
    assert "common_risky_ports" in config, "Port config should contain 'common_risky_ports'"
    assert isinstance(config["common_risky_ports"], list), "'common_risky_ports' should be a list"

