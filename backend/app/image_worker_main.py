from fastapi import FastAPI

from .config import settings
from .image_worker import image_worker
from .schemas import ImageWorkerRequest, ImageWorkerResponse

app = FastAPI(
    title="Alchemies Image Worker",
    version="0.1.0",
    description="Private image worker for Alchemies.PRO. This service should stay private behind the public API.",
)


@app.get("/healthz")
def healthz():
    return {
        "status": "ok",
        "service": "Alchemies Image Worker",
        "env": settings.env,
        "image_engine": settings.image_engine,
    }


@app.post("/internal/generate", response_model=ImageWorkerResponse)
def generate_image(payload: ImageWorkerRequest):
    return image_worker.generate(payload)
