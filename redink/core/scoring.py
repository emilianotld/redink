#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

from .model import Finding
from redink.config.loader import load_risk_config, load_scoring_config

def score_finding(finding: Finding) -> int:
    CONFIG = load_scoring_config()

    RULE_SEVERITY = CONFIG.get("RULE_SEVERITY", {})
    SEVERITY_WEIGHTS = CONFIG.get("SEVERITY_WEIGHTS", {})

    rule_id = finding.rule_id.strip().lower()
    severity = RULE_SEVERITY.get(rule_id, "low")

    weight = SEVERITY_WEIGHTS[severity]
    return weight

def risk_to_loss_range(risk_level: str) -> dict:
    CONFIG = load_risk_config()
    risks = CONFIG.get("risk_ranges", {})
    return risks.get(
        risk_level,
        {
            "label": "Unknown",
            "loss_usd": {"min": 0, "max": 0}
        }
    )
