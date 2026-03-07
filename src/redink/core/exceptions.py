#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""

class RedInkError(Exception):
    """
    Base exception for all RedInk errors.
    """
    def __init__(self, message: str, *, cause: Exception | None = None):
        super().__init__(message)
        self.cause = cause

class TargetResolutionError(RedInkError):
    """Failed to resolve or reach target"""

class ScanExecutionError(RedInkError):
    """Port scan or fingerprint failed"""

class RuleEvaluationError(RedInkError):
    """A rule crashed during evaluation"""

class InvalidConfigurationError(RedInkError):
    """Config or YAML is invalid"""

class ReportGenerationError(RedInkError):
    """Failed to generate output report"""

EXIT_OK = 0
EXIT_TARGET_ERROR = 2
EXIT_CONFIG_ERROR = 3
EXIT_INTERNAL_ERROR = 10

