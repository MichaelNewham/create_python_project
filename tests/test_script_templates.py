#!/usr/bin/env python3
"""
Tests for the script_templates module.
"""

import os
from typing import Any

import pytest

from create_python_project.utils import script_templates


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
        ]
    }


class TestCreateAutomationScripts:
    """Test the create_automation_scripts function."""

    def test_create_basic_scripts(self, temp_dir, mock_tech_stack):
        """Test creation of basic automation scripts."""
        # Arrange
        project_dir = temp_dir
        project_name = "test_project"
        package_name = "test_project"

        # Act
        success, message = script_templates.create_automation_scripts(
            project_dir, package_name, project_name, mock_tech_stack
        )
        scripts_dir = os.path.join(project_dir, "scripts")

        # Assert
        assert success is True
        assert "Automation scripts created successfully" in message
        assert os.path.exists(scripts_dir)

        # Verify expected script files exist
        expected_scripts = [
            "commit_workflow.py",
            "clean_run.py",
            "deploy.py",
            "maintenance.py",
            "test_runner.py",
        ]
        for script in expected_scripts:
            script_path = os.path.join(scripts_dir, script)
            assert os.path.exists(script_path), f"Script {script} missing"
            assert os.access(script_path, os.X_OK), f"Script {script} not executable"

        # Check script content
        with open(os.path.join(scripts_dir, "commit_workflow.py")) as f:
            content = f.read()
            assert "AI-powered commit workflow" in content
            assert "class CommitWorkflow" in content

    def test_create_django_specific_scripts(self, temp_dir, django_tech_stack):
        """Test creation of Django-specific scripts."""
        # Arrange
        project_dir = temp_dir
        project_name = "django_project"
        package_name = "django_project"

        # Act
        success, message = script_templates.create_automation_scripts(
            project_dir, package_name, project_name, django_tech_stack
        )
        scripts_dir = os.path.join(project_dir, "scripts")

        # Assert
        assert success is True
        assert os.path.exists(scripts_dir)

        # Verify Django-specific script
        django_script = os.path.join(scripts_dir, "django_manage.py")
        assert os.path.exists(django_script), "Django management script missing"
        assert os.access(django_script, os.X_OK), "Django script not executable"

        # Check script content
        with open(django_script) as f:
            content = f.read()
            assert "Django management script" in content
            assert "runserver" in content
            assert "migrate" in content

    def test_create_data_specific_scripts(self, temp_dir, data_tech_stack):
        """Test creation of data science specific scripts."""
        # Arrange
        project_dir = temp_dir
        project_name = "data_project"
        package_name = "data_project"

        # Act
        success, message = script_templates.create_automation_scripts(
            project_dir, package_name, project_name, data_tech_stack
        )
        scripts_dir = os.path.join(project_dir, "scripts")

        # Assert
        assert success is True
        assert os.path.exists(scripts_dir)

        # Verify data science script
        data_script = os.path.join(scripts_dir, "data_tools.py")
        assert os.path.exists(data_script), "Data tools script missing"
        assert os.access(data_script, os.X_OK), "Data script not executable"

        # Check script content
        with open(data_script) as f:
            content = f.read()
            assert "Data processing automation script" in content
            assert "jupyter" in content.lower()
            assert "notebooks" in content.lower()


class TestScriptCreationHelpers:
    """Test helper functions for script creation."""

    def test_create_commit_workflow(self, temp_dir):
        """Test creation of commit workflow script."""
        # Arrange
        scripts_dir = os.path.join(temp_dir, "scripts")
        os.makedirs(scripts_dir, exist_ok=True)
        package_name = "test_package"

        # Act
        script_templates._create_commit_workflow(scripts_dir, package_name)
        commit_script = os.path.join(scripts_dir, "commit_workflow.py")

        # Assert
        assert os.path.exists(commit_script)
        assert os.access(commit_script, os.X_OK)

        # Check content
        with open(commit_script) as f:
            content = f.read()
            assert f"AI-powered commit workflow for {package_name}" in content
            assert "class CommitWorkflow" in content
            assert "run_pre_commit_checks" in content
            assert "generate_smart_commit_message" in content

    def test_create_clean_run_script(self, temp_dir):
        """Test creation of clean run script."""
        # Arrange
        scripts_dir = os.path.join(temp_dir, "scripts")
        os.makedirs(scripts_dir, exist_ok=True)
        package_name = "test_package"

        # Act
        script_templates._create_clean_run_script(scripts_dir, package_name)
        clean_script = os.path.join(scripts_dir, "clean_run.py")

        # Assert
        assert os.path.exists(clean_script)
        assert os.access(clean_script, os.X_OK)

        # Check content
        with open(clean_script) as f:
            content = f.read()
            assert f"Clean run script for {package_name}" in content
            assert "setup_environment" in content
            assert "clear_terminal" in content

    def test_create_deployment_scripts(self, temp_dir, mock_tech_stack):
        """Test creation of deployment scripts."""
        # Arrange
        scripts_dir = os.path.join(temp_dir, "scripts")
        os.makedirs(scripts_dir, exist_ok=True)
        package_name = "test_package"

        # Act
        script_templates._create_deployment_scripts(
            scripts_dir, package_name, mock_tech_stack
        )
        deploy_script = os.path.join(scripts_dir, "deploy.py")

        # Assert
        assert os.path.exists(deploy_script)
        assert os.access(deploy_script, os.X_OK)

        # Check content
        with open(deploy_script) as f:
            content = f.read()
            assert f"Deployment script for {package_name}" in content
            assert "build_application" in content
            assert "deploy_to_production" in content
            assert "deploy_to_staging" in content


class TestExtractTechChoice:
    """Test the _extract_tech_choice function."""

    def test_extract_tech_choice_exists(self, mock_tech_stack):
        """Test extraction of an existing tech choice."""
        # Act
        result = script_templates._extract_tech_choice(
            mock_tech_stack, "Backend Framework"
        )

        # Assert
        assert result == "Flask"

    def test_extract_tech_choice_missing(self, mock_tech_stack):
        """Test extraction of a non-existent tech choice."""
        # Act
        result = script_templates._extract_tech_choice(
            mock_tech_stack, "Missing Category"
        )

        # Assert
        assert result == ""

    def test_extract_tech_choice_empty_stack(self):
        """Test extraction with an empty tech stack."""
        # Act
        result = script_templates._extract_tech_choice({}, "Any Category")

        # Assert
        assert result == ""
