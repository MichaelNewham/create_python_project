#!/usr/bin/env python3
"""
Logging Module

This module provides logging functionality for the Create Python Project application.
It configures loggers, handlers, and formatters for proper logging.
"""

import logging
import os


def setup_logging(log_dir: str | None = None) -> logging.Logger:
    """
    Set up and configure logging for the application.

    Args:
        log_dir: Directory where log files should be stored

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("create_python_project")
    logger.setLevel(logging.DEBUG)

    # Clear existing handlers if any
    if logger.handlers:
        logger.handlers.clear()

    # Create console handler - only show warnings and errors by default
    console_handler = logging.StreamHandler()
    # Check if DEBUG environment variable is set for verbose output
    console_level = logging.DEBUG if os.getenv("DEBUG") else logging.WARNING
    console_handler.setLevel(console_level)
    console_format = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # Create file handler if log_dir is provided
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "create_python_project.log")
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger


def create_logging_module(project_dir: str, project_name: str) -> tuple[bool, str]:
    """
    Create a logging module in the new project.

    Args:
        project_dir: The directory of the project
        project_name: The name of the project

    Returns:
        Tuple containing success status and message
    """
    try:
        # Create utils directory if it doesn't exist
        utils_dir = os.path.join(project_dir, "utils")
        os.makedirs(utils_dir, exist_ok=True)

        # Create logging.py file
        logging_file_path = os.path.join(utils_dir, "logging.py")

        # Create the content for the logging module
        logging_content = f'''#!/usr/bin/env python3
"""
Logging Module for {project_name}

This module handles logging setup and configuration.
"""

import logging
import os
from typing import Optional


def setup_logging(log_dir: Optional[str] = None) -> logging.Logger:
    """
    Set up and configure logging for the application.

    Args:
        log_dir: Directory where log files should be stored

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("{project_name}")
    logger.setLevel(logging.DEBUG)

    # Clear existing handlers if any
    if logger.handlers:
        logger.handlers.clear()

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # Create file handler if log_dir is provided
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "{project_name}.log")
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger
'''

        # Write the content to the file
        with open(logging_file_path, "w", encoding="utf-8") as f:
            f.write(logging_content)

        return True, f"Created logging module at {logging_file_path}"
    except Exception as e:
        return False, f"Failed to create logging module: {str(e)}"
