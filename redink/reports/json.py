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

def save_report_as_json(report, output_dir="report", filename="report.json"):
    """
    Save the report in JSON format in the specified directory.

    Args:
        report (ScanContext): The ScanContext object to save.
        output_dir (str): The directory where the report will be saved.
        filename (str): The base name of the JSON file.

    Returns:
        str: The path to the saved JSON file.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate a unique filename using a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name, ext = os.path.splitext(filename)
    unique_filename = f"{base_name}_{timestamp}{ext}"
    output_file = os.path.join(output_dir, unique_filename)

    # Serialize el reporte a JSON, manejando objetos no serializables
    def custom_serializer(obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return str(obj)

    # Save the report as a JSON file
    with open(output_file, "w") as f:
        json.dump(report, f, indent=4, default=custom_serializer)

    print(f"Report saved to {output_file}")
    return output_file