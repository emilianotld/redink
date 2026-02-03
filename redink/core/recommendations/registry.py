#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
from .http import RECOMMENDATIONS as HTTP_RECS
from .ssh import RECOMMENDATIONS as SSH_RECS
from .general import RECOMMENDATIONS as GENERAL_RECS

ALL_RECOMMENDATIONS = (
    HTTP_RECS +
    SSH_RECS +
    GENERAL_RECS
)

def get_recommendations(rule_id=None, service=None):
    results = ALL_RECOMMENDATIONS

    if rule_id:
        results = [r for r in results if r.rule_id == rule_id]

    if service:
        results = [r for r in results if r.service in (service, "any")]

    return results
