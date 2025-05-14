"""
Tests for the logging module.
"""

import os

from create_python_project.utils.logging import create_logging_module, setup_logging


class TestSetupLogging:
    """Tests for the setup_logging function."""

    def test_setup_logging_default(self) -> None:
        """Test setting up logging with default parameters."""
        # Execute
        logger = setup_logging()

        # Assert
        assert logger.name == "create_python_project", "Logger name is incorrect"
        assert len(logger.handlers) > 0, "Logger has no handlers"

    def test_setup_logging_custom_dir(self, temp_dir: str) -> None:
        """Test setting up logging with a custom log directory."""
        # Setup
        log_dir = os.path.join(temp_dir, "logs")

        # Execute
        logger = setup_logging(log_dir=log_dir)

        # Assert
        assert logger.name == "create_python_project", "Logger name is incorrect"
        assert len(logger.handlers) > 0, "Logger has no handlers"
        assert os.path.exists(log_dir), "Log directory was not created"


class TestCreateLoggingModule:
    """Tests for the create_logging_module function."""

    def test_create_logging_module(self, temp_dir: str) -> None:
        """Test creating a logging module in a project."""
        # Setup
        project_name = "test_project"
        project_dir = os.path.join(temp_dir, project_name)
        os.makedirs(os.path.join(project_dir, "utils"), exist_ok=True)

        # Execute
        success, message = create_logging_module(project_dir, project_name)

        # Assert
        assert success, f"Logging module creation failed: {message}"
        assert os.path.exists(
            os.path.join(project_dir, "utils", "logging.py")
        ), "logging.py not created"
        assert success, f"Logging module creation failed: {message}"
        assert os.path.exists(
            os.path.join(project_dir, "utils", "logging.py")
        ), "logging.py not created"
