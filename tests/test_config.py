"""
Tests for the config module.
"""

import os

from create_python_project.utils.config import (
    create_env_file,
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
        expected_types = ["basic", "web", "cli", "data", "ai"]
        for type_name in expected_types:
            assert type_name in project_types, f"{type_name} not found in project types"
            assert isinstance(
                project_types[type_name], dict
            ), f"{type_name} entry is not a dictionary"
            assert type_name in project_types, f"{type_name} not found in project types"
            assert isinstance(
                project_types[type_name], dict
            ), f"{type_name} entry is not a dictionary"
