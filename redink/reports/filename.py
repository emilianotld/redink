#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

from datetime import datetime, timezone
import os


def generate_report_filename(report, output_dir="report", extension="json"):
    """
    Generate a unique filename for the report based on the target and timestamp.

    Args:
        report (ScanContext or dict): The report data to generate the filename from.
        output_dir (str): The directory where the report will be saved.
        extension (str): The file extension for the report.

    Returns:
        str: The generated filename for the report.
    """
    # Determine a sensible filename if none provided
    target = "report"
    if isinstance(report, dict):
        target = report.get("target") or target
    else:
        target = getattr(report, "target", target)

    safe_target = str(target).replace(os.sep, "_")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    filename = f"{safe_target}_{timestamp}.{extension}"
    return filename