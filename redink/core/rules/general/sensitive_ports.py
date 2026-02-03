#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
from redink.core.model import Finding
from redink.core.rules.base import Rule
from redink.config.loader import read_SENSITIVE_PORTS
class SensitivePortRule(Rule):
    rule_id = "sensitive_port_exposed"
    service = "generic"
    severity = "high"

    SENSITIVE_PORTS = read_SENSITIVE_PORTS()

    def evaluate(self, scan_result: dict) -> Finding | None:
        port = scan_result.get("port")

        if port not in self.SENSITIVE_PORTS:
            return None

        service_name = self.SENSITIVE_PORTS[port]

        return Finding(
            rule_id=self.rule_id,
            service="generic",
            evidence=(
                f"Sensitive service port {port} ({service_name}) "
                "is exposed and may allow unauthorized access."
            )
        )
