#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
YAML report renderer/saver for RedInk.
"""

from typing import Any, Optional
import os
import dataclasses
import yaml

from redink.reports.filename import generate_report_filename

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

    filename = filename or generate_report_filename(report, output_dir=output_dir, extension="yaml")
    if filename:
        outpath = os.path.join(output_dir, filename)
    else:
        outpath = os.path.join(output_dir, f"{filename}")

    with open(outpath, "w", encoding="utf-8") as fh:
        fh.write(content)

    return outpath