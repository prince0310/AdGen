"""
Centralized logging configuration.

Every layer of the application (routes, services, providers) retrieves its
logger via `get_logger(__name__)` so log output is consistently formatted
and consistently leveled, and so the logging backend can be swapped out
(e.g. for structured JSON logging) in a single place.
"""

from __future__ import annotations

import logging
import sys

from app.core.config import get_settings

_CONFIGURED = False


def _configure_root_logger() -> None:
    """Configure the root logger exactly once per process."""
    global _CONFIGURED
    if _CONFIGURED:
        return

    settings = get_settings()

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(settings.log_level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """
    Return a module-scoped logger.

    Args:
        name: Typically `__name__` of the calling module.

    Returns:
        A configured `logging.Logger` instance.
    """
    _configure_root_logger()
    return logging.getLogger(name)
