#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

import sys
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
    
    try:
        #Initial ports scanning 
        open_ports = scan_target(
            target=args.target,
            ports=ports,                 
            timeout=args.timeout,        # timeout value from parser
            concurrency=args.concurrency # concurrency value from parser
        )
        services = fingerprint_services(host=args.target, open_ports=open_ports)
        print(f"Identified services: {services}")
        report = generate_risk_report(target=args.target, scan_results=services)
        
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
