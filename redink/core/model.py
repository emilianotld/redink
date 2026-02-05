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
    """
    Represents a basic finding detected during the risk evaluation process.

    Attributes:
        rule_id (str): The identifier of the rule that triggered this finding.
        evidence (str): A description or evidence supporting the finding.
        service (str): The service associated with the finding (e.g., HTTP, SSH).
    """
    rule_id: str
    evidence: str
    service: str
    
    def __bool__(self):
        """
        Determines the truthiness of the finding. Always returns True,
        indicating that the finding is valid or exists.

        Returns:
            bool: Always True.
        """
        return True