"""Logging utilities for the WCR Data API."""

from __future__ import annotations

import logging
import structlog


def configure_logging(level: int = logging.INFO) -> None:
    """Configure JSON structured logging for the application.

    Parameters
    ----------
    level:
        Minimum log level to emit. Defaults to :data:`logging.INFO`.
    """

    logging.basicConfig(format="%(message)s", level=level)
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
