#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
from .types import Recommendation

RECOMMENDATIONS = [
    Recommendation(
        rule_id="missing_csp",
        service="http",
        title="Missing Content Security Policy",
        description="Increases XSS attack surface",
        fix="Define a strict Content-Security-Policy header",
        references=["OWASP A05:2021"]
    ),
    Recommendation(
        rule_id="missing_xframe",
        service="http",
        title="Missing Content Security Policy",
        description="Increases XSS attack surface",
        fix="Define a strict Content-Security-Policy header",
        references=["OWASP A05:2021"]
    )
]
