"""Research package.

Each project renames ``src/pkg/`` to ``src/<project_package>/`` and fills
in module stubs for each pipeline stage.

The logging setup below is generic — copy it verbatim to any new project.
"""

from __future__ import annotations

import logging
import logging.handlers
import sys
from pathlib import Path

__version__ = "0.1.0"

_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
# Derived from the package name — survives package rename automatically.
ROOT_LOGGER_NAME: str = __name__

__all__ = [
    "ROOT_LOGGER_NAME",
    "setup_logging",
]


def setup_logging(logs_dir: str | Path = "logs") -> None:
    """Configure the project-wide logger.

    Sets up dual-output logging: DEBUG and above to a rotating log file in
    *logs_dir*, INFO and above to stdout.  Idempotent — safe to call
    multiple times.

    Args:
        logs_dir: Path to the log directory (relative or absolute).
            Defaults to ``"logs"``.

    Raises:
        OSError: If the log directory cannot be created.
    """
    root_logger = logging.getLogger(ROOT_LOGGER_NAME)

    # Avoid duplicate handler registration.
    if root_logger.handlers:
        return

    root_logger.setLevel(logging.DEBUG)

    logs_path = Path(logs_dir)
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
