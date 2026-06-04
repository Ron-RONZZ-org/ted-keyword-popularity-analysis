"""Tests for the config module."""

from __future__ import annotations

from pathlib import Path

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
        try:
            config.raw_data_filename = "overridden.csv"  # type: ignore[misc]
            assert False, "Expected FrozenInstanceError"
        except (TypeError, AttributeError):
            pass  # expected for frozen dataclass

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
