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
    target: str
    findings: List["ScanFinding"] = field(default_factory=list)

    open_ports: int = 0
    risk_score: float = 0.0
    risk_level: str = ""
    estimated_loss_range: Dict = field(default_factory=dict)

    def compute_summary(self) -> None:
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


@dataclass
class Recommendation:
    title: str
    fix: str
    references: List[str] = field(default_factory=list)

@dataclass
class ScanFinding:
    port: int
    service: str
    risk: str
    score: float
    estimated_loss_range: Dict
    rule_ids: List[str]
    reasons: List[str]
    recommendations: List[Recommendation]




