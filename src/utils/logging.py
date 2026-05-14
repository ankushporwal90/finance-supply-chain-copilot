"""Logging setup for consistent debugging across modules."""

import logging

from src.utils.config import get_settings


def get_logger(name: str) -> logging.Logger:
    """Return a module-level logger with a shared format."""

    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    return logging.getLogger(name)
