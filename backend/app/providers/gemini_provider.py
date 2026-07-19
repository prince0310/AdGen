from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import List

from google import genai
from google.genai import types

from app.core.config import get_settings
from app.core.logger import get_logger
from app.models.schemas import ProductMetadata

logger = get_logger(__name__)


class GeminiProvider:
    """
    Gemini provider responsible for:

    - Product analysis
    - Prompt generation

    Image generation is intentionally NOT handled here.
    """

    def __init__(self) -> None:
        settings = get_settings()

        self._model = settings.gemini_model
        self._client = genai.Client(
            api_key=settings.gemini_api_key
        )

    # ----------------------------------------------------------
    # Product Analysis
    # ----------------------------------------------------------

    async def analyze_product(
        self,
        image_path: Path,
        description: str,
    ) -> ProductMetadata:

        logger.info("Analyzing product with Gemini")

        image_bytes = image_path.read_bytes()

        prompt = f"""
You are an expert product analyst.

Analyze the uploaded product image together with the user description.

User Description:
{description}

Return ONLY valid JSON.

Required schema:

{{
    "product_name": "...",
    "category": "...",
    "description": "...",
    "packaging": "...",
    "primary_colors": ["...", "..."],
    "brand_style": "..."
}}

Do not include markdown.
Do not include explanations.
"""

        response = await asyncio.to_thread(
            self._client.models.generate_content,
            model=self._model,
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg",
                ),
            ],
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        data = json.loads(text)

        metadata = ProductMetadata(**data)

        logger.info("Gemini product analysis complete")

        return metadata

    # ----------------------------------------------------------
    # Prompt Generation
    # ----------------------------------------------------------

    async def generate_prompts(
        self,
        metadata: ProductMetadata,
        scenarios: List[str],
    ) -> List[str]:

        logger.info("Generating prompts with Gemini")

        prompt = f"""
            You are an expert prompt engineer for FLUX Kontext.

            The uploaded product image will be supplied separately as the reference image.
            Use the provided reference product image exactly as supplied.

            Do not modify the product itself.

            Only change the surrounding environment.

            The product has already been analyzed.

            Product Information

            Name:
            {metadata.product_name}

            Category:
            {metadata.category}

            Description:
            {metadata.description}

            Packaging:
            {metadata.packaging}

            Brand Style:
            {metadata.brand_style}

            Primary Colors:
            {", ".join(metadata.primary_colors)}

            Generate ONE FLUX Kontext prompt for EACH of these scenarios:

            {chr(10).join(f"- {scenario}" for scenario in scenarios)}

            IMPORTANT RULES

            The product image is provided separately.

            Do NOT redesign the product.

            Do NOT describe the bottle shape in detail.

            Do NOT recreate the label.

            Do NOT recreate the logo.

            Assume the product already exists exactly as desired.

            Your job is ONLY to describe:

            - environment
            - composition
            - camera angle
            - lighting
            - shadows
            - reflections
            - atmosphere
            - styling
            - props
            - background
            - depth of field

            Every prompt MUST explicitly instruct FLUX Kontext to preserve:

            - logo
            - branding
            - packaging
            - bottle
            - cap
            - colors
            - proportions
            - text
            - label placement

            The output should feel like instructions for an image editing model rather than an image generation model.

            Each prompt should , commercial-quality, and suitable for luxury product advertising.

            Return ONLY valid JSON.

            Format:

            {{
                "prompts": [
                    "...",
                    "...",
                    "..."
                ]
            }}
            """

        response = await asyncio.to_thread(
            self._client.models.generate_content,
            model=self._model,
            contents=prompt,
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        data = json.loads(text)

        logger.info("Generated %d prompts", len(data["prompts"]))

        return data["prompts"]