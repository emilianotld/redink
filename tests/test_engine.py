#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
import pytest
from redink.core.context import ScanContext, ScanFinding, Recommendation
from redink.core.engine import evaluate_service, generate_risk_report

def test_generate_risk_report_empty():
    """
    Test generate_risk_report with no scan results
    """
    target = "example.com"
    scan_results = []
    report = generate_risk_report(target, scan_results)

    # Validate that the report contains a ScanContext object
    assert isinstance(report, ScanContext), "Report should be a ScanContext object"
    assert report.target == target, "Target in ScanContext is incorrect"
    assert report.findings == [], "Findings should be empty"
    assert report.risk_score == 0.0, "Risk score should be 0.0 for no findings"
    assert report.risk_level == "none", "Risk level should be 'none' for no findings"
    assert report.estimated_loss_range == {"label": "None", "loss_usd": {"min": 0, "max": 0}}, \
        "Estimated loss range should be 'none'"


def test_generate_risk_report_with_results():
    """
    Test generate_risk_report with valid scan results
    """
    target = "example.com"
    scan_results = [
        ScanFinding(
            port=80,
            service="HTTP",
            risk="medium",
            score=5.0,
            estimated_loss_range={"min": 100, "max": 500},
            rule_ids=["R1"],
            reasons=["Reason 1"],
            recommendations=[
                Recommendation(
                    title="Fix HTTP",
                    fix="Enable HTTPS",
                    references=["https://example.com/fix-http"]
                )
            ]
        ),
        ScanFinding(
            port=443,
            service="HTTPS",
            risk="low",
            score=2.0,
            estimated_loss_range={"min": 50, "max": 200},
            rule_ids=["R2"],
            reasons=["Reason 2"],
            recommendations=[]
        )
    ]
    report = generate_risk_report(target, scan_results)

    # Validate that the report contains a ScanContext object
    assert isinstance(report, ScanContext), "Report should be a ScanContext object"
    assert report.target == target, "Target in ScanContext is incorrect"
    assert len(report.findings) == 2, "Findings should contain 2 items"
    assert report.risk_score == 3.5, "Risk score should be the average of the findings"
    assert report.risk_level == "medium", "Risk level should be 'medium'"
    assert report.estimated_loss_range == {"min": 75, "max": 350}, \
        "Estimated loss range should be the average of the findings"


def test_evaluate_service_empty():
    """
    Test evaluate_service with no findings
    """
    scan_results = []
    risk = evaluate_service(scan_results)
    assert risk == 0, "Expected a risk level of 0 for no findings"


def test_evaluate_service_with_findings():
    """
    Test evaluate_service with valid findings
    """
    scan_results = [
        ScanFinding(
            port=80,
            service="HTTP",
            risk="medium",
            score=5.0,
            estimated_loss_range={"min": 100, "max": 500},
            rule_ids=["R1"],
            reasons=["Reason 1"],
            recommendations=[]
        ),
        ScanFinding(
            port=443,
            service="HTTPS",
            risk="low",
            score=2.0,
            estimated_loss_range={"min": 50, "max": 200},
            rule_ids=["R2"],
            reasons=["Reason 2"],
            recommendations=[]
        )
    ]
    risk = evaluate_service(scan_results)
    assert risk == 3.5, "Risk level should be the average score of the findings"


def test_generate_risk_report_invalid_input():
    """
    Test generate_risk_report with invalid input
    """
    target = "example.com"
    scan_results = None  # Invalid input

    with pytest.raises(TypeError, match="Scan results must be a list"):
        generate_risk_report(target, scan_results)


def test_evaluate_service_invalid_input():
    """
    Test evaluate_service with invalid input
    """
    scan_results = None  # Invalid input

    with pytest.raises(TypeError, match="Scan results must be a list"):
        evaluate_service(scan_results)