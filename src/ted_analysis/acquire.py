"""Data acquisition — download and validate raw data.

See ``AGENTS-acquire.md`` for the full specification.
"""

from __future__ import annotations

import logging

from ted_analysis import ROOT_LOGGER_NAME
from ted_analysis.config import TEDAnalysisConfig

logger = logging.getLogger(ROOT_LOGGER_NAME)


def main(config: TEDAnalysisConfig | None = None) -> None:
    """Run the data acquisition stage.

    Args:
        config: Pipeline configuration.  Falls back to ``TEDAnalysisConfig()``
            defaults when ``None``.

    Raises:
        NotImplementedError: This module is a stub — override it with
            project-specific download logic.
    """
    cfg = config or TEDAnalysisConfig()
    msg = (
        f"acquire.py is a stub.  Implement:\n"
        f"  1. Fetch TED Talk transcripts via yt-transcript-pro\n"
        f"  2. Fetch view counts via YouTube Data API v3\n"
        f"  3. Merge and validate schema \u2192 {cfg.raw_dir / cfg.raw_data_filename}\n"
        f"  4. See AGENTS-acquire.md for details"
    )
    logger.error(msg)
    raise NotImplementedError(msg)


if __name__ == "__main__":
    main()
