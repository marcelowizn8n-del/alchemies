from fastapi import APIRouter, HTTPException

from .schemas import GenerationAcceptedResponse, ImageGenerationRequest, JobRecord, VideoGenerationRequest
from .store import store

router = APIRouter(prefix="/v1")


@router.get("/models")
def list_models():
    return {"items": store.list_models()}


@router.post("/generations/image", response_model=GenerationAcceptedResponse, status_code=202)
def create_image_generation(payload: ImageGenerationRequest):
    return store.create_image_generation(payload)


@router.post("/generations/video", response_model=GenerationAcceptedResponse, status_code=202)
def create_video_generation(payload: VideoGenerationRequest):
    return store.create_video_generation(payload)


@router.get("/jobs/{job_id}", response_model=JobRecord)
def get_job(job_id: str):
    job = store.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job_not_found")
    return job


@router.post("/jobs/{job_id}/mock-complete", response_model=JobRecord)
def mock_complete_job(job_id: str):
    job = store.mock_complete(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job_not_found")
    return job


@router.get("/generations/{generation_id}")
def get_generation(generation_id: str):
    generation = store.get_generation(generation_id)
    if not generation:
        raise HTTPException(status_code=404, detail="generation_not_found")
    return generation
