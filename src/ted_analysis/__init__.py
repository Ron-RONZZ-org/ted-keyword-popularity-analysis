"""TED Keyword Popularity Analysis.

Investigates which keywords are most globally prominent across all public
TED Talks, using Term Frequency weighted by view count.

Pipeline stages:
    acquire → preprocess → analyze → visualize → report
"""

from __future__ import annotations

import logging
import logging.handlers
import sys
from pathlib import Path

from ted_analysis.config import TEDAnalysisConfig

__version__ = "0.1.0"

_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
# Derived from the package name — survives package rename automatically.
ROOT_LOGGER_NAME: str = __name__

__all__ = [
    "ROOT_LOGGER_NAME",
    "setup_logging",
    "TEDAnalysisConfig",
]


def setup_logging(
    config: TEDAnalysisConfig | str | Path | None = None,
) -> None:
    """Configure the project-wide logger.

    Sets up dual-output logging: DEBUG and above to a rotating log file
    under the configured logs directory, INFO and above to stdout.
    Idempotent — safe to call multiple times.

    Args:
        config: Pipeline configuration, a path string, or ``None``.
            When a ``TEDAnalysisConfig`` instance is passed, its
            ``logs_dir`` field is used.  When a ``str`` or ``Path`` is
            passed it is treated as the log directory directly.
            Falls back to ``TEDAnalysisConfig().logs_dir`` when ``None``.

    Raises:
        OSError: If the log directory cannot be created.
    """
    root_logger = logging.getLogger(ROOT_LOGGER_NAME)

    # Avoid duplicate handler registration.
    if root_logger.handlers:
        return

    root_logger.setLevel(logging.DEBUG)

    if isinstance(config, (str, Path)):
        logs_path = Path(config)
    else:
        cfg = config or TEDAnalysisConfig()
        logs_path = Path(cfg.logs_dir)

    logs_path.mkdir(parents=True, exist_ok=True)

    file_handler = logging.handlers.RotatingFileHandler(
        logs_path / "pipeline.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=3,
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(_LOG_FORMAT))

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_LOG_FORMAT))

    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)
