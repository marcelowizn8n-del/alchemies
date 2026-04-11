from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

from .config import settings
from .schemas import ArtifactRecord


class PlaceholderArtifactFactory:
    def __init__(self) -> None:
        settings.artifacts_path.mkdir(parents=True, exist_ok=True)

    def create_image_bundle(self, generation_id: str, prompt: str, request: dict) -> list[ArtifactRecord]:
        width = int(request.get("width", 1024))
        height = int(request.get("height", 1024))
        image_path = settings.artifacts_path / f"{generation_id}.png"

        image = Image.new("RGB", (width, height), "#09090f")
        draw = ImageDraw.Draw(image)

        for index, color in enumerate(["#2f1a54", "#602f9a", "#47c4ff", "#ff5fd2"]):
            inset = 36 + index * 28
            draw.rounded_rectangle(
                (inset, inset, width - inset, height - inset),
                radius=max(24, 64 - index * 8),
                outline=color,
                width=6,
            )

        orb_bounds = (width * 0.22, height * 0.14, width * 0.78, height * 0.70)
        draw.ellipse(orb_bounds, fill="#10172d", outline="#89d9ff", width=8)
        draw.ellipse(
            (width * 0.34, height * 0.24, width * 0.66, height * 0.56),
            fill="#190f2e",
            outline="#ff6fe5",
            width=10,
        )
        draw.ellipse(
            (width * 0.42, height * 0.30, width * 0.58, height * 0.46),
            fill="#1f0d2b",
            outline="#c47eff",
            width=8,
        )

        lines = wrap_text(prompt, 34)
        text_y = int(height * 0.76)
        draw.text((54, text_y), "DEVELOPMENT PLACEHOLDER", fill="#47c4ff")

        for index, line in enumerate(lines[:4]):
            draw.text((54, text_y + 34 + index * 28), line, fill="#ffffff")

        image.save(image_path)
        manifest_path = self._write_manifest(generation_id, request, image_path, engine="placeholder-image-worker")

        return [
            ArtifactRecord(
                filename=image_path.name,
                media_type="image/png",
                download_url=f"/artifacts/{image_path.name}",
            ),
            ArtifactRecord(
                filename=manifest_path.name,
                media_type="application/json",
                download_url=f"/artifacts/{manifest_path.name}",
            ),
        ]

    def create_video_bundle(self, generation_id: str, prompt: str, request: dict) -> list[ArtifactRecord]:
        width, height = aspect_to_dimensions(request.get("aspect_ratio", "16:9"))
        frame_count = max(10, int(request.get("duration_seconds", 5)) * 4)
        gif_path = settings.artifacts_path / f"{generation_id}.gif"

        frames = []
        for index in range(frame_count):
            frame = Image.new("RGB", (width, height), "#09090f")
            draw = ImageDraw.Draw(frame)
            draw.rectangle((0, 0, width, height), fill="#09090f")

            for stripe, color in enumerate(["#20103c", "#602f9a", "#47c4ff"]):
                top = 28 + stripe * 28
                draw.rounded_rectangle((32, top, width - 32, top + 12), radius=8, fill=color)

            radius = min(width, height) * 0.14
            center_x = width * (0.2 + 0.6 * (index / max(frame_count - 1, 1)))
            center_y = height * (0.5 + 0.12 * math.sin(index / 2))
            draw.ellipse(
                (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
                fill="#ff5fd2",
                outline="#ffffff",
                width=5,
            )
            draw.text((36, height - 90), "DEVELOPMENT VIDEO PLACEHOLDER", fill="#47c4ff")
            draw.text((36, height - 58), prompt[:40], fill="#ffffff")
            frames.append(frame)

        frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=160, loop=0)
        manifest_path = self._write_manifest(generation_id, request, gif_path, engine="placeholder-video-inline")

        return [
            ArtifactRecord(
                filename=gif_path.name,
                media_type="image/gif",
                download_url=f"/artifacts/{gif_path.name}",
            ),
            ArtifactRecord(
                filename=manifest_path.name,
                media_type="application/json",
                download_url=f"/artifacts/{manifest_path.name}",
            ),
        ]

    def _write_manifest(self, generation_id: str, request: dict, primary_artifact_path: Path, *, engine: str) -> Path:
        manifest_path = settings.artifacts_path / f"{generation_id}.json"
        manifest = {
            "generation_id": generation_id,
            "engine": engine,
            "primary_artifact": primary_artifact_path.name,
            "request": request,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))
        return manifest_path


def aspect_to_dimensions(aspect_ratio: str) -> tuple[int, int]:
    if aspect_ratio == "9:16":
        return 540, 960
    if aspect_ratio == "1:1":
        return 768, 768
    return 960, 540


def wrap_text(value: str, chunk_size: int) -> list[str]:
    words = value.split()
    if not words:
        return [""]

    lines: list[str] = []
    current: list[str] = []

    for word in words:
        candidate = " ".join([*current, word]).strip()
        if len(candidate) <= chunk_size:
            current.append(word)
            continue
        lines.append(" ".join(current))
        current = [word]

    if current:
        lines.append(" ".join(current))

    return lines


placeholder_artifacts = PlaceholderArtifactFactory()
