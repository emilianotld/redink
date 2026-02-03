#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
from .types import Recommendation

RECOMENDATIONS = [
    Recommendation(
        rule_id="db_exposed_service",
        service="database",
        title="Database Service Exposed to Network",
        description="Exposed database ports increase attack surface and risk of unauthorized access",
        fix="Restrict database access to internal networks or localhost using firewall rules",
        references=["OWASP A05:2021"]
    ),
    Recommendation(
        rule_id="db_weak_authentication",
        service="database",
        title="Weak Database Authentication Controls",
        description="Weak or default credentials may allow unauthorized database access",
        fix="Enforce strong authentication, rotate credentials, and disable default accounts",
        references=["OWASP A02:2021", "CIS Database Benchmarks"]
    ),
]