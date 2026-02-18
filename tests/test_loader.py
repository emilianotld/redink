#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
import pytest
import yaml
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

def test_load_yaml_file_valid(tmp_path):
    """
    Test _load_yaml_file with a valid YAML file.
    """
    yaml_file = tmp_path / "test.yaml"
    yaml_file.write_text("key: value")
    data = _load_yaml_file(str(yaml_file))
    assert isinstance(data, dict), "YAML file should be loaded as a dictionary"
    assert data["key"] == "value", "YAML file should contain the correct key-value pair"

def test_load_yaml_file_invalid():
    """
    Test _load_yaml_file with an invalid or non-existent YAML file.
    """
    with pytest.raises(FileNotFoundError):
        _load_yaml_file("non_existent.yaml")

def test_load_yaml_file_malformed(tmp_path):
    """
    Test _load_yaml_file with a malformed YAML file.
    """
    
    config_dir = tmp_path / "config"
    config_dir.mkdir()

    yaml_file = config_dir / "malformed.yaml"
    yaml_file.write_text("key: value\nkey2: :value2")  

    with pytest.raises(yaml.YAMLError, match="while parsing a block mapping"):
        _load_yaml_file(str(yaml_file))