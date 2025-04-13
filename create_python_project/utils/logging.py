"""
Logging configuration for the project.

Provides detailed logging to help analyze issues and debug code problems.
Captures information about script execution, error states, and failure points.
"""

import logging
import logging.config
import os
from pathlib import Path

def configure_logging(log_level="INFO", log_file=None):
    """
    Configure logging for the application to help with debugging and issue analysis.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
    
    Returns:
        logging.Logger: The configured logger
    """
    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": log_level,
            "stream": "ext://sys.stdout",
        }
    }
    
    if log_file:
        # Create log directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            
        handlers["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "level": log_level,
            "filename": log_file,
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf8",
        }
    
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"
            },
        },
        "handlers": handlers,
        "loggers": {
            "": {  # Root logger
                "handlers": list(handlers.keys()),
                "level": log_level,
                "propagate": True,
            }
        },
    }
    
    logging.config.dictConfig(config)
    return logging.getLogger()
