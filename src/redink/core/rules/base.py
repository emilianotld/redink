#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
from abc import ABC, abstractmethod

class Rule(ABC):
    rule_id: str
    service: str

    @abstractmethod
    def evaluate(self, scan_result: dict):
        """
        Return Finding or None
        """
        pass
