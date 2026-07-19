"""
Image service.

Handles everything related to validating, storing, and locating uploaded
product images. Contains no AI-related logic.
"""

from __future__ import annotations

import uuid
from io import BytesIO
from pathlib import Path
from typing import Tuple

from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

from app.core.config import Settings, get_settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class ImageService:
    """Validates and persists uploaded product images."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()

    async def save_upload(self, file: UploadFile) -> Tuple[str, str, Path]:
        """
        Validate and persist an uploaded image file.

        Args:
            file: The incoming multipart file from FastAPI.

        Returns:
            A tuple of (image_id, stored_filename, absolute_path).

        Raises:
            HTTPException: If the file is missing, oversized, an
                unsupported format, or fails Pillow validation.
        """
        logger.info("Upload started | original_filename=%s", file.filename)

        raw_bytes = await file.read()
        self._validate_size(raw_bytes)

        image_format = self._validate_image(raw_bytes)

        image_id = str(uuid.uuid4())
        extension = self._extension_for_format(image_format)
        stored_filename = f"{image_id}{extension}"
        destination = self._settings.upload_dir / stored_filename

        destination.write_bytes(raw_bytes)

        logger.info(
            "Upload completed | image_id=%s | filename=%s | size_bytes=%d",
            image_id,
            stored_filename,
            len(raw_bytes),
        )

        return image_id, stored_filename, destination

    def resolve_image_path(self, image_id: str) -> Path:
        """
        Locate a previously uploaded image on disk by its UUID.

        Args:
            image_id: UUID assigned during upload.

        Returns:
            Absolute path to the stored image.

        Raises:
            HTTPException: If no matching file exists.
        """
        matches = list(self._settings.upload_dir.glob(f"{image_id}.*"))
        if not matches:
            logger.error("Image not found | image_id=%s", image_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No uploaded image found for image_id '{image_id}'",
            )
        return matches[0]

    def _validate_size(self, raw_bytes: bytes) -> None:
        if len(raw_bytes) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty.",
            )
        if len(raw_bytes) > self._settings.max_image_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=(
                    f"Uploaded file exceeds the maximum allowed size of "
                    f"{self._settings.max_image_size} bytes."
                ),
            )

    def _validate_image(self, raw_bytes: bytes) -> str:
        """
        Validate that the bytes represent a supported, non-corrupted image.

        Returns:
            The uppercase image format (e.g. 'PNG', 'JPEG', 'WEBP').
        """
        try:
            with Image.open(BytesIO(raw_bytes)) as image:
                image.verify()
            # Re-open after verify(), since verify() leaves the file unusable.
            with Image.open(BytesIO(raw_bytes)) as image:
                image_format = (image.format or "").upper()
        except UnidentifiedImageError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is not a valid or is a corrupted image.",
            ) from exc
        except Exception as exc:  # noqa: BLE001 - convert any Pillow failure to a 400
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file could not be processed as an image.",
            ) from exc

        if image_format not in self._settings.allowed_image_formats:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Unsupported image format '{image_format}'. "
                    f"Allowed formats: {', '.join(self._settings.allowed_image_formats)}."
                ),
            )

        return image_format

    @staticmethod
    def _extension_for_format(image_format: str) -> str:
        mapping = {"PNG": ".png", "JPEG": ".jpg", "WEBP": ".webp"}
        return mapping.get(image_format, ".img")
