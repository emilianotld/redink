#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

from typing import List
from redink.reports.console import print_final_report

def parse_ports(value: str) -> List[int]:
    
    ports = set()

    for part in value.split(","):
        if "-" in part:
            start, end = part.split("-")
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(part))

    return sorted(ports)


def render_output(report, mode="normal"):
   """Renders the final report based on the specified mode.""" 
   
   if mode == "json":
       print("JSON mode not implemented yet")
       #return render_json(report)
   elif mode == "quiet":
       print("Quiet mode not implemented yet")
       #return render_quiet(report)
   else:
        print_final_report(report)

def print_no_target_error():
    print("\n[!] Missing target")
    print("You must specify a target host or IP address.\n")
    print("Example:")
    print("  redink example.com")
    print("  redink 192.168.1.10 --ports 22,80,443\n")
    print("Run 'redink --help' to see all available options.\n")


