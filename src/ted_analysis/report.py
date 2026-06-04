"""Report — summary statistics, tables, and manuscript compilation.

See ``AGENTS-report.md`` for the full specification.
"""

from __future__ import annotations

import logging

from ted_analysis import ROOT_LOGGER_NAME
from ted_analysis.config import TEDAnalysisConfig

logger = logging.getLogger(ROOT_LOGGER_NAME)


def main(config: TEDAnalysisConfig | None = None) -> None:
    """Run the report stage.

    Args:
        config: Pipeline configuration.  Falls back to ``TEDAnalysisConfig()``
            defaults when ``None``.

    Raises:
        NotImplementedError: This module is a stub — override it with
            project-specific reporting logic.
    """
    cfg = config or TEDAnalysisConfig()
    msg = (
        f"report.py is a stub.  Implement:\n"
        f"  1. Read analysis results from {cfg.results_dir / cfg.analysis_results_filename}\n"
        f"  2. Read figure files from {cfg.figures_dir}\n"
        f"  3. Compile summary statistics and manuscript\n"
        f"  4. See AGENTS-report.md for details"
    )
    logger.error(msg)
    raise NotImplementedError(msg)


if __name__ == "__main__":
    main()
