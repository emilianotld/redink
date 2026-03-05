#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
YAML report renderer/saver for RedInk.
"""

from typing import Any, Optional
import os
from datetime import datetime, timezone
import dataclasses
import yaml

def _to_primitive(obj: Any) -> Any:
    """
    Convert dataclasses recursively to plain Python structures so YAML can serialize them.
    """
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, dict):
        return {k: _to_primitive(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [_to_primitive(v) for v in obj]
    return obj

def render_yaml(report: Any) -> str:
    """
    Render a report object as a YAML string.
    """
    data = _to_primitive(report)
    return yaml.safe_dump(
        data,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
        width=1000,
    )

def save_report_as_yaml(report: Any, output_dir: str = "report", filename: Optional[str] = None) -> str:
    """
    Save the report in YAML format to the given directory.
    Returns the path to the written file.
    """
    content = render_yaml(report)
    os.makedirs(output_dir, exist_ok=True)

    # Determine a sensible filename if none provided
    target = "report"
    if isinstance(report, dict):
        target = report.get("target") or report.get("host") or target
    else:
        target = getattr(report, "target", target)

    safe_target = str(target).replace(os.sep, "_")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if filename:
        outpath = os.path.join(output_dir, filename)
    else:
        outpath = os.path.join(output_dir, f"{safe_target}_{timestamp}.yaml")

    with open(outpath, "w", encoding="utf-8") as fh:
        fh.write(content)

    return outpath