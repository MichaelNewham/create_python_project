"""
Tests for the config module.
"""

import os
from typing import Any

import pytest

from create_python_project.utils.config import (
    _extract_dependencies_from_tech_stack,
    create_env_file,
    get_project_dependencies,
    get_project_types,
    load_env_file,
)


class TestLoadEnvFile:
    """Tests for the load_env_file function."""

    def test_load_env_file(self, temp_dir: str) -> None:
        """Test loading an environment file."""
        # Setup
        env_file = os.path.join(temp_dir, ".env")
        with open(env_file, "w") as f:
            f.write("TEST_VAR=test_value\n")
            f.write("ANOTHER_VAR=another_value\n")

        # Execute
        env_vars = load_env_file(env_file)

        # Assert
        assert isinstance(env_vars, dict), "Result should be a dictionary"
        assert env_vars.get("TEST_VAR") == "test_value", "TEST_VAR has incorrect value"
        assert (
            env_vars.get("ANOTHER_VAR") == "another_value"
        ), "ANOTHER_VAR has incorrect value"

    def test_load_env_file_not_exists(self) -> None:
        """Test loading a non-existent environment file."""
        # Setup
        env_file = "non_existent.env"

        # Execute
        env_vars = load_env_file(env_file)

        # Assert
        assert isinstance(env_vars, dict), "Result should be a dictionary"
        assert len(env_vars) == 0, "Dictionary should be empty"


class TestCreateEnvFile:
    """Tests for the create_env_file function."""

    def test_create_env_file(self, temp_dir: str) -> None:
        """Test creating an environment file."""
        # Setup
        project_dir = temp_dir
        variables = {
            "TEST_VAR": "test_value",
            "ANOTHER_VAR": "another_value",
        }

        # Execute
        success, message = create_env_file(project_dir, variables)

        # Assert
        assert success, f"Env file creation failed: {message}"

        env_file = os.path.join(project_dir, ".env")
        assert os.path.exists(env_file), ".env file not created"

        # Check file contents
        with open(env_file) as f:
            content = f.read()

        assert "TEST_VAR=test_value" in content, "TEST_VAR not found in .env file"
        assert (
            "ANOTHER_VAR=another_value" in content
        ), "ANOTHER_VAR not found in .env file"


@pytest.fixture
def mock_tech_stack() -> dict[str, Any]:
    """Provide a mock tech stack for testing."""
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
                    {
                        "name": "Flask",
                        "description": "Lightweight web framework",
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
                ],
            },
        ]
    }


class TestGetProjectDependencies:
    """Tests for the get_project_dependencies function."""

    def test_get_project_dependencies_defaults(self) -> None:
        """Test getting default dependencies without tech stack."""
        # Execute
        dependencies = get_project_dependencies(project_type="web")

        # Assert
        assert isinstance(dependencies, dict), "Result should be a dictionary"
        assert "main" in dependencies, "'main' key not found in dependencies"
        assert "dev" in dependencies, "'dev' key not found in dependencies"

        # Check for specific dependencies
        assert "flask" in dependencies["main"], "'flask' not found in main dependencies"
        assert "pytest" in dependencies["dev"], "'pytest' not found in dev dependencies"
        assert "black" in dependencies["dev"], "'black' not found in dev dependencies"

    def test_get_project_dependencies_with_tech_stack(
        self, mock_tech_stack: dict[str, Any]
    ) -> None:
        """Test getting dependencies with AI tech stack."""
        # Execute
        dependencies = get_project_dependencies(
            project_type="web", tech_stack=mock_tech_stack
        )

        # Assert
        assert isinstance(dependencies, dict), "Result should be a dictionary"

        # Check for Django-specific dependencies (from tech stack)
        assert (
            "django" in dependencies["main"]
        ), "'django' not found in main dependencies"
        assert (
            "django-environ" in dependencies["main"]
        ), "'django-environ' not found in main dependencies"
        assert (
            "psycopg2-binary" in dependencies["main"]
        ), "'psycopg2-binary' not found in main dependencies"

        # Dev dependencies should still be present
        assert "pytest" in dependencies["dev"], "'pytest' not found in dev dependencies"


class TestExtractDependenciesFromTechStack:
    """Tests for the _extract_dependencies_from_tech_stack function."""

    def test_extract_dependencies_from_tech_stack(
        self, mock_tech_stack: dict[str, Any]
    ) -> None:
        """Test extracting dependencies from tech stack."""
        # Execute
        dependencies = _extract_dependencies_from_tech_stack(mock_tech_stack)

        # Assert
        assert isinstance(dependencies, list), "Result should be a list"
        assert len(dependencies) > 0, "No dependencies extracted"

        # Check for specific dependencies
        assert "django" in dependencies, "'django' not found in dependencies"
        assert (
            "psycopg2-binary" in dependencies
        ), "'psycopg2-binary' not found in dependencies"

    def test_extract_dependencies_empty_tech_stack(self) -> None:
        """Test extracting dependencies from empty tech stack."""
        # Execute
        dependencies = _extract_dependencies_from_tech_stack({})

        # Assert
        assert isinstance(dependencies, list), "Result should be a list"
        assert len(dependencies) == 0, "Empty tech stack should yield no dependencies"


class TestGetProjectTypes:
    """Tests for the get_project_types function."""

    def test_get_project_types(self) -> None:
        """Test getting available project types."""
        # Execute
        project_types = get_project_types()

        # Assert
        assert isinstance(project_types, dict), "Result should be a dictionary"
        assert len(project_types) > 0, "No project types found"

        # Check for specific project types
        expected_types = ["web", "cli", "data", "ai"]
        for type_name in expected_types:
            assert type_name in project_types, f"{type_name} not found in project types"
            assert isinstance(
                project_types[type_name], dict
            ), f"{type_name} entry is not a dictionary"
