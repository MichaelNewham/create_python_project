"""
Tests for the core_project_builder module.
"""

import os
from typing import Any

import pytest

from create_python_project.utils.core_project_builder import (
    create_project_structure,
    initialize_git_repo,
    setup_virtual_environment,
)


@pytest.fixture
def mock_tech_stack() -> dict[str, Any]:
    """Provide a mock tech stack for testing."""
    return {
        "categories": [
            {
                "name": "Backend Framework",
                "options": [
                    {
                        "name": "Flask",
                        "description": "Lightweight web framework",
                        "recommended": True,
                    },
                ],
            },
            {
                "name": "Database",
                "options": [
                    {
                        "name": "PostgreSQL",
                        "description": "Robust relational database",
                        "recommended": True,
                    },
                ],
            },
        ]
    }


class TestInitializeGitRepo:
    """Tests for the initialize_git_repo function."""

    def test_initialize_git_repo_basic(self, temp_dir: str) -> None:
        """Test initializing a git repository without extras."""
        # Setup
        project_dir = temp_dir
        project_name = "test_project"

        # Execute
        success, message = initialize_git_repo(
            project_dir=project_dir,
            project_name=project_name,
        )

        # Assert
        assert success, f"Git initialization failed: {message}"
        assert os.path.exists(
            os.path.join(project_dir, ".git")
        ), ".git directory not created"
        assert os.path.exists(
            os.path.join(project_dir, ".gitignore")
        ), ".gitignore not created"

    def test_initialize_git_repo_with_github(
        self, temp_dir: str, mock_tech_stack: dict[str, Any]
    ) -> None:
        """Test initializing a git repository with GitHub config."""
        # Setup
        project_dir = temp_dir
        project_name = "test_github_project"
        github_username = "test-user"

        # Execute
        success, message = initialize_git_repo(
            project_dir=project_dir,
            project_name=project_name,
            github_username=github_username,
            with_github_config=True,
            project_type="web",
            tech_stack=mock_tech_stack,
        )

        # Assert
        assert success, f"Git initialization failed: {message}"
        assert os.path.exists(
            os.path.join(project_dir, ".github")
        ), ".github directory not created"
        assert os.path.exists(
            os.path.join(project_dir, ".github/CODEOWNERS")
        ), "CODEOWNERS file not created"


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

    def test_create_project_with_tech_stack(
        self, temp_dir: str, mock_tech_stack: dict[str, Any]
    ) -> None:
        """Test creating a project with a tech stack."""
        # Setup
        project_name = "tech_stack_project"
        project_dir = os.path.join(temp_dir, project_name)
        project_type = "web"

        # Execute
        success, message = create_project_structure(
            project_name=project_name,
            project_dir=project_dir,
            project_type=project_type,
            with_ai=True,
            tech_stack=mock_tech_stack,
        )

        # Assert
        assert success, f"Project creation failed: {message}"
        assert os.path.exists(
            os.path.join(project_dir, "src")
        ), "src directory not created"
        assert os.path.exists(
            os.path.join(project_dir, "scripts")
        ), "scripts directory not created"
        assert os.path.exists(
            os.path.join(project_dir, ".config")
        ), ".config directory not created"

        # Check for Flask-specific files (from tech stack)
        with open(os.path.join(project_dir, "pyproject.toml")) as f:
            content = f.read()
            assert (
                "flask" in content.lower()
            ), "Flask dependency not found in pyproject.toml"


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
