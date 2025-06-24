"""Logging utilities for the WCR Data API."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import structlog


LOG_DIR = Path(__file__).resolve().parent.parent / "logs"


def configure_logging(level: int = logging.INFO) -> None:
    """Configure JSON structured logging for the application.

    Parameters
    ----------
    level:
        Minimum log level to emit. Defaults to :data:`logging.INFO`.
    """

    LOG_DIR.mkdir(exist_ok=True)
    log_file = LOG_DIR / "api.log"
    file_handler = RotatingFileHandler(
        log_file, maxBytes=1_000_000, backupCount=3
    )
    file_handler.setFormatter(logging.Formatter("%(message)s"))
    logging.basicConfig(
        handlers=[file_handler, logging.StreamHandler()],
        format="%(message)s",
        level=level,
    )
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger() -> structlog.BoundLogger:
    """Return the module-level structured logger."""

    return structlog.get_logger()
