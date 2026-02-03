#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
redink.engine

Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

import logging
from redink.core.ruleset import (
    score_port,
    score_security_headers,
    score_server_disclosure
)
from redink.core.ruleset import classify_risk
from redink.core.scoring import score_finding, risk_to_loss_range
from redink.core.recommendations.registry import get_recommendations
from redink.core.model import Finding
from redink.core.rules import RULES_BY_SERVICE
from redink.core.context import Recommendation, ScanContext, ScanFinding

def evaluate_service(scan_result: dict) -> Finding:
    port = scan_result["port"]
    service = scan_result.get("service", "unknown")
    logger = logging.getLogger("redink")
    logger.info(f"Evaluating service {service} on port {port}...")
    # 1. Execute rules
    try:
        triggered_findings = execute_rules(service = service, scan_result = scan_result)
    except Exception as e:
        logger.error(f"Error executing rules for service {service} on port {port}: {e}")
        triggered_findings = []

    # 2. Scoring
    try: 
        total_score = 0.0
        total_score += score_port(port)

        if not isinstance(port, int) or not (1 <= port <= 65535):
            logger.warning(f"Invalid port: {port}. Skipping scoring for this port.")
        else:
            total_score += score_port(port)

        fingerprint = scan_result.get("fingerprint", {})
        if not isinstance(fingerprint, dict):
            logger.warning("Invalid fingerprint data. Skipping fingerprint scoring.")
        else:
            total_score += score_security_headers(
                fingerprint.get("security_headers", {})
            )
            total_score += score_server_disclosure(
                fingerprint.get("server", "")
            )

        reasons: list[str] = []
        recommendations: list[Recommendation] = []

        for finding in triggered_findings:
            try: 
                if not hasattr(finding, "evidence") or not hasattr(finding, "rule_id"):
                    logger.warning(f"Invalid finding: {finding}. Missing required attributes.")
                    continue

                score = score_finding(finding)
                total_score += score

                if finding.evidence:
                    reasons.append(finding.evidence)

                recs = get_recommendations(
                    rule_id=finding.rule_id,
                    service=service
                )
                recommendations.extend(recs)
            except Exception as e:
                logger.error(f"Error processing finding {finding}: {e}")
    except Exception as e:
        logger.error(f"Error during scoring process: {e}")

    # 3. Risk classification
    logger.info(f"Total score for service {service} on port {port}: {total_score}")
    try:
        risk_level = classify_risk(total_score)
    except Exception as e:
        logger.error(f"Error classifying risk for service {service} on port {port}: {e}")
        risk_level = "unknown"
    try: 
        loss_range = risk_to_loss_range(risk_level.lower())
    except Exception as e:
        logger.error(f"Error estimating loss range for risk level {risk_level}: {e}")
        loss_range = "unknown"

    # 4. Build domain object
    return ScanFinding(
        port=port,
        service=service,
        risk=risk_level,
        score=round(total_score, 2),
        estimated_loss_range=loss_range,
        rule_ids=[f.rule_id for f in triggered_findings],
        reasons=reasons,
        recommendations=recommendations
    )

def execute_rules(service, scan_result) -> list[Finding]:
    triggered_findings: list = []
    rules = RULES_BY_SERVICE.get(service, [])
    for rule in rules:
        finding = rule.evaluate(scan_result)
        if finding:
            triggered_findings.append(finding)
    return triggered_findings

def generate_risk_report(target: str, scan_results: list) -> dict:
    logger = logging.getLogger("redink")
    logger.info("Evaluating risks...")

    context = ScanContext(target=target)

    for scan_result in scan_results:
        finding = evaluate_service(scan_result)
        context.findings.append(finding)
        
    context.compute_summary()

    return context

