#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

import argparse
from redink import __version__

def build_parser():
    parser = argparse.ArgumentParser(
        prog="redink",
        description=(
            "redink - Exposure & Risk Analysis Framework\n\n"
            "A read-only, non-intrusive security analysis tool designed to\n"
            "identify exposure and configuration risks that may lead to\n"
            "real business impact.\n\n"
            "This tool must only be used on systems you own or are explicitly\n"
            "authorized to assess."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "target",
        nargs="?",
        help="Target hostname or IP address"
    )

    parser.add_argument(
        "--ports",
        type=str,
        help="Ports to scan (e.g. 80,443 or 1-1024)",
        default=None
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="HTTP request timeout in seconds (default: 5)"
    )

    parser.add_argument(
        "--concurrency",
        type=int,
        default=100,
        help="Maximum concurrent connections"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format (machine-readable)"
    )

    parser.add_argument(
        "--risk-only",
        action="store_true",
        help="Display only risk assessment results"
    )

    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Disable startup ASCII banner"
    )

    parser.add_argument(
        "--verify-tls",
        action="store_true",
        help="Enable TLS certificate verification (disabled by default)"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"redink {__version__}"
    )
  
    parser.add_argument(
        "-o",
        "--output",
        choices=["normal", "json", "quiet"],
        default="normal",
        help="Output format: normal (default), json, quiet"
    )
    
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (-v, -vv, -vvv)"
    )

    parser.add_argument(
        "--silent",
        action="store_true",
        help="Suppress all non-essential output"
    )

    return parser
