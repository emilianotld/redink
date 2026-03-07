#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
import logging
from  redink.core.rules.base import Rule
from  redink.core.model import Finding

class MissingCSPRule(Rule):
    rule_id = "missing_csp"
    service = "http"

    def evaluate(self, scan_result):
        if scan_result["port"] not in (80, 443):
            return None

        headers = (
            scan_result
            .get("fingerprint", {})
            .get("security_headers", {})
        )

        headers = {h.lower(): v for h, v in headers.items()}

        if "content-security-policy" not in headers:
            logger = logging.getLogger("redink")
            logger.warning("HTTP header missing CSP")

            return Finding(
                rule_id=self.rule_id,
                service=self.service,
                evidence="Content-Security-Policy header not present"
            )
        return None
