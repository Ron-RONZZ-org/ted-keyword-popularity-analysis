"""Statistical modelling — weighted TF, TF-IDF, temporal trends.

See ``AGENTS-analysis.md`` for the full specification.
"""

from __future__ import annotations

import logging

from ted_analysis import ROOT_LOGGER_NAME
from ted_analysis.config import TEDAnalysisConfig

logger = logging.getLogger(ROOT_LOGGER_NAME)


def main(config: TEDAnalysisConfig | None = None) -> None:
    """Run the analysis stage.

    Args:
        config: Pipeline configuration.  Falls back to ``TEDAnalysisConfig()``
            defaults when ``None``.

    Raises:
        NotImplementedError: This module is a stub — override it with
            project-specific statistical modelling logic.
    """
    cfg = config or TEDAnalysisConfig()
    msg = (
        f"analysis.py is a stub.  Implement:\n"
        f"  1. Read processed data from {cfg.processed_dir / cfg.processed_data_filename}\n"
        f"  2. Compute view-count-weighted term frequency scores\n"
        f"  3. Run bootstrap resampling (n={cfg.n_bootstrap}, "
        f"ci={cfg.bootstrap_ci_level})\n"
        f"  4. TF-IDF secondary analysis\n"
        f"  5. Temporal trend decomposition\n"
        f"  6. Write results to {cfg.results_dir / cfg.analysis_results_filename}\n"
        f"  7. See AGENTS-analysis.md for details"
    )
    logger.error(msg)
    raise NotImplementedError(msg)


if __name__ == "__main__":
    main()
