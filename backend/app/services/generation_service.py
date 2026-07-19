"""
Generation service.

Orchestrates the end-to-end scene generation flow: load/derive product
metadata, generate prompts, generate images, and shape the response. This
is the only service that routes should call for POST /generate.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from app.core.config import Settings, get_settings
from app.core.logger import get_logger
from app.models.schemas import GeneratedImage, GenerateResponse
# from app.providers.base_provider import AIProvider
from app.providers.base_image_provider import ImageProvider
from app.services.ai_service import AIService
from app.services.image_service import ImageService

logger = get_logger(__name__)


class GenerationService:
    """Coordinates ImageService + AIService to fulfil a generation request."""

    def __init__(
        self,
        image_provider: ImageProvider,
        image_service: ImageService,
        ai_service: AIService,
        settings: Settings | None = None,
    ) -> None:
        self._image_provider = image_provider
        self._image_service = image_service
        self._ai_service = ai_service
        self._settings = settings or get_settings()

    async def generate_scenes(
        self,
        image_id: str,
        scenarios: List[str],
    ) -> GenerateResponse:
        """
        Run the full generation pipeline for an uploaded product image.
        """

        # Resolve uploaded image path
        image_path = self._image_service.resolve_image_path(image_id)

        # Load cached metadata (created during /analyze)
        metadata = await self._ai_service.get_or_create_metadata(
            image_id=image_id,
            image_path=image_path,
        )

        # Generate prompts
        prompts = await self._ai_service.generate_prompts(
            metadata=metadata,
            scenarios=scenarios,
        )
        print("\n===== Generated Prompts =====")
        for i, prompt in enumerate(prompts, start=1):
            print(f"\nPrompt {i}:\n{prompt}")

        logger.info(
            "Image generation started | image_id=%s | count=%d",
            image_id,
            len(prompts),
        )

        # Generate images
        generated_paths = await self._image_provider.generate_images(
            image_path=image_path,
            prompts=prompts,
        )

        images = [
            GeneratedImage(
                scenario=scenario,
                image_url=self._to_public_url(path),
            )
            for scenario, path in zip(scenarios, generated_paths)
        ]

        logger.info(
            "Generation completed | image_id=%s | images=%d",
            image_id,
            len(images),
        )

        return GenerateResponse(
            image_id=image_id,
            images=images,
        )

    def _to_public_url(self, path: Path) -> str:
        """Convert an absolute generated-file path into a public URL."""
        return f"/generated/{path.name}"