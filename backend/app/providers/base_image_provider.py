from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class ImageProvider(ABC):
    """
    Base interface for image generation providers.

    Implementations:
    - MockImageProvider
    - FluxProvider (future)
    """

    @abstractmethod
    async def generate_image(
        self,
        image_path: Path,
        prompts: list[str],
    ) -> list[Path]:
        """
        Generate one image for each prompt.

        Args:
            image_path: Uploaded reference product image.
            prompts: Generated FLUX prompts.

        Returns:
            List of generated image paths.
        """
        ...