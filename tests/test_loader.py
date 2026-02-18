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

def test_load_default_config(tmp_path):
    """
    Test load_default_config to ensure it loads the default configuration correctly.
    """
    defaults_file = tmp_path / "defaults.yaml"
    defaults_file.write_text("""
    default_ports:
      - 21
      - 22
      - 23
      - 25
      - 53
      - 80
      - 110
      - 143
      - 443
      - 445
      - 3306
      - 3389
      - 5432
      - 6379
      - 8080

    services:
      21: FTP
      22: SSH
      23: TELNET
      25: SMTP
      53: DNS
      80: HTTP
      110: POP3
      143: IMAP
      443: HTTPS
      445: SMB
      3306: MySQL
      3389: RDP
      5432: PostgreSQL
      6379: Redis
      8080: HTTP-ALT
      27017: MongoDB
    """)

    load_default_config.__globals__["Path"] = lambda _: defaults_file

    config = load_default_config()
    assert isinstance(config, dict), "Default config should be a dictionary"
    assert "default_ports" in config, "Default config should contain 'default_ports'"
    assert "services" in config, "Default config should contain 'services'"
    assert config["default_ports"] == [
        21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 6379, 8080
    ], "Default ports should match the expected list"
    assert config["services"]["21"] == "FTP", "Service for port 21 should be FTP"
    assert config["services"]["443"] == "HTTPS", "Service for port 443 should be HTTPS"

def test_load_port_config(tmp_path):
    """
    Test load_port_config to ensure it loads the port configuration correctly.
    """

    ports_file = tmp_path / "ports.yaml"
    ports_file.write_text("""
    common_risky_ports:
      - 21
      - 23
      - 3306
      - 6379

    SENSITIVE_PORTS:
      21: FTP
      23: Telnet
      3306: MySQL
      5432: PostgreSQL
      6379: Redis
      27017: MongoDB
      9200: Elasticsearch
      11211: Memcached
    """)

    load_port_config.__globals__["Path"] = lambda _: ports_file

    config = load_port_config()
    assert isinstance(config, dict), "Port config should be a dictionary"
    assert "common_risky_ports" in config, "Port config should contain 'common_risky_ports'"
    assert "SENSITIVE_PORTS" in config, "Port config should contain 'SENSITIVE_PORTS'"
    assert config["common_risky_ports"] == [21, 23, 3306, 6379], "Common risky ports should match the expected list"
    assert config["SENSITIVE_PORTS"]["3306"] == "MySQL", "Sensitive port 3306 should be MySQL"
    assert config["SENSITIVE_PORTS"]["9200"] == "Elasticsearch", "Sensitive port 9200 should be Elasticsearch"
def test_read_default_ports(tmp_path):
    """
    Test read_DEFAULT_PORTS to ensure it reads default ports correctly.
    """
    # Crear un archivo defaults.yaml válido
    defaults_file = tmp_path / "defaults.yaml"
    defaults_file.write_text("""
    default_ports:
      - 80
      - 443
    """)

    # Mockear el directorio del archivo para que apunte al archivo temporal
    from redink.config.loader import read_DEFAULT_PORTS
    read_DEFAULT_PORTS.__globals__["Path"] = lambda _: defaults_file

    ports = read_DEFAULT_PORTS()
    assert ports == [80, 443], "Default ports should be read correctly"

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