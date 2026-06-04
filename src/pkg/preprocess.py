"""Preprocessing — QC, cleaning, and feature extraction.

See ``AGENTS-preprocess.md`` for the full specification.
"""

from __future__ import annotations

import logging

from pkg import ROOT_LOGGER_NAME
from pkg.config import ProjectConfig

logger = logging.getLogger(ROOT_LOGGER_NAME)


def main(config: ProjectConfig | None = None) -> None:
    """Run the preprocessing stage.

    Args:
        config: Pipeline configuration.  Falls back to ``ProjectConfig()``
            defaults when ``None``.

    Raises:
        NotImplementedError: This module is a stub — override it with
            project-specific preprocessing logic.
    """
    cfg = config or ProjectConfig()
    msg = (
        f"preprocess.py is a stub.  Implement:\n"
        f"  1. Read raw data from {cfg.raw_dir / cfg.raw_data_filename}\n"
        f"  2. Apply QC, cleaning, feature engineering\n"
        f"  3. Write processed data to {cfg.processed_dir / cfg.processed_data_filename}\n"
        f"  4. See AGENTS-preprocess.md for details"
    )
    logger.error(msg)
    raise NotImplementedError(msg)


if __name__ == "__main__":
    main()
