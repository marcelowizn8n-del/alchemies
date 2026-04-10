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
        job = self.jobs.get(job_id)
        if not job:
            return None
        self._sync_job(job)
        return job

    def get_generation(self, generation_id: str) -> Optional[GenerationRecord]:
        generation = self.generations.get(generation_id)
        if not generation:
            return None

        job = next((item for item in self.jobs.values() if item.generation_id == generation_id), None)
        if job:
            self._sync_job(job)
        return generation

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

    def _sync_job(self, job: JobRecord) -> None:
        if job.status in {JobStatus.succeeded, JobStatus.failed}:
            return

        generation = self.generations[job.generation_id]
        now = utcnow()
        elapsed = (now - job.created_at).total_seconds()
        target_seconds = 5.0 if job.kind == GenerationKind.image else 7.5

        if elapsed < 1.2:
            job.status = JobStatus.queued
            job.progress = max(6, min(18, int(elapsed * 10)))
            job.message = "queued for orchestration dispatch"
            generation.status = JobStatus.queued
        elif elapsed < target_seconds:
            progress_ratio = (elapsed - 1.2) / (target_seconds - 1.2)
            job.status = JobStatus.processing
            job.progress = max(20, min(96, 20 + int(progress_ratio * 72)))
            job.message = self._processing_message(generation)
            generation.status = JobStatus.processing
        else:
            job.status = JobStatus.succeeded
            job.progress = 100
            job.message = "mock worker completed successfully"
            generation.status = JobStatus.succeeded
            generation.artifacts = self._build_artifacts(generation)
            generation.output_urls = [artifact.download_url for artifact in generation.artifacts if artifact.download_url]

        job.updated_at = now
        generation.updated_at = now

    def _processing_message(self, generation: GenerationRecord) -> str:
        if generation.kind == GenerationKind.image:
            if generation.request.get("reference_assets"):
                return "conditioning reference-guided image job"
            return "running text-to-image diffusion pass"
        return "assembling temporal video frames"

    def _build_artifacts(self, generation: GenerationRecord) -> list[ArtifactRecord]:
        extension = "png" if generation.kind == GenerationKind.image else "mp4"
        primary = ArtifactRecord(
            filename=f"{generation.id}.{extension}",
            media_type="image/png" if generation.kind == GenerationKind.image else "video/mp4",
        )
        metadata = ArtifactRecord(
            filename=f"{generation.id}.json",
            media_type="application/json",
            download_url=f"{generation.id}.json",
        )
        return [primary, metadata]


store = MemoryStore()
