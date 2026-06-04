"""Pytest configuration and shared fixtures."""

from __future__ import annotations

import logging
from typing import Generator

import pytest

from ted_analysis import ROOT_LOGGER_NAME


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line("markers", "slow: marks tests that take >2 seconds to run")


@pytest.fixture(autouse=True)
def _disable_logging(caplog: pytest.LogCaptureFixture) -> Generator[None, None, None]:
    """Suppress log output during tests.

    The project root logger is set to CRITICAL for the duration of every
    test.  Individual tests can override by calling ``caplog.set_level(...)``.
    """
    caplog.set_level(logging.CRITICAL, logger=ROOT_LOGGER_NAME)
    yield
