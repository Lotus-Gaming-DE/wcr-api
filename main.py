"""Application entry point for the WCR Data API."""

from __future__ import annotations

from contextlib import asynccontextmanager
import logging
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from wcr_api.api import router
from wcr_api.loaders import DataLoadError
from wcr_api.logging import configure_logging, get_logger
from wcr_api.middleware import LoggingMiddleware

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Configure logging and load data once on startup."""
    level = os.getenv("LOG_LEVEL", "INFO")
    configure_logging(logging.getLevelName(level.upper()))
    from wcr_api.loaders import get_data_loader

    logger = get_logger()
    logger.info("startup", message="Loading unit data")
    get_data_loader()
    yield


app = FastAPI(title="WCR Data API", lifespan=lifespan)
app.add_middleware(LoggingMiddleware)
app.include_router(router)


@app.exception_handler(DataLoadError)
async def dataloader_error_handler(
    request: Request, exc: DataLoadError
) -> JSONResponse:
    """Convert :class:`DataLoadError` into a generic ``500`` response.

    Parameters
    ----------
    request:
        Incoming request that triggered the error.
    exc:
        The raised :class:`DataLoadError` instance.

    Returns
    -------
    JSONResponse
        Response with a generic error payload.
    """
    logger.error("data_load_failed", error=str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": "Interner Serverfehler"},
    )
