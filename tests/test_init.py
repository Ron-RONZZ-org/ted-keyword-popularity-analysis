"""Tests for the package __init__ module (logging setup)."""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path

from pkg import setup_logging


class TestSetupLogging:
    """Verify the logging setup works correctly."""

    def test_logging_creates_file(self) -> None:
        """setup_logging creates a log file in the specified directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir) / "logs"
            setup_logging(str(log_dir))
            logger = logging.getLogger("pkg")
            logger.info("Test message")
            logger.handlers.clear()  # clean up for other tests

            log_file = log_dir / "pipeline.log"
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test message" in content

    def test_logging_is_idempotent(self) -> None:
        """Calling setup_logging twice does not duplicate handlers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir) / "logs"
            setup_logging(str(log_dir))
            logger = logging.getLogger("pkg")
            n_handlers = len(logger.handlers)
            setup_logging(str(log_dir))
            assert len(logger.handlers) == n_handlers
            logger.handlers.clear()

    def test_log_format_contains_level_and_name(self) -> None:
        """Log lines include timestamp, level, logger name, and message."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir) / "logs"
            setup_logging(str(log_dir))
            logger = logging.getLogger("pkg")
            logger.info("Format check")
            logger.handlers.clear()

            log_file = log_dir / "pipeline.log"
            content = log_file.read_text()
            assert "INFO" in content
            assert "pkg" in content
            assert "Format check" in content
