#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Recommendation:
    rule_id: str
    service: str
    title: str
    description: str
    fix: str
    references: List[str]
