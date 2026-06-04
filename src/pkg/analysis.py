"""Statistical modelling — fit model, bootstrap, sensitivity analysis.

See ``AGENTS-analysis.md`` for the full specification.
"""

from __future__ import annotations

import logging

from pkg import ROOT_LOGGER_NAME
from pkg.config import ProjectConfig

logger = logging.getLogger(ROOT_LOGGER_NAME)


def main(config: ProjectConfig | None = None) -> None:
    """Run the analysis stage.

    Args:
        config: Pipeline configuration.  Falls back to ``ProjectConfig()``
            defaults when ``None``.

    Raises:
        NotImplementedError: This module is a stub — override it with
            project-specific statistical modelling logic.
    """
    cfg = config or ProjectConfig()
    msg = (
        f"analysis.py is a stub.  Implement:\n"
        f"  1. Read processed data from {cfg.processed_dir / cfg.processed_data_filename}\n"
        f"  2. Fit statistical model (n_bootstrap={cfg.n_bootstrap}, "
        f"ci_level={cfg.bootstrap_ci_level})\n"
        f"  3. Run sensitivity variants\n"
        f"  4. Write results to {cfg.results_dir / cfg.analysis_results_filename}\n"
        f"  5. See AGENTS-analysis.md for details"
    )
    logger.error(msg)
    raise NotImplementedError(msg)


if __name__ == "__main__":
    main()
