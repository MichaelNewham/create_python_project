#!/usr/bin/env python3
"""
Core Project Builder Module

This module contains the core functionality for creating Python projects.
It handles file creation, directory structure, and template rendering.
"""

import os
import shutil
import subprocess
import sys
from typing import Any, Tuple


def create_project_structure(
    project_name: str,
    project_dir: str,
    project_type: str,
    with_ai: bool = True,
    **kwargs: Any,
) -> Tuple[bool, str]:
    """
    Create the base project structure.

    Args:
        project_name: Name of the project
        project_dir: Directory where the project should be created
        project_type: Type of the project (web, cli, etc.)
        with_ai: Whether to include AI integration
        **kwargs: Additional parameters for project creation

    Returns:
        Tuple containing success status and message
    """
    try:
        # Create project directory if it doesn't exist
        os.makedirs(project_dir, exist_ok=True)

        # Create base files
        base_files = {
            "README.md": f"# {project_name}\n\n{kwargs.get('description', 'A Python project.')}\n",
            ".gitignore": """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environments
venv/
.env
.venv
env/
ENV/

# IDE files
.idea/
.vscode/
*.swp
*.swo

# Logs
logs/
*.log
            """,
            "pyproject.toml": f"""
[tool.poetry]
name = "{project_name.replace('-', '_').replace(' ', '_').lower()}"
version = "0.1.0"
description = "{kwargs.get('description', 'A Python project.')}"
authors = ["{kwargs.get('author_name', 'Your Name')} <{kwargs.get('author_email', 'your.email@example.com')}>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^{kwargs.get('python_version', '3.9')}"

[tool.poetry.group.dev.dependencies]
pytest = "^7.3.1"
black = "^23.3.0"
pylint = "^2.17.4"
mypy = "^1.3.0"
pytest-cov = "^4.1.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
            """,
        }

        for filename, content in base_files.items():
            with open(os.path.join(project_dir, filename), "w") as file:
                file.write(content)

        # Create src directory with project package
        src_dir = os.path.join(project_dir, "src")
        package_dir = os.path.join(
            src_dir, project_name.replace("-", "_").replace(" ", "_").lower()
        )
        os.makedirs(package_dir, exist_ok=True)

        # Create __init__.py
        with open(os.path.join(package_dir, "__init__.py"), "w") as file:
            file.write(
                f'"""Top-level package for {project_name}."""\n\n__version__ = "0.1.0"\n'
            )

        # Create tests directory
        tests_dir = os.path.join(project_dir, "tests")
        os.makedirs(tests_dir, exist_ok=True)
        with open(os.path.join(tests_dir, "__init__.py"), "w") as file:
            file.write('"""Test package for the project."""\n')

        # Add AI integration if requested
        if with_ai:
            ai_docs_dir = os.path.join(project_dir, "ai-docs")
            os.makedirs(ai_docs_dir, exist_ok=True)

            # Create claude file
            with open(os.path.join(project_dir, ".claude"), "w") as file:
                file.write(f"workspaceName: {project_name}\n")

            # Create convo.md in ai-docs
            with open(os.path.join(ai_docs_dir, "convo.md"), "w") as file:
                file.write(
                    f"# {project_name} Project\n\nThis file contains the conversation history with AI assistants for this project.\n"
                )

        # Create additional project-specific files based on project_type
        if project_type == "web":
            # Create web-specific directories
            templates_dir = os.path.join(package_dir, "templates")
            static_dir = os.path.join(package_dir, "static")
            os.makedirs(templates_dir, exist_ok=True)
            os.makedirs(static_dir, exist_ok=True)

            # Add web-specific dependencies to pyproject.toml
            with open(os.path.join(project_dir, "pyproject.toml"), "a") as file:
                file.write('\nflask = "^2.3.2"\n')

        elif project_type == "cli":
            # Add CLI entry point to pyproject.toml
            with open(os.path.join(project_dir, "pyproject.toml"), "a") as file:
                file.write(
                    f"""
[tool.poetry.scripts]
{project_name.replace('-', '_').replace(' ', '_').lower()} = "{project_name.replace('-', '_').replace(' ', '_').lower()}.cli:main"
                """
                )

            # Create CLI module
            cli_file = os.path.join(package_dir, "cli.py")
            with open(cli_file, "w", encoding="utf-8") as file:
                file.write(
                    f'''"""Command-line interface for {project_name}."""

import sys
import argparse


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="{kwargs.get('description', 'A Python CLI application.')}")
    # Add arguments here
    args = parser.parse_args()
    
    # Main logic here
    print("Hello from {project_name}!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''
                )

        elif project_type == "ai":
            # Create AI-specific directories
            models_dir = os.path.join(package_dir, "models")
            prompts_dir = os.path.join(package_dir, "prompts")
            os.makedirs(models_dir, exist_ok=True)
            os.makedirs(prompts_dir, exist_ok=True)

            # Add AI-specific dependencies to pyproject.toml
            with open(os.path.join(project_dir, "pyproject.toml"), "a") as file:
                file.write('\nopenai = "^1.1.1"\n')

        # Create utils directory in the project package
        utils_dir = os.path.join(package_dir, "utils")
        os.makedirs(utils_dir, exist_ok=True)
        with open(os.path.join(utils_dir, "__init__.py"), "w") as file:
            file.write('"""Utility functions for the project."""\n')

        return True, f"Project structure created at {project_dir}"

    except Exception as e:
        return False, f"Failed to create project structure: {str(e)}"


def setup_virtual_environment(project_dir: str) -> Tuple[bool, str]:
    """
    Set up a virtual environment in the project directory.

    Args:
        project_dir: The project directory where the virtual environment should be created

    Returns:
        Tuple containing success status and message
    """
    try:
        venv_dir = os.path.join(project_dir, ".venv")

        # Create virtual environment
        if sys.platform.startswith("win"):
            python_exe = sys.executable
            subprocess.run([python_exe, "-m", "venv", venv_dir], check=True)
        else:
            subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)

        # Install dependencies using Poetry if available
        if shutil.which("poetry"):
            cmd = ["poetry", "install"]
            subprocess.run(cmd, cwd=project_dir, check=True)

        return True, f"Virtual environment created at {venv_dir}"
    except Exception as e:
        return False, f"Failed to set up virtual environment: {str(e)}"


def initialize_git_repo(
    project_dir: str,
    project_name: str,
    github_username: str = "",
    gitlab_username: str = "",
) -> Tuple[bool, str]:
    """
    Initialize a Git repository and set up GitHub and GitLab remotes.

    Args:
        project_dir: The project directory
        project_name: Name of the project
        github_username: GitHub username for remote setup
        gitlab_username: GitLab username for remote setup

    Returns:
        Tuple containing success status and message
    """
    try:
        # Check if git is installed
        if not shutil.which("git"):
            return False, "Git is not installed or not in PATH"

        # Initialize git repository
        subprocess.run(["git", "init"], cwd=project_dir, check=True)

        # Add all files to git
        subprocess.run(["git", "add", "."], cwd=project_dir, check=True)

        # Create initial commit
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"], cwd=project_dir, check=True
        )

        # Set up remotes if usernames are provided
        if github_username:
            repo_name = project_name.replace(" ", "-").lower()
            github_url = f"https://github.com/{github_username}/{repo_name}.git"
            subprocess.run(
                ["git", "remote", "add", "github", github_url],
                cwd=project_dir,
                check=True,
            )

        if gitlab_username:
            repo_name = project_name.replace(" ", "-").lower()
            gitlab_url = f"https://gitlab.com/{gitlab_username}/{repo_name}.git"
            subprocess.run(
                ["git", "remote", "add", "gitlab", gitlab_url],
                cwd=project_dir,
                check=True,
            )

        return True, "Git repository initialized with remotes"
    except subprocess.CalledProcessError as e:
        return False, f"Git command failed: {str(e)}"
    except Exception as e:
        return False, f"Failed to set up Git repository: {str(e)}"
