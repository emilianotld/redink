#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

from dataclasses import dataclass

@dataclass
class Finding:
    rule_id: str
    evidence: str
    service: str
    
    def __bool__(self):
        return True
