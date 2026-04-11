from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:16]}"


class JobStatus(str, Enum):
    queued = "queued"
    processing = "processing"
    succeeded = "succeeded"
    failed = "failed"


class GenerationKind(str, Enum):
    image = "image"
    video = "video"


class ReferenceAsset(BaseModel):
    kind: str = Field(default="image")
    uri: str


class ArtifactRecord(BaseModel):
    filename: str
    media_type: str
    download_url: Optional[str] = None


class ImageGenerationRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = None
    model: str = Field(default="sd3.5-large")
    width: int = Field(default=1024, ge=256, le=2048)
    height: int = Field(default=1024, ge=256, le=2048)
    guidance_scale: float = Field(default=6.5, ge=1.0, le=20.0)
    num_inference_steps: int = Field(default=30, ge=1, le=100)
    reference_assets: list[ReferenceAsset] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class VideoGenerationRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = None
    model: str = Field(default="wan2.1-t2v-1.3b")
    duration_seconds: int = Field(default=5, ge=1, le=12)
    aspect_ratio: str = Field(default="16:9")
    fps: int = Field(default=16, ge=8, le=30)
    reference_assets: list[ReferenceAsset] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class GenerationRecord(BaseModel):
    id: str
    kind: GenerationKind
    status: JobStatus
    model: str
    prompt: str
    artifacts: list[ArtifactRecord] = Field(default_factory=list)
    output_urls: list[str] = Field(default_factory=list)
    request: dict[str, Any]
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class JobRecord(BaseModel):
    id: str
    generation_id: str
    kind: GenerationKind
    status: JobStatus
    progress: int = Field(default=0, ge=0, le=100)
    message: str = Field(default="queued")
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class GenerationAcceptedResponse(BaseModel):
    generation: GenerationRecord
    job: JobRecord


class ModelDescriptor(BaseModel):
    id: str
    kind: GenerationKind
    provider: str
    placement: str
    status: str
    notes: str


class ImageWorkerRequest(BaseModel):
    generation_id: str
    model: str
    prompt: str
    request: dict[str, Any]


class ImageWorkerResponse(BaseModel):
    generation_id: str
    engine: str
    message: str
    artifacts: list[ArtifactRecord] = Field(default_factory=list)
