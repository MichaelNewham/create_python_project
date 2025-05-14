"""
Tests for the core_project_builder module.
"""

import os

from create_python_project.utils.core_project_builder import (
    create_project_structure,
    setup_virtual_environment,
)


class TestCreateProjectStructure:
    """Tests for the create_project_structure function."""

    def test_create_basic_project(self, temp_dir: str) -> None:
        """Test creating a basic project."""
        # Setup
        project_name = "test_project"
        project_dir = os.path.join(temp_dir, project_name)
        project_type = "basic"

        # Execute
        success, message = create_project_structure(
            project_name=project_name,
            project_dir=project_dir,
            project_type=project_type,
        )

        # Assert
        assert success, f"Project creation failed: {message}"
        assert os.path.exists(project_dir), "Project directory was not created"
        assert os.path.exists(
            os.path.join(project_dir, "README.md")
        ), "README.md not created"
        assert os.path.exists(
            os.path.join(project_dir, "pyproject.toml")
        ), "pyproject.toml not created"
        assert os.path.exists(
            os.path.join(project_dir, ".gitignore")
        ), ".gitignore not created"

    def test_create_project_with_ai(self, temp_dir: str) -> None:
        """Test creating a project with AI integration."""
        # Setup
        project_name = "test_ai_project"
        project_dir = os.path.join(temp_dir, project_name)
        project_type = "ai"

        # Execute
        success, message = create_project_structure(
            project_name=project_name,
            project_dir=project_dir,
            project_type=project_type,
            with_ai=True,
        )

        # Assert
        assert success, f"Project creation failed: {message}"
        assert os.path.exists(
            os.path.join(project_dir, "ai-docs")
        ), "ai-docs directory not created"
        assert os.path.exists(
            os.path.join(project_dir, ".claude")
        ), ".claude file not created"


class TestSetupVirtualEnvironment:
    """Tests for the setup_virtual_environment function."""

    def test_setup_virtual_environment(self, temp_dir: str) -> None:
        """Test setting up a virtual environment."""
        # Setup
        project_dir = temp_dir

        # Execute
        success, message = setup_virtual_environment(project_dir)

        # Assert
        assert success, f"Virtual environment setup failed: {message}"
        assert os.path.exists(
            os.path.join(project_dir, ".venv")
        ), ".venv directory not created"
        assert success, f"Virtual environment setup failed: {message}"
        assert os.path.exists(
            os.path.join(project_dir, ".venv")
        ), ".venv directory not created"
