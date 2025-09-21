"""
Common utility functions for YouTube channel scripts.

This module contains helper functions that are commonly used
across different scripts in the project.
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging configuration for scripts.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
        log_format: Custom log format string
    
    Returns:
        Configured logger instance
    """
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        filename=log_file
    )
    
    return logging.getLogger(__name__)


def get_project_root() -> Path:
    """
    Get the project root directory.
    
    Returns:
        Path object pointing to the project root
    """
    return Path(__file__).parent.parent


def load_config(config_file: str) -> Dict[str, Any]:
    """
    Load configuration from a file.
    
    Args:
        config_file: Path to configuration file
    
    Returns:
        Configuration dictionary
    
    Raises:
        FileNotFoundError: If config file doesn't exist
    """
    config_path = get_project_root() / config_file
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    # Implementation depends on config file format (JSON, YAML, etc.)
    # This is a placeholder - implement based on your needs
    return {}


def ensure_directory(directory_path: str) -> Path:
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        directory_path: Path to directory
    
    Returns:
        Path object pointing to the directory
    """
    path = Path(directory_path)
    path.mkdir(parents=True, exist_ok=True)
    return path