"""Tests for the config module."""

from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest

from pkg.config import ProjectConfig


class TestProjectConfig:
    """Verify the config dataclass has sensible defaults."""

    def test_default_construction(self) -> None:
        """A config can be constructed with no arguments."""
        config = ProjectConfig()
        assert isinstance(config, ProjectConfig)

    def test_frozen_prevents_mutation(self) -> None:
        """The dataclass is frozen — attribute assignment raises FrozenInstanceError."""
        config = ProjectConfig()
        with pytest.raises(dataclasses.FrozenInstanceError):
            config.raw_data_filename = "overridden.csv"  # type: ignore[misc]

    def test_default_paths_are_relative(self) -> None:
        """Default path fields are relative Path objects."""
        config = ProjectConfig()
        assert isinstance(config.data_dir, Path)
        assert not config.data_dir.is_absolute()  # relative to project root
        assert config.raw_dir.name == "raw"
        assert config.processed_dir.name == "processed"

    def test_output_filenames_have_defaults(self) -> None:
        """Output filename fields have non-empty defaults."""
        config = ProjectConfig()
        assert config.raw_data_filename.endswith(".csv")
        assert config.processed_data_filename.endswith(".csv")
        assert config.analysis_results_filename.endswith(".json")

    def test_logs_dir_default(self) -> None:
        """logs_dir defaults to 'logs'."""
        config = ProjectConfig()
        assert config.logs_dir == Path("logs")

    def test_missing_config_fields_from_agents(self) -> None:
        """Fields referenced in AGENTS-*.md files exist on ProjectConfig."""
        config = ProjectConfig()
        # AGENTS-acquire.md references config.local_fallback_dir
        assert hasattr(config, "local_fallback_dir")
        # AGENTS-analysis.md references config.n_bootstrap and .bootstrap_ci_level
        assert hasattr(config, "n_bootstrap")
        assert hasattr(config, "bootstrap_ci_level")
