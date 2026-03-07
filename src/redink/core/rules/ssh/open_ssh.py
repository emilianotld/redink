#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

from  redink.core.rules.base import Rule
from  redink.core.model import Finding

class OpenSSHRule(Rule):
    rule_id = "open_ssh"
    service = "ssh"

    def evaluate(self, scan_result):
        if scan_result["port"] != 22:
         return None
        
        headers = (
            scan_result
            .get("fingerprint", {})
            .get("security_headers", {})
        )

        headers = {h.lower(): v for h, v in headers.items()}

        if "strict-transport-security" not in headers:
            return Finding(
                rule_id=self.rule_id,
                service=self.service,
                evidence="X-Frame-Options header not present"
            )
        return None