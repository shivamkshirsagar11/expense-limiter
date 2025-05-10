import logging
from logging.handlers import RotatingFileHandler
from core.config import settings
import os

def create_logger(name: str, log_dir=settings.LOGGING.base_dir, level=settings.LOGGING.level) -> logging.Logger:
    log_file = os.path.join(log_dir, f"{name}.log")

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # Avoid double logging

    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter("%(levelname)s|%(name)s|%(message)s")
        console_handler.setFormatter(console_formatter)

        # File handler with rotation
        file_handler = RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=5
        )
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            "%(asctime)s|%(name)s|%(levelname)s|%(message)s"
        )
        file_handler.setFormatter(file_formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

def log_debug_and_info(logger: logging.Logger, message: str):
    logger.info(message)
    logger.debug(message)