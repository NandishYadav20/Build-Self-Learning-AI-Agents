"""Logging configuration for AI Agents"""

import logging
import sys
from typing import Optional
from datetime import datetime


def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Setup logger with both file and console handlers

    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))

    # File handler
    log_dir = "logs"
    import os
    os.makedirs(log_dir, exist_ok=True)

    log_file = f"{log_dir}/agent_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, level.upper()))

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Create root logger
logger = setup_logger("ai_agents")
