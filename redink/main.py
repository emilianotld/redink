#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

from dataclasses import asdict
from datetime import datetime, timezone
import sys
import uuid
from redink.core.exceptions import InvalidConfigurationError, RedInkError, TargetResolutionError, EXIT_TARGET_ERROR, EXIT_CONFIG_ERROR, EXIT_INTERNAL_ERROR
from redink.modules.ports.scanner import scan_target
from redink.modules.headers.fingerprint import fingerprint_services
from redink.config.common import print_banner
from redink import __version__
from redink.core.engine import generate_risk_report
from redink.config.loader import  read_DEFAULT_PORTS
from redink.shell.parser import build_parser
from redink.shell.cli import parse_ports, print_no_target_error, render_output
from redink.shell.logger import setup_logger

def main():
    parser = build_parser()
    args = parser.parse_args()

    if len(sys.argv) == 1:
        print_banner()
        print_no_target_error()
        sys.exit(1)
        
    logger = setup_logger(verbosity=args.verbose, silent=args.silent)
    DEFAULT_PORTS = read_DEFAULT_PORTS()

    #Initial Banner with the logo of REDINK
    if not args.no_banner:
        print_banner()
    
    if args.ports:
        ports = parse_ports(args.ports)
    else:
        ports = DEFAULT_PORTS
    
    targets = []
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                for line in fh:
                    t = line.split("#", 1)[0].strip()
                    if t:
                        targets.append(t)

            if not targets:
                logger.error("Targets file is empty or contains only comments.")
                sys.exit(EXIT_CONFIG_ERROR)

        except FileNotFoundError:
            logger.error(f"Targets file not found: {args.file}")
            sys.exit(EXIT_CONFIG_ERROR)

        except OSError as e:
            logger.error(f"Error reading targets file: {e}")
            sys.exit(EXIT_CONFIG_ERROR)

    # Add single positional target if present
    if getattr(args, "target", None):
        targets.append(args.target)

    # Add multiple positional targets if present
    if getattr(args, "targets", None):
        for t in args.targets:
            if t:
                targets.append(t)

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for t in targets:
        if t not in seen:
            seen.add(t)
            deduped.append(t)
    targets = deduped

    if not targets:
        logger.error("No target specified.")
        sys.exit(EXIT_CONFIG_ERROR)
   
    
    try:
        for t in targets:            
            open_ports = scan_target(
                target=t,
                ports=ports,
                timeout=args.timeout,
                concurrency=args.concurrency
            )
            services = fingerprint_services(host=t, open_ports=open_ports)
            scan_metadata = {
                "scan_id": str(uuid.uuid4()),
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "redink_version": __version__,
            }
            report = generate_risk_report(target=t, scan_results=services, scan_metadata=scan_metadata)
            render_output(report, args.output)
        
    except TargetResolutionError as e:
        logger.error(e)
        sys.exit(EXIT_TARGET_ERROR)

    except InvalidConfigurationError as e:
        logger.error(e)
        sys.exit(EXIT_CONFIG_ERROR)

    except RedInkError as e:
        logger.error(e)
        if args.verbose:
            logger.debug(e.cause)
        sys.exit(EXIT_INTERNAL_ERROR)
        
if __name__ == "__main__":
    main()
