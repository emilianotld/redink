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
        rule_id="ftp_cleartext_auth",
        service="ftp",
        title="FTP Uses Cleartext Authentication",
        description="Credentials transmitted over FTP can be intercepted via network sniffing",
        fix="Disable FTP or migrate to SFTP/FTPS using encrypted channels",
        references=["OWASP A02:2021", "CIS FTP Benchmark"]
    ),
    Recommendation(
        rule_id="ftp_anonymous_enabled",
        service="ftp",
        title="Anonymous FTP Access Enabled",
        description="Allows unauthenticated users to access the FTP service",
        fix="Disable anonymous FTP access and enforce authenticated users only",
        references=["OWASP A05:2021"]
    ),
]