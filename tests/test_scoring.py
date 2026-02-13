#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
import pytest
from redink.core.scoring import risk_to_loss_range, score_finding
from redink.core.model import Finding

def test_score_finding_valid():
    """
    Test score_finding with a valid finding.
    """
    finding = Finding(rule_id="sensitive_port", evidence="Test evidence", service="http")
    score = score_finding(finding)
    assert score == 5, "Expected score for rule R1 is 5"

def test_score_finding_invalid():
    """
    Test score_finding with an invalid input.
    """
    with pytest.raises(ValueError, match="Invalid finding object provided."):
        score_finding("invalid_object")

def test_risk_to_loss_range_valid():
    """
    Test risk_to_loss_range with valid risk levels.
    """
    low_risk = risk_to_loss_range("low")
    assert low_risk["label"] == "Low Risk"
    assert low_risk["loss_usd"]["min"] == 0
    assert low_risk["loss_usd"]["max"] > 0

    high_risk = risk_to_loss_range("high")
    assert high_risk["label"] == "High Risk"
    assert high_risk["loss_usd"]["min"] > 0
    assert high_risk["loss_usd"]["max"] > high_risk["loss_usd"]["min"]

def test_risk_to_loss_range_unknown():
    """
    Test risk_to_loss_range with an unknown risk level.
    """
    unknown_risk = risk_to_loss_range("unknown")
    assert unknown_risk["label"] == "Unknown"
    assert unknown_risk["loss_usd"]["min"] == 0
    assert unknown_risk["loss_usd"]["max"] == 0