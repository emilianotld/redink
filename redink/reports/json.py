#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
import os
import json
from datetime import datetime

def save_report_as_json(report, output_dir="reports", filename="report.json"):
    """
    Save the report in JSON format in the specified directory.

    Args:
        report (ScanContext): The ScanContext object to save.
        output_dir (str): The directory where the report will be saved.
        filename (str): The name of the JSON file.

    Returns:
        str: The path to the saved JSON file.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, filename)

    def custom_serializer(obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return str(obj)

    with open(output_file, "w") as f:
        json.dump(report, f, indent=4, default=custom_serializer)

    print(f"Report saved to {output_file}")
    return output_file