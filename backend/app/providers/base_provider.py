from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from app.models.schemas import ProductMetadata


class AIProvider(ABC):
    """Contract that all AI providers must fulfil."""

    @abstractmethod
    async def analyze_product(self,image_path: Path, description: str) -> ProductMetadata:
        """
        Analyze a product image and extract structured metadata.

        Args:
            image_path: Absolute path to the product image on disk.
            description: Description of the product.

        Returns:
            A `ProductMetadata` instance describing the product.
        """
        raise NotImplementedError

    @abstractmethod
    async def generate_prompts(
        self,
        metadata: ProductMetadata,
        scenarios: List[str],
    ) -> List[str]:
        """
        Generate one image-generation prompt per requested scenario.

        Args:
            metadata: Previously extracted product metadata.
            scenarios: List of scenario descriptions requested by the caller.

        Returns:
            A list of prompts, one per scenario, in the same order as
            `scenarios`.
        """
        raise NotImplementedError

    @abstractmethod
    async def generate_images(
        self,
        image_path: Path,
        prompts: List[str],
    ) -> List[Path]:
        """
        Generate one scene image per prompt.

        Args:
            image_path: Absolute path to the original product image, used
                as a reference so branding/packaging remains identical.
            prompts: List of prompts previously produced by
                `generate_prompts`.

        Returns:
            A list of absolute paths to the generated image files, in the
            same order as `prompts`.
        """
        raise NotImplementedError
