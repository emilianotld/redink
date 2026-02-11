#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

from redink.core.context import ScanContext
from redink.core.engine import evaluate_service, generate_risk_report


def test_generate_risk_report():
    """
    Test generate_risk_report with no scan results
    """
    target = "example.com"
    scan_results = []
    report = generate_risk_report(target, scan_results)
    assert report == {}, "Expected an empty report for no scan results"
    

def test_evaluate_service():
    """
    Test evaluate_service with no findings
    """
    scan_results = []
    risk = evaluate_service(scan_results)
    assert risk == 0, "Expected a risk level of 0 for no findings"
    risk = evaluate_service(scan_results)
     