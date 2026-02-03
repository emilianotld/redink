#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

import asyncio
import socket
from typing import List, Dict
from redink.core.exceptions import TargetResolutionError

async def check_port(host: str, port: int, timeout: float = 1.0) -> Dict:
    """
    Try establishing a TCP connection to the specified port.
    If it connects, the port is considered open.
    """
    try:
        conn = asyncio.open_connection(host, port)
        reader, writer = await asyncio.wait_for(conn, timeout=timeout)
        writer.close()
        await writer.wait_closed()

        return {
            "port": port,
            "status": "open"
        }

    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return {
            "port": port,
            "status": "closed"
        }

async def scan_ports_async(
    host: str,
    ports: List[int],
    timeout: float,
    concurrency: int,
) -> List[Dict]:
    """
    Scan multiple ports in parallel using asyncio.
    """
    semaphore = asyncio.Semaphore(concurrency)

    async def guarded_check(port: int):
        async with semaphore:
            return await check_port(host, port, timeout=timeout)

    tasks = [
        guarded_check(port)
        for port in ports
    ]

    results = await asyncio.gather(*tasks)
    return results

def resolve_target(target: str) -> str:
    """
    Resolves domain to IP.
    """
    try:
        return socket.gethostbyname(target)
    except socket.gaierror as e:
        raise TargetResolutionError(
            f"Unable to resolve target '{target}'",
            cause=e
        ) from e

