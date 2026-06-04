"""Pipeline configuration.

All tunable parameters and file paths are declared in the
:class:`ProjectConfig` dataclass.  No module in this package hardcodes
a threshold or a path — they all read from a config instance.

Adapt this dataclass per project: add fields for your data source,
QC thresholds, analysis parameters, and output paths.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ProjectConfig:
    """Configuration for the research pipeline.

    All pipeline parameters are defined here.  Modules import the config
    class rather than hardcoding values.  Path fields are relative to the
    project root directory (assumed to be the current working directory at
    runtime).

    The dataclass is frozen (immutable) to prevent accidental modification
    after construction.
    """

    # ── Data source ───────────────────────────────────────────────────
    # TODO: add fields for your data source (URLs, station IDs, etc.)

    # ── QC thresholds ─────────────────────────────────────────────────
    # TODO: add QC thresholds (missing data limits, physical bounds, etc.)

    # ── Analysis parameters ───────────────────────────────────────────
    # TODO: add model parameters, bootstrap settings, etc.

    # ── Output paths (relative to project root) ───────────────────────
    data_dir: Path = field(default_factory=lambda: Path("data"))
    raw_dir: Path = field(default_factory=lambda: Path("data") / "raw")
    processed_dir: Path = field(default_factory=lambda: Path("data") / "processed")
    external_dir: Path = field(default_factory=lambda: Path("data") / "external")
    results_dir: Path = field(default_factory=lambda: Path("results"))
    figures_dir: Path = field(default_factory=lambda: Path("results") / "figures")
    logs_dir: Path = field(default_factory=lambda: Path("logs"))

    # ── Output filenames ──────────────────────────────────────────────
    # TODO: update filenames per project
    raw_data_filename: str = "raw_data.csv"
    processed_data_filename: str = "processed_data.csv"
    analysis_results_filename: str = "analysis_results.json"
