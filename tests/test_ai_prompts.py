"""
Tests for the ai_prompts module.
"""

from create_python_project.utils.ai_prompts import (
    get_dependencies_prompt,
    get_project_structure_prompt,
    get_project_type_prompt,
)


class TestProjectTypePrompt:
    """Tests for the get_project_type_prompt function."""

    def test_get_project_type_prompt(self) -> None:
        """Test getting a project type prompt."""
        # Setup
        project_name = "test_project"
        project_description = "A test project for data analysis"

        # Execute
        prompt = get_project_type_prompt(project_name, project_description)

        # Assert
        assert isinstance(prompt, str), "Prompt should be a string"
        assert project_name in prompt, "Project name not found in prompt"
        assert project_description in prompt, "Project description not found in prompt"


class TestProjectStructurePrompt:
    """Tests for the get_project_structure_prompt function."""

    def test_get_project_structure_prompt(self) -> None:
        """Test getting a project structure prompt."""
        # Setup
        project_name = "test_project"
        project_description = "A test project for web development"
        project_type = "web"

        # Execute
        prompt = get_project_structure_prompt(
            project_name, project_description, project_type
        )

        # Assert
        assert isinstance(prompt, str), "Prompt should be a string"
        assert project_name in prompt, "Project name not found in prompt"
        assert project_description in prompt, "Project description not found in prompt"
        assert project_type in prompt, "Project type not found in prompt"


class TestDependenciesPrompt:
    """Tests for the get_dependencies_prompt function."""

    def test_get_dependencies_prompt(self) -> None:
        """Test getting a dependencies prompt."""
        # Setup
        project_name = "test_project"
        project_description = "A test project for data science"
        project_type = "data"

        # Execute
        prompt = get_dependencies_prompt(
            project_name, project_description, project_type
        )

        # Assert
        assert isinstance(prompt, str), "Prompt should be a string"
        assert project_name in prompt, "Project name not found in prompt"
        assert project_description in prompt, "Project description not found in prompt"
        assert project_type in prompt, "Project type not found in prompt"
        assert project_type in prompt, "Project type not found in prompt"
