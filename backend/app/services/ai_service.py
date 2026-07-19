"""
AI service.

Wraps the AIProvider to add business logic: metadata caching to disk so the
same image is never re-analyzed, and translation between the provider layer
and the API's Pydantic schemas.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

from fastapi import HTTPException, status

from app.core.config import Settings, get_settings
from app.core.logger import get_logger
from app.models.schemas import ProductMetadata
from app.providers.base_provider import AIProvider

logger = get_logger(__name__)


class AIService:
    """Coordinates product analysis and prompt generation via an AIProvider."""

    def __init__(
        self,
        provider: AIProvider,
        settings: Settings | None = None,
    ) -> None:
        self._provider = provider
        self._settings = settings or get_settings()

    async def get_or_create_metadata(
        self,
        image_id: str,
        image_path: Path,
        description: str | None = None,
    ) -> ProductMetadata:
        """
        Return cached metadata if available.
        Otherwise analyze the product and cache the metadata.

        Args:
            image_id: Uploaded image id.
            image_path: Absolute path of uploaded image.
            description: User supplied description (required only for first analysis).

        Returns:
            ProductMetadata
        """

        # Return cached metadata if available
        cached = self._load_cached_metadata(image_id)
        if cached is not None:
            logger.info("Metadata loaded from cache | image_id=%s", image_id)
            return cached

        # No cache found
        if description is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product description is required for first-time analysis.",
            )

        logger.info("Metadata cache miss | analyzing product | image_id=%s", image_id)

        metadata = await self._provider.analyze_product(
            image_path=image_path,
            description=description,
        )

        self._cache_metadata(image_id, metadata)

        logger.info("Metadata cached | image_id=%s", image_id)

        return metadata

    async def generate_prompts(
        self,
        metadata: ProductMetadata,
        scenarios: List[str],
    ) -> List[str]:
        logger.info(
            "Prompt generation started | scenario_count=%d",
            len(scenarios),
        )

        return await self._provider.generate_prompts(
            metadata,
            scenarios,
        )

    def _metadata_file(self, image_id: str) -> Path:
        return self._settings.metadata_dir / f"{image_id}.json"

    def _load_cached_metadata(
        self,
        image_id: str,
    ) -> ProductMetadata | None:

        metadata_path = self._metadata_file(image_id)

        if not metadata_path.exists():
            return None

        try:
            raw = json.loads(metadata_path.read_text(encoding="utf-8"))
            return ProductMetadata(**raw)

        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            logger.error(
                "Failed to parse cached metadata | image_id=%s | error=%s",
                image_id,
                exc,
            )
            return None

    def _cache_metadata(
        self,
        image_id: str,
        metadata: ProductMetadata,
    ) -> None:

        metadata_path = self._metadata_file(image_id)

        try:
            metadata_path.write_text(
                metadata.model_dump_json(indent=2),
                encoding="utf-8",
            )

        except OSError as exc:
            logger.error(
                "Failed to write metadata cache | image_id=%s | error=%s",
                image_id,
                exc,
            )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to persist product metadata.",
            ) from exc