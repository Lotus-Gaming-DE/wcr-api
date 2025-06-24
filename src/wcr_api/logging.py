"""Logging utilities for the WCR Data API."""

from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
import structlog


def configure_logging(level: int | str | None = None) -> None:
    """Configure JSON structured logging for the application.

    Parameters
    ----------
    level:
        Minimum log level to emit. If ``None`` (default), the value is read
        from the ``LOG_LEVEL`` environment variable and falls back to
        :data:`logging.INFO`.
    """

    if level is None:
        env_level = os.getenv("LOG_LEVEL", "INFO")
        level = logging.getLevelName(env_level.upper())

    os.makedirs("logs", exist_ok=True)
    file_handler = RotatingFileHandler(
        "logs/api.log", maxBytes=1_048_576, backupCount=3
    )

    logging.basicConfig(
        format="%(message)s",
        level=level,
        handlers=[logging.StreamHandler(), file_handler],
        force=True,
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
