#!/usr/bin/env python3
"""
Tests for the development_tools module.
"""

import os
from typing import Any

import pytest

from create_python_project.utils import development_tools


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
        ]
    }


@pytest.fixture
def django_tech_stack() -> dict[str, Any]:
    """Provide a Django tech stack for testing."""
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
        ]
    }


@pytest.fixture
def react_tech_stack() -> dict[str, Any]:
    """Provide a tech stack with React for testing."""
    return {
        "categories": [
            {
                "name": "Frontend",
                "options": [
                    {
                        "name": "React",
                        "description": "Modern UI library",
                        "recommended": True,
                    },
                ],
            },
        ]
    }


class TestSetupDevelopmentTools:
    """Test the setup_development_tools function."""

    def test_setup_development_tools_basic(self, temp_dir, mock_tech_stack):
        """Test setting up development tools with minimal tech stack."""
        # Arrange
        project_dir = temp_dir

        # Act
        success, message = development_tools.setup_development_tools(
            project_dir, mock_tech_stack
        )

        # Assert
        assert success is True
        assert "Development tools configured successfully" in message

        # Verify essential files
        assert os.path.exists(os.path.join(project_dir, ".pre-commit-config.yaml"))
        assert os.path.exists(os.path.join(project_dir, ".config/mypy.ini"))
        assert os.path.exists(os.path.join(project_dir, ".config/ruff.toml"))
        assert os.path.exists(os.path.join(project_dir, ".secrets.baseline"))
        assert os.path.exists(os.path.join(project_dir, "scripts/quality_check.py"))
        assert os.path.exists(os.path.join(project_dir, "scripts/dev_setup.py"))

        # Check execute permissions on scripts
        assert os.access(os.path.join(project_dir, "scripts/quality_check.py"), os.X_OK)
        assert os.access(os.path.join(project_dir, "scripts/dev_setup.py"), os.X_OK)

    def test_setup_development_tools_django(self, temp_dir, django_tech_stack):
        """Test setting up development tools with Django tech stack."""
        # Arrange
        project_dir = temp_dir

        # Act
        success, message = development_tools.setup_development_tools(
            project_dir, django_tech_stack
        )

        # Assert
        assert success is True

        # Verify Django-specific configurations in pre-commit
        with open(os.path.join(project_dir, ".pre-commit-config.yaml")) as f:
            content = f.read()
            assert "django-upgrade" in content
            assert "--target-version" in content

    def test_setup_development_tools_react(self, temp_dir, react_tech_stack):
        """Test setting up development tools with React tech stack."""
        # Arrange
        project_dir = temp_dir

        # Act
        success, message = development_tools.setup_development_tools(
            project_dir, react_tech_stack
        )

        # Assert
        assert success is True

        # Verify React-specific configurations in pre-commit
        with open(os.path.join(project_dir, ".pre-commit-config.yaml")) as f:
            content = f.read()
            assert "eslint" in content
            assert "(js|jsx|ts|tsx)" in content
            assert "typescript" in content.lower()


class TestCreatePrecommitConfig:
    """Test the _create_precommit_config function."""

    def test_create_precommit_config_basic(self, temp_dir, mock_tech_stack):
        """Test creating basic pre-commit configuration."""
        # Arrange
        project_dir = temp_dir

        # Act
        development_tools._create_precommit_config(project_dir, mock_tech_stack)
        config_file = os.path.join(project_dir, ".pre-commit-config.yaml")

        # Assert
        assert os.path.exists(config_file)

        # Check content
        with open(config_file) as f:
            content = f.read()
            assert "default_stages: [pre-commit]" in content
            assert "repo: https://github.com/psf/black" in content
            assert "repo: https://github.com/astral-sh/ruff-pre-commit" in content
            assert "repo: https://github.com/pre-commit/mirrors-mypy" in content
            assert "repo: https://github.com/Yelp/detect-secrets" in content
            assert "repo: https://github.com/pre-commit/pre-commit-hooks" in content
            assert "repo: https://github.com/commitizen-tools/commitizen" in content


