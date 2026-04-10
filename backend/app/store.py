from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .schemas import (
    ArtifactRecord,
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

    def get_job(self, job_id: str) -> Optional[JobRecord]:
        return self.jobs.get(job_id)

    def get_generation(self, generation_id: str) -> Optional[GenerationRecord]:
        return self.generations.get(generation_id)

    def mock_complete(self, job_id: str) -> Optional[JobRecord]:
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
        generation.artifacts = self._build_artifacts(generation)
        generation.output_urls = [artifact.download_url for artifact in generation.artifacts if artifact.download_url]
        generation.updated_at = now
        return job

    def mark_processing(self, job_id: str, message: str) -> JobRecord:
        job = self.jobs[job_id]
        generation = self.generations[job.generation_id]
        now = utcnow()

        job.status = JobStatus.processing
        job.progress = 38
        job.message = message
        job.updated_at = now

        generation.status = JobStatus.processing
        generation.updated_at = now
        return job

    def mark_succeeded(self, job_id: str, artifacts: list[ArtifactRecord], message: str) -> JobRecord:
        job = self.jobs[job_id]
        generation = self.generations[job.generation_id]
        now = utcnow()

        job.status = JobStatus.succeeded
        job.progress = 100
        job.message = message
        job.updated_at = now

        generation.status = JobStatus.succeeded
        generation.artifacts = artifacts
        generation.output_urls = [artifact.download_url for artifact in artifacts if artifact.download_url]
        generation.updated_at = now
        return job

    def mark_failed(self, job_id: str, message: str) -> JobRecord:
        job = self.jobs[job_id]
        generation = self.generations[job.generation_id]
        now = utcnow()

        job.status = JobStatus.failed
        job.progress = 100
        job.message = message
        job.updated_at = now

        generation.status = JobStatus.failed
        generation.updated_at = now
        return job


store = MemoryStore()
