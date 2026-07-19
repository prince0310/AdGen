"""
Pydantic schemas shared across the API layer.

These models define the public contract of the API (request/response
bodies) as well as the internal data structures (e.g. `ProductMetadata`)
that are persisted to disk as JSON.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------------

class UploadResponse(BaseModel):
    """Response returned after a successful image upload."""

    image_id: str = Field(..., description="UUID assigned to the uploaded image")
    filename: str = Field(..., description="Stored filename on disk")
    path: str = Field(..., description="Relative path to the stored image")


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

class AnalyzeRequest(BaseModel):
    """Request body for triggering product analysis."""

    image_id: str = Field(..., description="UUID of a previously uploaded image")
    description: str = Field(..., description="Description of the product")


class ProductMetadata(BaseModel):
    """
    Structured description of a product, produced by the AI provider from
    the uploaded product image and cached to disk thereafter.
    """

    product_name: str
    category: str
    description: str
    packaging: str
    primary_colors: List[str]
    brand_style: str


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

class GenerateRequest(BaseModel):
    """Request body for triggering scene generation."""

    image_id: str = Field(..., description="UUID of a previously uploaded image")
    scenarios: List[str] = Field(
        ...,
        min_length=1,
        description="List of scenario descriptions, e.g. 'luxury marble countertop'",
    )


class GeneratedImage(BaseModel):
    """A single generated scene image."""

    scenario: str = Field(..., description="The scenario this image was generated for")
    image_url: str = Field(..., description="URL at which the generated image can be retrieved")


class GenerateResponse(BaseModel):
    """Response returned after scene generation completes."""

    image_id: str
    images: List[GeneratedImage]


# ---------------------------------------------------------------------------
# Generic / error responses
# ---------------------------------------------------------------------------

class ErrorResponse(BaseModel):
    """Consistent error envelope returned for all handled API errors."""

    error: str
    detail: Optional[str] = None
