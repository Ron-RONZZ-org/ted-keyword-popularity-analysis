"""Tests for pipeline stub modules — verify they import and raise NotImplementedError."""

from __future__ import annotations

from pathlib import Path

import pytest

from ted_analysis.config import TEDAnalysisConfig


def _stub_test(module_name: str) -> None:
    """Import *module_name* and call ``main()`` — must raise ``NotImplementedError``."""
    import importlib

    mod = importlib.import_module(f"ted_analysis.{module_name}")
    config = TEDAnalysisConfig()
    with pytest.raises(NotImplementedError):
        mod.main(config)


class TestAcquireStub:
    """acquire.py stub raises NotImplementedError."""

    def test_main_raises(self) -> None:
        _stub_test("acquire")


class TestPreprocessStub:
    """preprocess.py stub raises NotImplementedError."""

    def test_main_raises(self) -> None:
        _stub_test("preprocess")


class TestAnalysisStub:
    """analysis.py stub raises NotImplementedError."""

    def test_main_raises(self) -> None:
        _stub_test("analysis")


class TestVisualizeStub:
    """visualize.py stub raises NotImplementedError."""

    def test_main_raises(self) -> None:
        _stub_test("visualize")


class TestReportStub:
    """report.py stub raises NotImplementedError."""

    def test_main_raises(self) -> None:
        _stub_test("report")


class TestValidationStub:
    """_validation.py stub raises NotImplementedError."""

    def test_main_raises(self) -> None:
        _stub_test("_validation")
