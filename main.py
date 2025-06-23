from fastapi import FastAPI

from app.api import router

app = FastAPI(title="WCR Data API")
app.include_router(router)


@app.on_event("startup")
def startup_event():
    # Load data at startup
    from app.loaders import get_data_loader

    get_data_loader()
