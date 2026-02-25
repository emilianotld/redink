#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

from dataclasses import dataclass, field
from typing import Dict, List
from redink.core.ruleset import classify_risk
from redink.core.scoring import risk_to_loss_range

@dataclass
class ScanContext:
    """
    Represents the context of a scan, including findings and computed risk metrics.

    Attributes:
        target (str): The target being scanned (e.g., an IP address or domain).
        findings (List[ScanFinding]): A list of findings detected during the scan.
        open_ports (int): The number of open ports detected on the target.
        risk_score (float): The computed risk score based on the findings.
        risk_level (str): The classified risk level (e.g., "low", "medium", "high").
        estimated_loss_range (Dict): The estimated financial loss range based on the risk level.
    """
    target: str
    findings: List["ScanFinding"] = field(default_factory=list)
    open_ports: int = 0
    risk_score: float = 0.0
    risk_level: str = ""
    estimated_loss_range: Dict = field(default_factory=dict)
    metadata: Dict = field(default_factory=dict)
    
    def add_metadata(self, key: str, value: any):
        """
        Add metadata to the ScanContext object.
        """
        self.metadata[key] = value

    def compute_summary(self) -> None:
        """
        Computes a summary of the scan, including the risk score, risk level,
        and estimated financial loss range.

        This method calculates the number of open ports, averages the risk scores
        of the findings, and classifies the overall risk level.
        """
        self.open_ports = len(self.findings)

        if self.open_ports == 0:
            self.risk_score = 0.0
            self.risk_level = "none"
            self.estimated_loss_range = risk_to_loss_range("none")
            return

        self.risk_score = round(
            sum(f.score for f in self.findings) / self.open_ports,
            2
        )

        self.risk_level = classify_risk(self.risk_score)
        self.estimated_loss_range = risk_to_loss_range(
            self.risk_level.lower()
        )
    
    def __init__(self, target, findings=None, open_ports=0, risk_score=0.0, risk_level="", estimated_loss_range=None):
        self.target = target
        self.findings = findings if findings is not None else []
        self.open_ports = open_ports
        self.risk_score = risk_score
        self.risk_level = risk_level
        self.estimated_loss_range = estimated_loss_range if estimated_loss_range is not None else {}

    def to_dict(self):
        """
        Convert the ScanContext object to a dictionary.

        Returns:
            dict: A dictionary representation of the ScanContext object.
        """
        return {
            "target": self.target,
            "findings": [finding.to_dict() if hasattr(finding, "to_dict") else str(finding) for finding in self.findings],
            "open_ports": self.open_ports,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level,
            "estimated_loss_range": self.estimated_loss_range,
        }

@dataclass
class Recommendation:
    """
    Represents a recommendation for mitigating a specific risk.

    Attributes:
        title (str): The title or summary of the recommendation.
        fix (str): A description of the fix or mitigation strategy.
        references (List[str]): A list of references or links for further information.
    """
    title: str
    fix: str
    references: List[str] = field(default_factory=list)

    def __init__(self, title, fix, references):
        self.title = title
        self.fix = fix
        self.references = references

    def to_dict(self):
        return {
            "title": self.title,
            "fix": self.fix,
            "references": self.references,
        }

@dataclass
class ScanFinding:
    """
    Represents a detailed finding detected during a scan.

    Attributes:
        port (int): The port number where the finding was detected.
        service (str): The service running on the detected port (e.g., HTTP, SSH).
        risk (str): The risk level associated with the finding (e.g., "low", "medium", "high").
        score (float): The risk score assigned to the finding.
        estimated_loss_range (Dict): The estimated financial loss range for this finding.
        rule_ids (List[str]): A list of rule IDs that triggered this finding.
        reasons (List[str]): A list of reasons or explanations for the finding.
        recommendations (List[Recommendation]): A list of recommendations to mitigate the risk.
    """
    port: int
    service: str
    risk: str
    score: float
    estimated_loss_range: Dict
    rule_ids: List[str]
    reasons: List[str]
    recommendations: List[Recommendation]

    def __init__(self, port, service, risk, score, estimated_loss_range, rule_ids, reasons, recommendations):
        self.port = port
        self.service = service
        self.risk = risk
        self.score = score
        self.estimated_loss_range = estimated_loss_range
        self.rule_ids = rule_ids
        self.reasons = reasons
        self.recommendations = recommendations

    def to_dict(self):
        """
        Convert the ScanFinding object to a dictionary.

        Returns:
            dict: A dictionary representation of the ScanFinding object.
        """
        return {
            "port": self.port,
            "service": self.service,
            "risk": self.risk,
            "score": self.score,
            "estimated_loss_range": self.estimated_loss_range,
            "rule_ids": self.rule_ids,
            "reasons": self.reasons,
            "recommendations": [
                rec.to_dict() if hasattr(rec, "to_dict") else str(rec) for rec in self.recommendations
            ],
        }