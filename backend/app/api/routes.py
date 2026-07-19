"""
API routes.

Routes contain NO business logic. Their only responsibilities are:
  - Parse/validate the incoming request (mostly handled by FastAPI/Pydantic).
  - Delegate to the appropriate service.
  - Translate service results/exceptions into HTTP responses.

Routes never talk to an AI provider directly.
"""

from __future__ import annotations

from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
import os
from app.core.logger import get_logger
from app.models.schemas import (
    AnalyzeRequest,
    GenerateRequest,
    GenerateResponse,
    ProductMetadata,
    UploadResponse,
)
from app.providers.base_provider import AIProvider
from app.providers.base_image_provider import ImageProvider
from app.providers.flux_image_provider import FluxImageProvider
# from app.providers.openai_provider import OpenAIProvider
from app.providers.gemini_provider import GeminiProvider
from app.services.ai_service import AIService
from app.services.generation_service import GenerationService
from app.services.image_service import ImageService

logger = get_logger(__name__)

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency providers
#
# Centralizing construction here means swapping OpenAIProvider for a future
# GeminiProvider/ClaudeProvider/DeepSeekProvider is a one-line change, and
# nothing in the routes or services layer needs to know.
# ---------------------------------------------------------------------------

@lru_cache
def get_ai_provider() -> AIProvider:
    """Return the process-wide AIProvider singleton."""
    return GeminiProvider()


@lru_cache
def get_image_provider() -> ImageProvider:
    """Return the process-wide ImageProvider singleton."""
    
    return FluxImageProvider()


def get_image_service() -> ImageService:
    """Return a new ImageService instance."""
    return ImageService()


def get_ai_service(provider: AIProvider = Depends(get_ai_provider)) -> AIService:
    """Return a new AIService instance bound to the active AIProvider."""
    return AIService(provider=provider)


def get_generation_service(
    image_provider: ImageProvider = Depends(get_image_provider),
    image_service: ImageService = Depends(get_image_service),
    ai_service: AIService = Depends(get_ai_service),
) -> GenerationService:

    return GenerationService(
        image_provider=image_provider,
        image_service=image_service,
        ai_service=ai_service,
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_image(
    file: UploadFile = File(...),
    image_service: ImageService = Depends(get_image_service),
) -> UploadResponse:
    """Upload a product image (PNG, JPEG, or WEBP)."""
    try:
        image_id, filename, path = await image_service.save_upload(file)
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001 - guarantee a consistent error envelope
        logger.exception("Unexpected error during upload")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while uploading the image.",
        ) from exc

    return UploadResponse(image_id=image_id, filename=filename, path=str(path))


@router.post("/analyze", response_model=ProductMetadata)
async def analyze_product(
    request: AnalyzeRequest,
    image_service: ImageService = Depends(get_image_service),
    ai_service: AIService = Depends(get_ai_service),
) -> ProductMetadata:
    """Analyze a previously uploaded product image, using cached metadata if available."""
    try:
        image_path = image_service.resolve_image_path(request.image_id)
        metadata = await ai_service.get_or_create_metadata(image_id=request.image_id,image_path=image_path,description=request.description)
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error during analysis | image_id=%s", request.image_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while analyzing the product image.",
        ) from exc

    return metadata


@router.post("/generate", response_model=GenerateResponse)
async def generate_scenes(
    request: GenerateRequest,
    generation_service: GenerationService = Depends(get_generation_service),
) -> GenerateResponse:
    """Generate product scene images for the given scenarios."""
    try:
        response = await generation_service.generate_scenes(
            image_id=request.image_id,
            scenarios=request.scenarios,
        )
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error during generation | image_id=%s", request.image_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while generating scene images.",
        ) from exc

    return response
