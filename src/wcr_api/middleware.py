"""ASGI middleware components for the API."""

from __future__ import annotations

import time
from starlette.middleware.base import BaseHTTPMiddleware
from .logging import get_logger

logger = get_logger()


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log incoming HTTP requests and responses."""

    async def dispatch(self, request, call_next):
        """Log the request and response including the processing time."""
        # record the start time so we can log how long the request took
        start = time.perf_counter()
        logger.info("request", method=request.method, path=request.url.path)
        try:
            response = await call_next(request)
        except Exception:
            logger.error(
                "error",
                method=request.method,
                path=request.url.path,
                exc_info=True,
            )
            raise
        # convert runtime to milliseconds for readability in logs
        duration = (time.perf_counter() - start) * 1000
        logger.info(
            "response",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration, 2),
        )
        return response
