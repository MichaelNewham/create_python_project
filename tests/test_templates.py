"""
Tests for the templates module.
"""

import os

from create_python_project.utils.templates import (
    create_file_from_template,
    get_template_path,
    get_template_variables,
    render_template,
)


class TestGetTemplatePath:
    """Tests for the get_template_path function."""

    def test_get_template_path(self) -> None:
        """Test getting a template path."""
        # Setup
        template_name = "readme"

        # Execute
        path = get_template_path(template_name)

        # Assert
        assert path is not None, "Template path should not be None"


class TestRenderTemplate:
    """Tests for the render_template function."""

    def test_render_template(self) -> None:
        """Test rendering a template."""
        # Setup
        template_name = "readme"
        context = {
            "project_name": "test_project",
            "project_description": "A test project",
        }

        # Execute
        rendered = render_template(template_name, context)

        # Assert
        assert isinstance(rendered, str), "Rendered template should be a string"
        assert "test_project" in rendered, "Project name not found in rendered template"
        assert (
            "A test project" in rendered
        ), "Project description not found in rendered template"


class TestCreateFileFromTemplate:
    """Tests for the create_file_from_template function."""

    def test_create_file_from_template(self, temp_dir: str) -> None:
        """Test creating a file from a template."""
        # Setup
        template_name = "readme"
        output_path = os.path.join(temp_dir, "README.md")
        context = {
            "project_name": "test_project",
            "project_description": "A test project",
        }

        # Execute
        success, message = create_file_from_template(
            template_name, output_path, context
        )

        # Assert
        assert success, f"File creation failed: {message}"
        assert os.path.exists(output_path), "File was not created"

        # Check file contents
        with open(output_path) as f:
            content = f.read()

        assert "test_project" in content, "Project name not found in created file"
        assert (
            "A test project" in content
        ), "Project description not found in created file"


class TestGetTemplateVariables:
    """Tests for the get_template_variables function."""

    def test_get_template_variables(self) -> None:
        """Test getting template variables."""
        # Setup
        project_type = "web"

        # Execute
        variables = get_template_variables(project_type)

        # Assert
        assert isinstance(variables, list), "Result should be a list"
        assert "project_name" in variables, "project_name not found in variables"
        assert (
            "project_description" in variables
        ), "project_description not found in variables"
        assert "project_name" in variables, "project_name not found in variables"
        assert (
            "project_description" in variables
        ), "project_description not found in variables"