class TestCreateLintingConfigs:
    """Test the _create_linting_configs function."""

    def test_create_linting_configs(self, temp_dir):
        """Test creating linting configuration files."""
        # Arrange
        project_dir = temp_dir

        # Act
        development_tools._create_linting_configs(project_dir)
        config_dir = os.path.join(project_dir, ".config")

        # Assert
        assert os.path.exists(config_dir)
        assert os.path.exists(os.path.join(config_dir, "mypy.ini"))
        assert os.path.exists(os.path.join(config_dir, "ruff.toml"))
        assert os.path.exists(os.path.join(project_dir, ".secrets.baseline"))

        # Check mypy config content
        with open(os.path.join(config_dir, "mypy.ini")) as f:
            content = f.read()
            assert "[mypy]" in content
            assert "python_version = 3.11" in content
            assert "disallow_untyped_defs = True" in content
            assert "[[mypy.overrides]]" in content

        # Check ruff config content
        with open(os.path.join(config_dir, "ruff.toml")) as f:
            content = f.read()
            assert 'target-version = "py311"' in content
            assert "line-length = 88" in content
            assert "[lint]" in content
            assert "[format]" in content


class TestCreateDevScripts:
    """Test the _create_dev_scripts function."""

    def test_create_dev_scripts(self, temp_dir):
        """Test creating development utility scripts."""
        # Arrange
        project_dir = temp_dir

        # Act
        development_tools._create_dev_scripts(project_dir)
        scripts_dir = os.path.join(project_dir, "scripts")

        # Assert
        assert os.path.exists(scripts_dir)
        assert os.path.exists(os.path.join(scripts_dir, "quality_check.py"))
        assert os.path.exists(os.path.join(scripts_dir, "dev_setup.py"))

        # Check script content
        with open(os.path.join(scripts_dir, "quality_check.py")) as f:
            content = f.read()
            assert "Run all code quality checks" in content
            assert "run_command" in content
            assert "black" in content
            assert "ruff" in content
            assert "mypy" in content
            assert "pytest" in content
            assert "detect-secrets" in content

        # Check execute permissions
        assert os.access(os.path.join(scripts_dir, "quality_check.py"), os.X_OK)
        assert os.access(os.path.join(scripts_dir, "dev_setup.py"), os.X_OK)


class TestCreatePytestConfig:
    """Test the create_pytest_config function."""

    def test_create_pytest_config(self, temp_dir):
        """Test creating pytest configuration."""
        # Arrange
        project_dir = temp_dir

        # Create a basic pyproject.toml
        with open(os.path.join(project_dir, "pyproject.toml"), "w") as f:
            f.write('[tool.poetry]\nname = "test-project"\nversion = "0.1.0"\n')

        # Act
        development_tools.create_pytest_config(project_dir)

        # Assert
        assert os.path.exists(os.path.join(project_dir, "pyproject.toml"))

        # Check content
        with open(os.path.join(project_dir, "pyproject.toml")) as f:
            content = f.read()
            assert "[tool.pytest.ini_options]" in content
            assert 'testpaths = ["tests"]' in content
            assert "--cov=src" in content
            assert "--cov-fail-under=80" in content
            assert "markers = [" in content


class TestCreateCoverageConfig:
    """Test the create_coverage_config function."""

    def test_create_coverage_config(self, temp_dir):
        """Test creating coverage configuration."""
        # Arrange
        project_dir = temp_dir

        # Create a basic pyproject.toml
        with open(os.path.join(project_dir, "pyproject.toml"), "w") as f:
            f.write('[tool.poetry]\nname = "test-project"\nversion = "0.1.0"\n')

        # Act
        development_tools.create_coverage_config(project_dir)

        # Assert
        assert os.path.exists(os.path.join(project_dir, "pyproject.toml"))

        # Check content
        with open(os.path.join(project_dir, "pyproject.toml")) as f:
            content = f.read()
            assert "[tool.coverage.run]" in content
            assert 'source = ["src"]' in content
            assert "branch = true" in content
            assert "[tool.coverage.report]" in content
            assert "show_missing = true" in content
            assert "[tool.coverage.html]" in content


class TestExtractTechChoice:
    """Test the _extract_tech_choice function."""

    def test_extract_tech_choice_exists(self, mock_tech_stack):
        """Test extraction of an existing tech choice."""
        # Act
        result = development_tools._extract_tech_choice(
            mock_tech_stack, "Backend Framework"
        )

        # Assert
        assert result == "Flask"

    def test_extract_tech_choice_missing(self, mock_tech_stack):
        """Test extraction of a non-existent tech choice."""
        # Act
        result = development_tools._extract_tech_choice(
            mock_tech_stack, "Missing Category"
        )

        # Assert
        assert result == ""

    def test_extract_tech_choice_empty_stack(self):
        """Test extraction with an empty tech stack."""
        # Act
        result = development_tools._extract_tech_choice({}, "Any Category")

        # Assert
        assert result == ""
