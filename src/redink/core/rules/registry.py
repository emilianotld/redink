#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

from collections import defaultdict
from .http.missing_hsts import MissingHSTSRule
from .http.missing_csp import MissingCSPRule
from .http.missing_xframe import MissingXframeRule
from .ssh.open_ssh import OpenSSHRule
from .general.sensitive_ports import SensitivePortRule

def load_rules():
    rules = [
        MissingHSTSRule(),
        MissingCSPRule(),
        MissingXframeRule(),
        OpenSSHRule(),
        SensitivePortRule()
    ]

    registry = defaultdict(list)

    for rule in rules:
        registry[rule.service].append(rule)

    return registry
