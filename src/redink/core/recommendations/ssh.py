#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
from .types import Recommendation

RECOMMENDATIONS = [
    Recommendation(
        rule_id="open_ssh",
        service="ssh",
        title="SSH service exposed",
        description="Increases brute-force risk",
        fix="Restrict SSH access or use key-based auth",
        references=["CIS SSH Benchmark"]
    )
]
