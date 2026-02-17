#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
import re
import pytest
from redink.shell.logger import setup_logger

def test_logger_error_level(capsys):
    """
    Test logger at ERROR level.
    """
    logger = setup_logger(verbosity=0, silent=False)
    logger.error("This is an error message.")
    logger.warning("This warning message should not appear.")
    captured = capsys.readouterr()

    error_pattern = r"\[\d{2}:\d{2}:\d{2}\] \[ERROR\] This is an error message\."
    warning_pattern = r"\[\d{2}:\d{2}:\d{2}\] \[WARNING\] This warning message should not appear\."

    assert re.search(error_pattern, captured.err), "Expected ERROR log not found"
    assert not re.search(warning_pattern, captured.err), "Unexpected WARNING log found"

def test_logger_info_level(capsys):
    """
    Test logger at INFO level.
    """
    logger = setup_logger(verbosity=2, silent=False)
    logger.info("This is an info message.")
    captured = capsys.readouterr()

    # Use regex to match the log format, ignoring the exact time
    info_pattern = r"\[\d{2}:\d{2}:\d{2}\] \[INFO\] This is an info message\."
    assert re.search(info_pattern, captured.err), "Expected INFO log not found"

def test_logger_debug_level(capsys):
    """
    Test logger at DEBUG level.
    """
    logger = setup_logger(verbosity=3, silent=False)
    logger.debug("This is a debug message.")
    captured = capsys.readouterr()

    # Use regex to match the log format, ignoring the exact time
    debug_pattern = r"\[\d{2}:\d{2}:\d{2}\] \[DEBUG\] This is a debug message\."
    assert re.search(debug_pattern, captured.err), "Expected DEBUG log not found"

def test_logger_silent(capsys):
    """
    Test logger in silent mode.
    """
    logger = setup_logger(verbosity=2, silent=True)
    logger.info("This message should not appear.")
    logger.error("This error should appear.")
    captured = capsys.readouterr()

    # Use regex to match the log format, ignoring the exact time
    error_pattern = r"\[\d{2}:\d{2}:\d{2}\] \[ERROR\] This error should appear\."
    assert re.search(error_pattern, captured.err), "Expected ERROR log not found"
    assert "This message should not appear." not in captured.err

def test_logger_warning_level(capsys):
    """
    Test logger at WARNING level.
    """
    logger = setup_logger(verbosity=1, silent=False)
    logger.warning("This is a warning message.")
    logger.info("This info message should not appear.")
    captured = capsys.readouterr()

    # Use regex to match the log format, ignoring the exact time
    warning_pattern = r"\[\d{2}:\d{2}:\d{2}\] \[WARNING\] This is a warning message\."
    assert re.search(warning_pattern, captured.err), "Expected WARNING log not found"
    assert "This info message should not appear." not in captured.err