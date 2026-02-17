#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
import logging
import pytest
from redink.shell.logger import setup_logger

def test_logger_info_level(capsys):
    """
    Test logger at INFO level.
    """
    logger = setup_logger(verbosity=2, silent=False)
    logger.info("This is an info message.")
    captured = capsys.readouterr()
    assert "[INFO]" in captured.out
    assert "This is an info message." in captured.out

def test_logger_debug_level(capsys):
    """
    Test logger at DEBUG level.
    """
    logger = setup_logger(verbosity=3, silent=False)
    logger.debug("This is a debug message.")
    captured = capsys.readouterr()
    assert "[DEBUG]" in captured.out
    assert "This is a debug message." in captured.out

def test_logger_silent(capsys):
    """
    Test logger in silent mode.
    """
    logger = setup_logger(verbosity=2, silent=True)
    logger.info("This message should not appear.")
    captured = capsys.readouterr()
    assert captured.out == ""

def test_logger_warning_level(capsys):
    """
    Test logger at WARNING level.
    """
    logger = setup_logger(verbosity=1, silent=False)
    logger.warning("This is a warning message.")
    captured = capsys.readouterr()
    assert "[WARNING]" in captured.out
    assert "This is a warning message." in captured.out

def test_logger_error_level(capsys):
    """
    Test logger at ERROR level.
    """
    logger = setup_logger(verbosity=0, silent=False)
    logger.error("This is an error message.")
    captured = capsys.readouterr()
    assert "[ERROR]" in captured.out
    assert "This is an error message." in captured.out