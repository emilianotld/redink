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
        rule_id="unencrypted_service",
        service="generic",
        title="Unencrypted Network Service Exposed",
        description="The service communicates without encryption, allowing interception or manipulation of data in transit.",
        fix="Enable TLS/SSL or migrate to a secure alternative that enforces encrypted communication.",
        references=["OWASP A02:2021", "NIST SP 800-52"]
    ),

    Recommendation(
        rule_id="weak_authentication",
        service="generic",
        title="Weak or Legacy Authentication Mechanism",
        description="The service relies on weak authentication mechanisms that are susceptible to brute-force or credential reuse attacks.",
        fix="Enforce strong authentication, disable legacy auth methods, and apply account lockout policies.",
        references=["OWASP A07:2021", "NIST SP 800-63B"]
    ),

    Recommendation(
        rule_id="service_version_disclosure",
        service="generic",
        title="Service Version Disclosure",
        description="The service exposes version or banner information that can help attackers fingerprint the system.",
        fix="Disable service banners and suppress version disclosure where possible.",
        references=["OWASP A06:2021", "CIS Controls v8"]
    ),

    Recommendation(
        rule_id="outdated_software",
        service="generic",
        title="Outdated or Unsupported Software Detected",
        description="The detected service version is outdated and may contain known vulnerabilities.",
        fix="Update the service to a supported version and apply the latest security patches.",
        references=["CVE Details", "NIST SP 800-40"]
    ),

    Recommendation(
        rule_id="excessive_port_exposure",
        service="generic",
        title="Unnecessary Network Port Exposure",
        description="The service is exposed on a network port that may not be required for normal operation.",
        fix="Restrict access using firewall rules or disable the service if it is not strictly necessary.",
        references=["CIS Controls v8", "NIST SP 800-41"]
    ),

    Recommendation(
        rule_id="missing_security_headers",
        service="http",
        title="Missing Security Headers",
        description="The HTTP service does not implement recommended security headers, increasing exposure to common web attacks.",
        fix="Configure HTTP security headers such as Content-Security-Policy, X-Frame-Options, and X-Content-Type-Options.",
        references=["OWASP Secure Headers Project"]
    ),

    Recommendation(
        rule_id="default_configuration",
        service="generic",
        title="Default or Insecure Service Configuration",
        description="The service appears to be running with default or insecure configuration settings.",
        fix="Harden the service configuration following vendor and CIS hardening guidelines.",
        references=["CIS Benchmarks"]
    ),

]
