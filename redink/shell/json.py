#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
import json
from venv import logger

def render_json(report):
    """
    Render the report in JSON format.

    Args:
        report (dict): The report data to render.

    Returns:
        str: The JSON-formatted string of the report.
    """
    try:
        logger.debug("Rendering report as JSON")
        # Convert the report dictionary to a JSON string
        return json.dumps(report, indent=4, default=custom_serializer)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Failed to render report as JSON: {e}")

def custom_serializer(obj):
    """
    Custom serializer for objects not serializable by default.

    Args:
        obj: The object to serialize.

    Returns:
        dict: A dictionary representation of the object.
    """
    if hasattr(obj, "__dict__"):
        # Serialize objects by their __dict__ attribute
        return obj.__dict__
    return str(obj)  # As a fallback, convert to string