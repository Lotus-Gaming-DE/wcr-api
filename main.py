"""Application entry point for the WCR Data API."""

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api import router
from app.loaders import DataLoadError

app = FastAPI(title="WCR Data API")
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
    logging.error("Data loading failed: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.on_event("startup")
def startup_event() -> None:
    """Configure logging and load data once on startup."""
    logging.basicConfig(level=logging.INFO)
    from app.loaders import get_data_loader

    logging.info("Loading unit data")
    get_data_loader()
