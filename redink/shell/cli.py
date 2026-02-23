#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

from typing import List
from redink.reports.console import print_final_report
from redink.reports.json import save_report_as_json
from redink.shell.json import render_json

def parse_ports(value: str) -> List[int]:
    
    ports = set()

    for part in value.split(","):
        if "-" in part:
            start, end = part.split("-")
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(part))

    return sorted(ports)


def render_output(report, mode="normal", output_dir="reports"):
    """
    Renders the final report based on the specified mode.

    Args:
        report (dict): The report data to render.
        mode (str): The output mode ("normal", "json", "quiet").
        output_dir (str): The directory where the report will be saved (for JSON mode).
    """
    if mode == "json":
        # Render the report as a JSON string
        json_report = render_json(report)
        print(json_report)  # Optionally print the JSON to the console
        # Save the report as a JSON file
        save_report_as_json(report, output_dir=output_dir)
    elif mode == "quiet":
        print("Quiet mode not implemented yet")
        report = {}
        return render_quiet()
    else:
            print_final_report(report)

def print_no_target_error():
    print("\n[!] Missing target")
    print("You must specify a target host or IP address.\n")
    print("Example:")
    print("  redink example.com")
    print("  redink 192.168.1.10 --ports 22,80,443\n")
    print("Run 'redink --help' to see all available options.\n")

def render_quiet():
    """
    Render the report in quiet mode.
    This function intentionally does nothing to suppress all output.
    
    Args:
        report (dict): The report data to render (ignored in quiet mode).
    """
    pass  # No output is produced in quiet mode