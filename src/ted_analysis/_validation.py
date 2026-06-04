"""Private validation module — bootstrap resampling + Spearman rank stability.

See ``AGENTS-analysis.md`` for the full specification.
"""

from __future__ import annotations

import logging

from ted_analysis import ROOT_LOGGER_NAME
from ted_analysis.config import TEDAnalysisConfig

logger = logging.getLogger(ROOT_LOGGER_NAME)


def main(config: TEDAnalysisConfig | None = None) -> None:
    """Run the validation / sensitivity analysis.

    Args:
        config: Pipeline configuration.  Falls back to ``TEDAnalysisConfig()``
            defaults when ``None``.

    Raises:
        NotImplementedError: This module is a stub — override it with
            project-specific validation logic.
    """
    cfg = config or TEDAnalysisConfig()
    msg = (
        f"_validation.py is a stub.  Implement:\n"
        f"  1. Bootstrap resampling for confidence intervals "
        f"(n={cfg.n_bootstrap}, ci={cfg.bootstrap_ci_level})\n"
        f"  2. Spearman rank stability on random subsamples "
        f"{cfg.subsample_fractions}\n"
        f"  3. See AGENTS-analysis.md for details"
    )
    logger.error(msg)
    raise NotImplementedError(msg)


if __name__ == "__main__":
    main()
