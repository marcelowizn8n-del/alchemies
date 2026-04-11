from __future__ import annotations

import json
from urllib import error, request

from .artifacts import placeholder_artifacts
from .config import settings
from .schemas import ArtifactRecord, GenerationKind, ImageWorkerRequest, ImageWorkerResponse
from .store import store


class ImageWorkerClient:
    def generate(self, generation_id: str) -> ImageWorkerResponse:
        generation = store.get_generation(generation_id)
        if not generation:
            raise ValueError(f"generation {generation_id} was not found")
        if not settings.image_worker_url:
            raise RuntimeError("ALCHEMIES_IMAGE_WORKER_URL is not configured")

        payload = ImageWorkerRequest(
            generation_id=generation.id,
            model=generation.model,
            prompt=generation.prompt,
            request=generation.request,
        )
        body = json.dumps(payload.model_dump(mode="json")).encode("utf-8")
        endpoint = f"{settings.image_worker_url.rstrip('/')}/internal/generate"
        outgoing = request.Request(
            endpoint,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(outgoing, timeout=settings.image_worker_timeout_seconds) as response:
                response_body = response.read().decode("utf-8")
        except error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"image worker returned HTTP {exc.code}: {details}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"image worker unreachable: {exc.reason}") from exc

        return ImageWorkerResponse.model_validate_json(response_body)


class GenerationProcessor:
    def __init__(self) -> None:
        self.image_worker_client = ImageWorkerClient()

    def process_job(self, job_id: str) -> None:
        job = store.get_job(job_id)
        if not job:
            raise ValueError(f"job {job_id} was not found")

        generation = store.get_generation(job.generation_id)
        if not generation:
            raise ValueError(f"generation {job.generation_id} was not found")

        try:
            store.mark_processing(job.id, "worker accepted the queued generation")

            if generation.kind == GenerationKind.image:
                artifacts, message = self._process_image_generation(generation.id)
            else:
                artifacts, message = self._process_video_generation(generation.id)

            store.mark_succeeded(job.id, artifacts, message)
        except Exception as exc:
            store.mark_failed(job.id, f"worker failed: {exc}")

    def _process_image_generation(self, generation_id: str) -> tuple[list[ArtifactRecord], str]:
        if settings.image_worker_url:
            worker_result = self.image_worker_client.generate(generation_id)
            return worker_result.artifacts, worker_result.message

        if not settings.inline_worker_enabled:
            raise RuntimeError("image worker is disabled and no private image worker URL is configured")

        generation = store.get_generation(generation_id)
        if not generation:
            raise ValueError(f"generation {generation_id} was not found")

        artifacts = placeholder_artifacts.create_image_bundle(generation_id, generation.prompt, generation.request)
        return artifacts, "image artifact generated inline for development fallback"

    def _process_video_generation(self, generation_id: str) -> tuple[list[ArtifactRecord], str]:
        generation = store.get_generation(generation_id)
        if not generation:
            raise ValueError(f"generation {generation_id} was not found")
        if settings.video_engine != "placeholder":
            raise NotImplementedError("Only the placeholder video engine is wired in this stage")
        if not settings.inline_worker_enabled:
            raise RuntimeError("video processing is disabled until a dedicated video worker is connected")

        artifacts = placeholder_artifacts.create_video_bundle(generation_id, generation.prompt, generation.request)
        return artifacts, "video artifact generated inline for development fallback"


processor = GenerationProcessor()
