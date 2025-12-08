"""Logging configuration for Xyber Chatbot."""

import logging
import logging.handlers


def setup_logger(name: str) -> logging.Logger:
    """Set up a basic console logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
