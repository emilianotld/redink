#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
from .types import Recommendation

RECOMENDATIONS = [
    Recommendation(
        rule_id="tls_missing_hsts",
        service="tls",
        title="HSTS Not Enabled",
        description="Allows downgrade attacks from HTTPS to HTTP",
        fix="Enable Strict-Transport-Security header with an appropriate max-age",
        references=["OWASP A02:2021", "RFC 6797"]
    ),
    Recommendation(
        rule_id="weak_tls_configuration",
        service="tls",
        title="Weak TLS Configuration",
        description="Outdated TLS versions or weak ciphers may be supported",
        fix="Disable TLS 1.0/1.1 and enforce strong cipher suites (TLS 1.2 or higher)",
        references=["OWASP A02:2021", "NIST SP 800-52r2"]
    ),
]