#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

from redink.core.context import ScanContext

def print_service_report(services: dict) -> None: 
    for service in services: 
        print(f"Service: {service.get('service')}") 
        details = service.get('details', {}) 
        print(f"Estate: {details.get('status_code', 'N/A')}") 
        print(f"Server: {details.get('server', 'N/A')}") 
        print("Security headers:") 
        security_headers = details.get("security_headers", {})
        if not security_headers: 
         print("[!] No security headers detected")
        else: 
         for header, value in security_headers.items(): 
            print(f" {header}: {value}") 
            print("-" * 30)

def print_final_report(report: ScanContext) -> None:
    print("\n" + "=" * 70)
    print("[ redink ] Risk Assessment Report")
    print("=" * 70)

    print(f"\nTarget               : {report.target}")
    print(f"Open ports detected  : {report.open_ports}")
    print(f"Overall risk score   : {report.risk_score:.1f}")
    print(f"Overall risk level   : {report.risk_level.upper()}")

    loss = report.estimated_loss_range.get("loss_usd", {})
    print(
        f"Estimated loss       : "
        f"${loss.get('min', 0)} - ${loss.get('max', 0)}"
    )

    print("\n" + "-" * 70)
    print("Findings")
    print("-" * 70)

    for finding in report.findings:
        print(
            f"\n[ Port {finding.port} | {finding.service} ]"
        )
        print(f"  Risk level     : {finding.risk.upper()}")
        print(f"  Risk score     : {finding.score}")

        loss = finding.estimated_loss_range["loss_usd"]
        print(
            f"  Estimated loss : "
            f"${loss['min']} - ${loss['max']}"
        )

        reasons = finding.reasons
        if reasons:
            print("  Reasons:")
            for reason in reasons:
                print(f"   - {reason}")

        recommendations = finding.recommendations
        if recommendations:
            print("  Recommendations:")
            print_recommendations(recommendations)

    print("\n" + "=" * 70)
    print("Note:")
    print("Estimated losses are indicative ranges based on industry benchmarks.")
    print("This report does not represent actual financial damage.")
    print("=" * 70 + "\n")

def print_recommendations(recommendations: list) -> None:
    for rec in recommendations:
        print(f"   • {rec.title}")
        print(f"     Fix: {rec.fix}")

        refs = rec.references
        if refs:
            print(f"     Reference: {', '.join(refs)}")

