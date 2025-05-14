"""
Tests for the create_python_project main module.
"""

import os
import sys
from unittest.mock import patch

from create_python_project.create_python_project import main


class TestMainApplication:
    """Tests for the main application."""

    @patch(
        "create_python_project.create_python_project.core_project_builder.create_project_structure"
    )
    @patch("create_python_project.create_python_project.cli.enhanced_input")
    def test_main_application_flow(
        self, mock_input, mock_create_project, temp_dir: str
    ) -> None:
        """Test the main application flow."""
        # Setup
        project_name = "test_project"
        project_dir = os.path.join(temp_dir, project_name)
        project_description = "A test project"
        project_type = "basic"

        # Mock user inputs
        mock_input.side_effect = [
            project_name,  # Project name
            "y",  # Use AI
            project_description,  # Project description
            project_type,  # Project type
            project_dir,  # Project directory
            "y",  # Confirm creation
        ]

        # Mock project creation
        mock_create_project.return_value = (True, "Project created successfully")

        # Execute
        with patch.object(sys, "argv", ["create_python_project"]):
            exit_code = main()

        # Assert
        assert exit_code == 0, "Application did not exit successfully"
        mock_create_project.assert_called_once()

        # Verify the parameters passed to create_project_structure
        args, kwargs = mock_create_project.call_args
        assert kwargs["project_name"] == project_name
        assert kwargs["project_dir"] == project_dir
        assert kwargs["project_type"] == project_type

    @patch(
        "create_python_project.create_python_project.core_project_builder.create_project_structure"
    )
    @patch("create_python_project.create_python_project.cli.enhanced_input")
    def test_main_with_cli_arguments(
        self, mock_input, mock_create_project, temp_dir: str
    ) -> None:
        """Test the main application with CLI arguments."""
        # Setup
        project_name = "test_project"
        project_dir = os.path.join(temp_dir, project_name)

        # No user inputs needed when CLI args are provided
        mock_input.side_effect = []

        # Mock project creation
        mock_create_project.return_value = (True, "Project created successfully")

        # Execute with CLI arguments
        with patch.object(
            sys,
            "argv",
            [
                "create_python_project",
                "--name",
                project_name,
                "--dir",
                project_dir,
                "--type",
                "basic",
                "--no-ai",
            ],
        ):
            exit_code = main()

        # Assert
        assert exit_code == 0, "Application did not exit successfully"
        mock_create_project.assert_called_once()

        # Verify the parameters passed to create_project_structure
        args, kwargs = mock_create_project.call_args
        assert kwargs["project_name"] == project_name
        assert kwargs["project_dir"] == project_dir
        assert kwargs["project_type"] == "basic"
        assert kwargs["with_ai"] is False
        assert kwargs["project_type"] == "basic"
        assert kwargs["with_ai"] is False
