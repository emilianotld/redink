#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
import logging
from redink.core.rules.base import Rule
from redink.core.model import Finding

class MissingXframeRule(Rule):
    rule_id = "missing_hsts"
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

        if "x-frame-options" not in headers:
            logger = logging.getLogger("redink")
            logger.warning("HTTP header missing HSTS")
            return Finding(
                rule_id=self.rule_id,
                service=self.service,
                evidence="X-Frame-Options header not present"
            )
        return None
