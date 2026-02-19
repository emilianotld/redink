#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
import json

def render_json(report):
    """
    Render the report in JSON format.

    Args:
        report (dict): The report data to render.

    Returns:
        str: The JSON-formatted string of the report.
    """
    try:
        # Convert the report dictionary to a JSON string
        return json.dumps(report, indent=4)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Failed to render report as JSON: {e}")