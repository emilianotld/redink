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
        report (dict): The report data to save.
        output_dir (str): The directory where the report will be saved.
        filename (str): The name of the JSON file.

    Returns:
        str: The path to the saved JSON file.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate a unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"{filename}_{timestamp}.json")

    try:
        # Save report as JSON file
        with open(output_file, "w") as f:
            json.dump(report, f, indent=4)
        print(f"Report saved to {output_file}")
        return output_file
    except (OSError, ValueError) as e:
        print(f"Failed to save report: {e}")
        return None