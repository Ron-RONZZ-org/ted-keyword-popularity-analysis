"""Pipeline configuration for TED Keyword Popularity Analysis.

All tunable parameters and file paths are declared in the
:class:`TEDAnalysisConfig` dataclass.  No module in this package hardcodes
a threshold or a path — they all read from a config instance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class TEDAnalysisConfig:
    """Configuration for the TED Keyword Popularity Analysis pipeline.

    All pipeline parameters are defined here.  Modules import the config
    class rather than hardcoding values.  Path fields are relative to the
    project root directory (assumed to be the current working directory at
    runtime).

    The dataclass is frozen (immutable) to prevent accidental modification
    after construction.

    Fields are grouped by concern:
    - **Data source**: TED YouTube channel identifiers and API credentials.
    - **Transcript acquisition**: ``yt-transcript-pro`` settings.
    - **YouTube API**: View-count fetch settings.
    - **Preprocessing**: Tokenization and stopword parameters.
    - **Analysis**: Weighted TF, bootstrap, TF-IDF, and subsampling.
    - **Paths**: Input / output directories and filenames.
    """

    # ── TED data source ───────────────────────────────────────────────
    channel_id: str = "UCAuUUnT6oDeKwE6v1NGQxug"
    """YouTube channel ID for the official TED Talks channel (~5,700 videos)."""

    channel_url: str = "https://www.youtube.com/@TED"
    """Full YouTube channel URL (handle form), used by ``yt-transcript-pro``."""

    youtube_api_key_env: str = "YOUTUBE_API_KEY"
    """Environment variable name that holds the YouTube Data API v3 key."""

    # ── Transcript acquisition (yt-transcript-pro) ────────────────────
    transcript_concurrency: int = 5
    """Number of concurrent transcript fetch requests. Lower to 2 on cloud IPs."""

    transcript_backend: str = "auto"
    """Backend for ``yt-transcript-pro`` (``"auto"`` cascades 4 endpoints)."""

    transcript_retries: int = 5
    """Maximum retries per video when transcript fetch fails."""

    transcript_languages: tuple[str, ...] = ("en", "en-US", "en-GB")
    """Preferred language codes for transcript fallback, in order."""

    transcript_cookies_file: str | None = None
    """Path to a Netscape-format cookies file for authenticated transcript access.

    When set (e.g. ``"data/external/cookies.txt"``), this file is passed to
    ``yt-transcript-pro`` which uses it to authenticate with YouTube.
    Useful when running from an IP that YouTube blocks for unauthenticated
    transcript requests.

    .. note::
       Cookie auth is currently **disabled** in the upstream
       ``youtube-transcript-api`` library.  If cookies don't work, use
       ``transcript_proxy`` instead.
    """

    transcript_proxy: str | None = None
    """HTTP/SOCKS proxy URL for transcript fetching (e.g.
    ``"http://user:pass@host:port"`` or ``"socks5://host:port"``).

    This is passed to the ``youtube-transcript-api`` library which uses it
    to work around IP-based blocking by YouTube.  See the library's README
    for proxy provider recommendations.
    """

    # ── YouTube Data API settings ─────────────────────────────────────
    api_batch_size: int = 50
    """Number of video IDs per ``videos.list`` request (YouTube max is 50)."""

    api_retries: int = 3
    """Number of retries with exponential backoff on 429 / quota errors."""

    # ── Preprocessing ─────────────────────────────────────────────────
    min_word_length: int = 2
    """Minimum character length for a token to be kept (shorter tokens discarded)."""

    stopwords_language: str = "english"
    """Language identifier passed to ``nltk.corpus.stopwords.words()``."""

    # ── Analysis ──────────────────────────────────────────────────────
    n_top_keywords: int = 100
    """Number of top keywords to report in output tables and figures."""

    n_bootstrap: int = 1000
    """Number of bootstrap resamples for confidence intervals."""

    bootstrap_ci_level: float = 0.95
    """Confidence level for bootstrap percentile intervals."""

    subsample_fractions: tuple[float, ...] = (0.5, 0.75)
    """Fractions of videos to randomly subsample for Spearman rank-stability analysis."""

    # ── Paths (relative to project root) ──────────────────────────────
    data_dir: Path = field(default_factory=lambda: Path("data"))
    """Top-level data directory."""

    raw_dir: Path = field(default_factory=lambda: Path("data") / "raw")
    """Directory for raw (unprocessed) downloaded data."""

    processed_dir: Path = field(default_factory=lambda: Path("data") / "processed")
    """Directory for cleaned / tokenised intermediate data."""

    external_dir: Path = field(default_factory=lambda: Path("data") / "external")
    """Directory for tracked reference / metadata files (currently unused by pipeline)."""

    results_dir: Path = field(default_factory=lambda: Path("results"))
    """Top-level results directory."""

    figures_dir: Path = field(default_factory=lambda: Path("results") / "figures")
    """Directory for output figures (PDF and PNG)."""

    logs_dir: Path = field(default_factory=lambda: Path("logs"))
    """Directory for pipeline execution logs."""

    # ── Output filenames ──────────────────────────────────────────────
    raw_data_filename: str = "ted_dataset.csv"
    """Filename for the raw merged dataset (transcripts + view counts)."""

    processed_data_filename: str = "tokenized_tf.csv"
    """Filename for the tokenised per-video term-frequency data."""

    analysis_results_filename: str = "keyword_analysis_results.json"
    """Filename for the final analysis results (JSON)."""
