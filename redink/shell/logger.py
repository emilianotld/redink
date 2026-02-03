#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

import logging

def setup_logger(verbosity: int, silent: bool):
    if silent:
        level = logging.ERROR
    else:
        if verbosity >= 3:
            level = logging.DEBUG
        elif verbosity == 2:
            level = logging.INFO
        elif verbosity == 1:
            level = logging.WARNING
        else:
            level = logging.ERROR

    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(message)s"
    )

    return logging.getLogger("redink")