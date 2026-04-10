from fastapi import FastAPI

from .api import router as api_router
from .config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "Own API foundation for Alchemies.PRO. This service is the orchestration layer for self-hosted image "
        "and video generation workers."
    ),
)


@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": settings.app_name, "env": settings.env}


@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "docs": "/docs",
        "openapi": "/openapi.json",
        "public_base_url": settings.public_base_url,
    }


app.include_router(api_router)
