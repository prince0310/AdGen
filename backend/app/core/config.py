"""
Application configuration.

All runtime configuration is sourced from environment variables (optionally
loaded from a local .env file). Centralizing configuration here means no
other module ever needs to call `os.environ` directly.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Typed, centralized application settings.
    """

    def __init__(self) -> None:
        # ------------------------------------------------------------------
        # Application
        # ------------------------------------------------------------------
        self.app_name: str = os.getenv("APP_NAME", "AI Product Scene Generator")
        self.app_host: str = os.getenv("APP_HOST", "0.0.0.0")
        self.app_port: int = int(os.getenv("APP_PORT", "8000"))

        # ------------------------------------------------------------------
        # Gemini
        # ------------------------------------------------------------------
        self.gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
        self.gemini_model: str = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash",
        )

        # ------------------------------------------------------------------
        # OpenAI
        # ------------------------------------------------------------------
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
        self.openai_image_model: str = os.getenv(
            "OPENAI_IMAGE_MODEL",
            "gpt-image-1",
        )
        self.hf_api_key: str = os.getenv("HF_API_KEY", "")
        self.flux_model: str = os.getenv(
            "FLUX_MODEL",
            "black-forest-labs/FLUX.1-Kontext-dev",
        )

        # ------------------------------------------------------------------
        # Flux
        # ------------------------------------------------------------------
        self.flux_api_key: str = os.getenv("FLUX_API_KEY", "")
        self.flux_base_url: str = os.getenv("FLUX_BASE_URL", "")
        self.flux_model: str = os.getenv(
            "FLUX_MODEL",
            "flux-kontext-pro",
        )

        # ------------------------------------------------------------------
        # Storage
        # ------------------------------------------------------------------
        self.upload_dir: Path = Path(
            os.getenv("UPLOAD_DIR", "uploads")
        ).resolve()

        self.generated_dir: Path = Path(
            os.getenv("GENERATED_DIR", "generated")
        ).resolve()

        self.metadata_dir: Path = Path(
            os.getenv("METADATA_DIR", "metadata")
        ).resolve()

        # ------------------------------------------------------------------
        # Upload Limits
        # ------------------------------------------------------------------
        self.max_image_size: int = int(
            os.getenv(
                "MAX_IMAGE_SIZE",
                str(10 * 1024 * 1024),
            )
        )

        # ------------------------------------------------------------------
        # Logging
        # ------------------------------------------------------------------
        self.log_level: str = os.getenv(
            "LOG_LEVEL",
            "INFO",
        ).upper()

        # ------------------------------------------------------------------
        # Supported Formats
        # ------------------------------------------------------------------
        self.allowed_image_formats: tuple[str, ...] = (
            "PNG",
            "JPEG",
            "WEBP",
        )

        self.allowed_content_types: tuple[str, ...] = (
            "image/png",
            "image/jpeg",
            "image/webp",
        )

        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Create storage directories if they do not exist."""

        for directory in (
            self.upload_dir,
            self.generated_dir,
            self.metadata_dir,
        ):
            directory.mkdir(
                parents=True,
                exist_ok=True,
            )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.
    """
    return Settings()


settings = get_settings()