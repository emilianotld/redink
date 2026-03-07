#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List
from redink.core.model import Finding

@dataclass
class ScanReport:
    """
    Structured representation of a scan report, containing all relevant
    information about the findings, metadata, and context.
    """
    findings: List[Finding]
    metadata: Dict[str, Any] = field(default_factory=dict)