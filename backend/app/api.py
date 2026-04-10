from fastapi import APIRouter, BackgroundTasks, HTTPException

from .schemas import GenerationAcceptedResponse, ImageGenerationRequest, JobRecord, VideoGenerationRequest
from .processing import processor
from .store import store

router = APIRouter(prefix="/v1")


@router.get("/models")
def list_models():
    return {"items": store.list_models()}


@router.post("/generations/image", response_model=GenerationAcceptedResponse, status_code=202)
def create_image_generation(payload: ImageGenerationRequest, background_tasks: BackgroundTasks):
    accepted = store.create_image_generation(payload)
    background_tasks.add_task(processor.process_job, accepted.job.id)
    return accepted


@router.post("/generations/video", response_model=GenerationAcceptedResponse, status_code=202)
def create_video_generation(payload: VideoGenerationRequest, background_tasks: BackgroundTasks):
    accepted = store.create_video_generation(payload)
    background_tasks.add_task(processor.process_job, accepted.job.id)
    return accepted


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
