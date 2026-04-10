from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .schemas import (
    GenerationAcceptedResponse,
    GenerationKind,
    GenerationRecord,
    ImageGenerationRequest,
    JobRecord,
    JobStatus,
    ModelDescriptor,
    VideoGenerationRequest,
    new_id,
    utcnow,
)


@dataclass
class MemoryStore:
    jobs: dict[str, JobRecord] = field(default_factory=dict)
    generations: dict[str, GenerationRecord] = field(default_factory=dict)

    def list_models(self) -> list[ModelDescriptor]:
        return [
            ModelDescriptor(
                id="sd3.5-large",
                kind=GenerationKind.image,
                provider="self-hosted",
                placement="gpu-worker:image",
                status="planned",
                notes="Recommended commercial image baseline for the first real worker.",
            ),
            ModelDescriptor(
                id="wan2.1-t2v-1.3b",
                kind=GenerationKind.video,
                provider="self-hosted",
                placement="gpu-worker:video",
                status="planned",
                notes="Recommended low-entry video baseline for the first real worker.",
            ),
        ]

    def create_image_generation(self, payload: ImageGenerationRequest) -> GenerationAcceptedResponse:
        return self._create_generation(
            kind=GenerationKind.image,
            model=payload.model,
            prompt=payload.prompt,
            request=payload.model_dump(mode="json"),
        )

    def create_video_generation(self, payload: VideoGenerationRequest) -> GenerationAcceptedResponse:
        return self._create_generation(
            kind=GenerationKind.video,
            model=payload.model,
            prompt=payload.prompt,
            request=payload.model_dump(mode="json"),
        )

    def _create_generation(
        self,
        *,
        kind: GenerationKind,
        model: str,
        prompt: str,
        request: dict[str, Any],
    ) -> GenerationAcceptedResponse:
        generation = GenerationRecord(
            id=new_id("gen"),
            kind=kind,
            status=JobStatus.queued,
            model=model,
            prompt=prompt,
            request=request,
        )
        job = JobRecord(
            id=new_id("job"),
            generation_id=generation.id,
            kind=kind,
            status=JobStatus.queued,
            progress=0,
            message="queued for worker dispatch",
        )
        self.generations[generation.id] = generation
        self.jobs[job.id] = job
        return GenerationAcceptedResponse(generation=generation, job=job)

    def get_job(self, job_id: str) -> JobRecord | None:
        return self.jobs.get(job_id)

    def get_generation(self, generation_id: str) -> GenerationRecord | None:
        return self.generations.get(generation_id)

    def mock_complete(self, job_id: str) -> JobRecord | None:
        job = self.jobs.get(job_id)
        if not job:
            return None

        generation = self.generations[job.generation_id]
        now = utcnow()

        job.status = JobStatus.succeeded
        job.progress = 100
        job.message = "mock output generated"
        job.updated_at = now

        generation.status = JobStatus.succeeded
        generation.output_urls = [
            f"/mock-output/{generation.id}.{ 'mp4' if generation.kind == GenerationKind.video else 'png' }"
        ]
        generation.updated_at = now
        return job


store = MemoryStore()
