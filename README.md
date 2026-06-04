# TED Keyword Popularity Analysis

Which keywords are most globally prominent across all public TED Talks?
This project investigates keyword prominence using **Term Frequency weighted
by view count**, providing a data-driven answer grounded in the full corpus
of ~5,700 TED Talks.

## Pipeline Stages

| `make` target | Module | What it does |
|---|---|---|
| `acquire` | `ted_analysis.acquire` | Download transcripts (via `yt-transcript-pro`) + view counts (YouTube Data API v3) |
| `preprocess` | `ted_analysis.preprocess` | NLTK tokenization, stopword removal, per-video term-frequency |
| `analyze` | `ted_analysis.analysis` | Weighted TF scoring, bootstrap CIs, TF-IDF, temporal trends |
| `visualize` | `ted_analysis.visualize` | Publication-quality figures (PDF + PNG) |
| `report` | `ted_analysis.report` | Summary statistics, tables, Quarto manuscript |
| `test` | `tests/` | Run test suite (independent of data) |

## Setup

```bash
# Create and activate virtual environment
uv venv && source .venv/bin/activate

# Install the package with dev dependencies
uv pip install -e ".[dev]"

# Verify everything works
make test
```

> **Note:** View counts require a YouTube Data API v3 key. Set the
> `YOUTUBE_API_KEY` environment variable before running `make acquire`.
> Transcripts are fetched without an API key via `yt-transcript-pro`.

## Quick Start

```bash
# Run the test suite (no data needed)
make test

# Run the full pipeline (after OSF pre-registration)
make all
```

Individual stages can be run with `make acquire`, `make preprocess`, etc.

## AI Collaboration

This project uses a hierarchical AGENTS.md framework to guide AI-assisted
development. See the [root AGENTS.md](AGENTS.md) for global conventions and
module-level files (`AGENTS-acquire.md`, `AGENTS-preprocess.md`, etc.) for
stage-specific rules.

## License

| Component | License | File |
|---|---|---|
| **Source code** (Python scripts) | **MIT** | [LICENSE](LICENSE) |
| **Non-software materials** (data, figures, report, documentation) | **CC BY 4.0** | [LICENSE.content](LICENSE.content) |
