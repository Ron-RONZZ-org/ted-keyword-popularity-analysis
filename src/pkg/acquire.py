"""Data acquisition — download and validate raw data.

See ``AGENTS-acquire.md`` for the full specification.
"""

from __future__ import annotations

import logging

from pkg import ROOT_LOGGER_NAME
from pkg.config import ProjectConfig

logger = logging.getLogger(ROOT_LOGGER_NAME)


def main(config: ProjectConfig | None = None) -> None:
    """Run the data acquisition stage.

    Args:
        config: Pipeline configuration.  Falls back to ``ProjectConfig()``
            defaults when ``None``.

    Raises:
        NotImplementedError: This module is a stub — override it with
            project-specific download logic.
    """
    cfg = config or ProjectConfig()
    msg = (
        f"acquire.py is a stub.  Implement:\n"
        f"  1. Download data from source → {cfg.raw_dir / cfg.raw_data_filename}\n"
        f"  2. Validate schema and value ranges\n"
        f"  3. See AGENTS-acquire.md for details"
    )
    logger.error(msg)
    raise NotImplementedError(msg)


if __name__ == "__main__":
    main()
