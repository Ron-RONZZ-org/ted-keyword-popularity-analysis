"""Preprocessing — NLTK tokenization, stopword removal, per-video TF.

See ``AGENTS-preprocess.md`` for the full specification.
"""

from __future__ import annotations

import logging

from ted_analysis import ROOT_LOGGER_NAME
from ted_analysis.config import TEDAnalysisConfig

logger = logging.getLogger(ROOT_LOGGER_NAME)


def main(config: TEDAnalysisConfig | None = None) -> None:
    """Run the preprocessing stage.

    Args:
        config: Pipeline configuration.  Falls back to ``TEDAnalysisConfig()``
            defaults when ``None``.

    Raises:
        NotImplementedError: This module is a stub — override it with
            project-specific preprocessing logic.
    """
    cfg = config or TEDAnalysisConfig()
    msg = (
        f"preprocess.py is a stub.  Implement:\n"
        f"  1. Read raw data from {cfg.raw_dir / cfg.raw_data_filename}\n"
        f"  2. Tokenize transcripts with NLTK, remove stopwords\n"
        f"  3. Compute per-video term frequency\n"
        f"  4. Write to {cfg.processed_dir / cfg.processed_data_filename}\n"
        f"  5. See AGENTS-preprocess.md for details"
    )
    logger.error(msg)
    raise NotImplementedError(msg)


if __name__ == "__main__":
    main()
