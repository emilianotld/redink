#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

import asyncio
from typing import List, Dict
import logging
from .rules import resolve_target, scan_ports_async

logger = logging.getLogger("redink")

def scan_target(
    target: str,
    ports: List[int],
    timeout: float,
    concurrency: int
) -> List[Dict]:
    """
    Public function of the module.
    Resolves the target and performs the scan.
    """
    
    logger.info("Scanning ports...")
    logger.debug(f"Using timeout={timeout}, concurrency={concurrency}")
    ip = ip = resolve_target(target)
    results = asyncio.run(
        scan_ports_async(
            ip,
            ports,
            timeout=timeout,
            concurrency=concurrency
       )
    )
    
    open_ports = [
        r for r in results if r["status"] == "open"
    ]
    return open_ports
