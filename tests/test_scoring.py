#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
import pytest
from redink.core.scoring import score_finding
from redink.core.model import Finding

def test_score_finding_valid():
    """
    Test score_finding with a valid finding.
    """
    finding = Finding(rule_id="R1", evidence="Test evidence", service="HTTP")
    score = score_finding(finding)
    assert score == 5, "Expected score for rule R1 is 5"

def test_score_finding_invalid():
    """
    Test score_finding with an invalid input.
    """
    with pytest.raises(ValueError, match="Invalid finding object provided."):
        score_finding("invalid_object")