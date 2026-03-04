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
        report (ScanContext): The ScanContext object to render.

    Returns:
        str: The JSON-formatted string of the report.
    """
    try:
        # Convert the ScanContext object to a JSON string
        return json.dumps(report.to_dict(), indent=4, default=custom_serializer)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Failed to render report as JSON: {e}")

def custom_serializer(obj):
    """
    Custom serializer for objects not serializable by default.

    Args:
        obj: The object to serialize.

    Returns:
        dict or str: A dictionary representation of the object, or its string representation.
    """
    if hasattr(obj, "to_dict"):
        # Use the to_dict method if available
        return obj.to_dict()
    if hasattr(obj, "__dict__"):
        # Fallback to using the __dict__ attribute
        return obj.__dict__
    return str(obj)  # As a last resort, convert to string