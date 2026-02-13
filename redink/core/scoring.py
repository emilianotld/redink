#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

from .model import Finding
from redink.config.loader import load_risk_config, load_scoring_config

# Cargar configuraciones una sola vez al inicio del módulo
SCORING_CONFIG = load_scoring_config()
RISK_CONFIG = load_risk_config()

def score_finding(finding: Finding) -> int:
    """
    Scores a finding based on its rule severity.

    Args:
        finding (Finding): The finding to score.

    Returns:
        int: The weight of the finding based on its severity.

    Raises:
        ValueError: If the finding's rule ID is invalid or if the severity is not found in the configuration.
    """
    if not isinstance(finding, Finding):
        raise ValueError("Invalid finding object provided.")
    
    if not finding.rule_id:
        raise ValueError("Finding must have a valid rule_id.")
    
    if not isinstance(finding.rule_id, str):
        raise ValueError("Finding's rule_id must be a string.")

    RULE_SEVERITY = SCORING_CONFIG.get("RULE_SEVERITY", {})
    SEVERITY_WEIGHTS = SCORING_CONFIG.get("SEVERITY_WEIGHTS", {})

    rule_id = finding.rule_id.strip().lower()
    severity = RULE_SEVERITY.get(rule_id, "low")

    if severity not in SEVERITY_WEIGHTS:
        raise ValueError(f"Severity '{severity}' not found in configuration.")

    weight = SEVERITY_WEIGHTS[severity]
    return weight

def risk_to_loss_range(risk_level: str) -> dict:
    """
    Maps a risk level to a financial loss range.

    Args:
        risk_level (str): The risk level to evaluate (e.g., "low", "medium", "high").

    Returns:
        dict: A dictionary containing the loss range for the given risk level.

    Raises:
        ValueError: If the risk level is not a string.
    """
    if not isinstance(risk_level, str):
        raise ValueError("Risk level must be a string.")

    risks = RISK_CONFIG.get("risk_ranges", {})
    return risks.get(
        risk_level.lower(),
        {
            "label": "Unknown",
            "loss_usd": {"min": 0, "max": 0}
        }
    )