#!/usr/bin/env python3
"""
Tests for the workspace_config module.
"""

import json
import os
from typing import Any

import pytest

from create_python_project.utils import workspace_config


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
                    {
                        "name": "Django",
                        "description": "Full-featured web framework",
                        "recommended": False,
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
                    {
                        "name": "SQLite",
                        "description": "Lightweight file-based database",
                        "recommended": False,
                    },
                ],
            },
            {
                "name": "Frontend",
                "options": [
                    {
                        "name": "React",
                        "description": "Modern UI library",
                        "recommended": True,
                    },
                    {
                        "name": "Vue.js",
                        "description": "Progressive framework",
                        "recommended": False,
                    },
                ],
            },
        ]
    }


@pytest.fixture
def web_tech_stack() -> dict[str, Any]:
    """Provide a web project tech stack for testing."""
    return {
        "categories": [
            {
                "name": "Backend Framework",
                "options": [
                    {
                        "name": "Django",
                        "description": "Full-featured web framework",
                        "recommended": True,
                    },
                ],
            },
            {
                "name": "Frontend",
                "options": [
                    {
                        "name": "React+TypeScript",
                        "description": "Modern UI library with TypeScript",
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


@pytest.fixture
def data_tech_stack() -> dict[str, Any]:
    """Provide a data science tech stack for testing."""
    return {
        "categories": [
            {
                "name": "Data Processing",
                "options": [
                    {
                        "name": "Pandas",
                        "description": "Data analysis library",
                        "recommended": True,
                    },
                ],
            },
            {
                "name": "Visualization",
                "options": [
                    {
                        "name": "Matplotlib",
                        "description": "Visualization library",
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


class TestCreateWorkspaceFile:
    """Test the create_workspace_file function."""

    def test_create_basic_workspace_file(self, temp_dir, mock_tech_stack):
        """Test creation of a basic workspace file."""
        # Arrange
        project_dir = temp_dir
        project_name = "test_project"
        project_type = "basic"

        # Act
        success, message = workspace_config.create_workspace_file(
            project_dir, project_name, project_type, mock_tech_stack
        )
        workspace_file = os.path.join(project_dir, f"{project_name}.code-workspace")

        # Assert
        assert success is True
        assert "Workspace file created" in message
        assert os.path.exists(workspace_file)

        # Verify workspace file content
        with open(workspace_file) as f:
            workspace_data = json.load(f)
            assert "folders" in workspace_data
            assert "settings" in workspace_data
            assert "extensions" in workspace_data
            assert "tasks" in workspace_data
            assert "launch" in workspace_data

            # Verify folder structure
            folders = [folder["name"] for folder in workspace_data["folders"]]
            assert "Test Project" in folders
            assert "Tests" in folders
            assert "Scripts" in folders
            assert "Documentation" in folders

    def test_create_web_workspace_file(self, temp_dir, web_tech_stack):
        """Test creation of a web project workspace file."""
        # Arrange
        project_dir = temp_dir
        project_name = "web_project"
        project_type = "web"

        # Act
        success, message = workspace_config.create_workspace_file(
            project_dir, project_name, project_type, web_tech_stack
        )
        workspace_file = os.path.join(project_dir, f"{project_name}.code-workspace")

        # Assert
        assert success is True
        assert "Workspace file created" in message
        assert os.path.exists(workspace_file)

        # Verify workspace file content
        with open(workspace_file) as f:
            workspace_data = json.load(f)

            # Check for web-specific folders
            folders = workspace_data["folders"]
            folder_names = [folder["name"] for folder in folders]
            assert "Backend" in folder_names
            assert "Frontend" in folder_names

            # Check for Django-specific settings
            settings = workspace_data["settings"]
            assert "django.managePyPath" in settings
            assert "emmet.includeLanguages" in settings
            assert "files.associations" in settings

            # Check for React extensions
            extensions = workspace_data["extensions"]["recommendations"]
            react_extensions = [ext for ext in extensions if "react" in ext.lower()]
            assert len(react_extensions) > 0
            assert any("typescript" in ext.lower() for ext in extensions)

    def test_create_data_workspace_file(self, temp_dir, data_tech_stack):
        """Test creation of a data science workspace file."""
        # Arrange
        project_dir = temp_dir
        project_name = "data_project"
        project_type = "data"

        # Act
        success, message = workspace_config.create_workspace_file(
            project_dir, project_name, project_type, data_tech_stack
        )
        workspace_file = os.path.join(project_dir, f"{project_name}.code-workspace")

        # Assert
        assert success is True
        assert "Workspace file created" in message
        assert os.path.exists(workspace_file)

        # Verify workspace file content
        with open(workspace_file) as f:
            workspace_data = json.load(f)

            # Check for data-specific folders
            folders = workspace_data["folders"]
            folder_names = [folder["name"] for folder in folders]
            assert "Data" in folder_names
            assert "Notebooks" in folder_names

            # Check for data science specific settings
            settings = workspace_data["settings"]
            assert "jupyter.askForKernelRestart" in settings
            assert "jupyter.interactiveWindowMode" in settings
            assert "python.dataScience.enableCellCodeLens" in settings

            # Check for data science extensions
            extensions = workspace_data["extensions"]["recommendations"]
            assert any("jupyter" in ext.lower() for ext in extensions)
            assert any("csv" in ext.lower() for ext in extensions)
            assert any("data-preview" in ext.lower() for ext in extensions)


class TestExtractTechChoice:
    """Test the _extract_tech_choice function."""

    def test_extract_tech_choice_exists(self, mock_tech_stack):
        """Test extraction of an existing tech choice."""
        # Act
        result = workspace_config._extract_tech_choice(
            mock_tech_stack, "Backend Framework"
        )

        # Assert
        assert result == "Flask"

    def test_extract_tech_choice_missing(self, mock_tech_stack):
        """Test extraction of a non-existent tech choice."""
        # Act
        result = workspace_config._extract_tech_choice(
            mock_tech_stack, "Missing Category"
        )

        # Assert
        assert result == ""

    def test_extract_tech_choice_empty_stack(self):
        """Test extraction with an empty tech stack."""
        # Act
        result = workspace_config._extract_tech_choice({}, "Any Category")

        # Assert
        assert result == ""
