"""Tests for the config module."""

from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest

from ted_analysis.config import TEDAnalysisConfig


class TestTEDAnalysisConfig:
    """Verify the ``TEDAnalysisConfig`` dataclass has sensible defaults."""

    def test_default_construction(self) -> None:
        """A config can be constructed with no arguments."""
        config = TEDAnalysisConfig()
        assert isinstance(config, TEDAnalysisConfig)

    def test_frozen_prevents_mutation(self) -> None:
        """The dataclass is frozen — attribute assignment raises."""
        config = TEDAnalysisConfig()
        with pytest.raises(dataclasses.FrozenInstanceError):
            config.raw_data_filename = "overridden.csv"  # type: ignore[misc]

    def test_default_paths_are_relative(self) -> None:
        """Default path fields are relative Path objects."""
        config = TEDAnalysisConfig()
        assert isinstance(config.data_dir, Path)
        assert not config.data_dir.is_absolute()
        assert config.raw_dir.name == "raw"
        assert config.processed_dir.name == "processed"

    def test_output_filenames_match_project(self) -> None:
        """Output filename defaults match the TED project naming."""
        config = TEDAnalysisConfig()
        assert config.raw_data_filename == "ted_dataset.csv"
        assert config.processed_data_filename == "tokenized_tf.csv"
        assert config.analysis_results_filename == "keyword_analysis_results.json"

    def test_channel_identifiers_set(self) -> None:
        """TED channel IDs are populated correctly."""
        config = TEDAnalysisConfig()
        assert config.channel_id == "UCAuUUnT6oDeKwE6v1NGQxug"
        assert config.channel_url == "https://www.youtube.com/@TED"

    def test_youtube_api_key_env_default(self) -> None:
        """The API-key env-var name defaults to YOUTUBE_API_KEY."""
        config = TEDAnalysisConfig()
        assert config.youtube_api_key_env == "YOUTUBE_API_KEY"

    def test_transcript_settings(self) -> None:
        """Transcript acquisition settings have sensible defaults."""
        config = TEDAnalysisConfig()
        assert config.transcript_concurrency == 5
        assert config.transcript_backend == "auto"
        assert config.transcript_retries == 5
        assert isinstance(config.transcript_languages, tuple)
        assert "en" in config.transcript_languages

    def test_api_settings(self) -> None:
        """YouTube Data API settings have sensible defaults."""
        config = TEDAnalysisConfig()
        assert config.api_batch_size == 50
        assert config.api_retries == 3

    def test_preprocessing_params(self) -> None:
        """Preprocessing defaults are project-appropriate."""
        config = TEDAnalysisConfig()
        assert config.min_word_length == 2
        assert config.stopwords_language == "english"

    def test_analysis_params(self) -> None:
        """Analysis parameters have sensible defaults."""
        config = TEDAnalysisConfig()
        assert config.n_top_keywords == 100
        assert config.n_bootstrap == 1000
        assert config.bootstrap_ci_level == 0.95

    def test_subsample_fractions(self) -> None:
        """Subsample fractions for rank-stability are (0.5, 0.75)."""
        config = TEDAnalysisConfig()
        assert config.subsample_fractions == (0.5, 0.75)

    def test_extra_path_fields(self) -> None:
        """All path fields return sensible Path defaults."""
        config = TEDAnalysisConfig()
        assert config.external_dir == Path("data") / "external"
        assert config.results_dir == Path("results")
        assert config.figures_dir == Path("results") / "figures"
        assert config.logs_dir == Path("logs")

    def test_all_agents_fields_exist(self) -> None:
        """All fields referenced in AGENTS-*.md files exist."""
        config = TEDAnalysisConfig()
        # AGENTS-acquire.md
        assert hasattr(config, "channel_id")
        assert hasattr(config, "channel_url")
        assert hasattr(config, "youtube_api_key_env")
        assert hasattr(config, "transcript_concurrency")
        assert hasattr(config, "transcript_backend")
        assert hasattr(config, "transcript_retries")
        assert hasattr(config, "transcript_languages")
        assert hasattr(config, "api_batch_size")
        assert hasattr(config, "api_retries")
        assert hasattr(config, "raw_dir")
        assert hasattr(config, "raw_data_filename")
        # AGENTS-preprocess.md
        assert hasattr(config, "min_word_length")
        assert hasattr(config, "stopwords_language")
        assert hasattr(config, "processed_dir")
        assert hasattr(config, "processed_data_filename")
        # AGENTS-analysis.md
        assert hasattr(config, "n_top_keywords")
        assert hasattr(config, "n_bootstrap")
        assert hasattr(config, "bootstrap_ci_level")
        assert hasattr(config, "subsample_fractions")
        # AGENTS-visualize.md
        assert hasattr(config, "figures_dir")
        assert hasattr(config, "n_top_keywords")
