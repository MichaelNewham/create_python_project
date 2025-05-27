#!/usr/bin/env python3
# mypy: disable-error-code="name-defined"
"""
Core Project Builder Module

This module contains the core functionality for creating Python projects.
It handles file creation, directory structure, and template rendering.
"""

import os
import shutil
import subprocess
from typing import Any


def create_project_structure(
    project_name: str,
    project_dir: str,
    project_type: str,
    with_ai: bool = True,
    tech_stack: dict[Any, Any] | None = None,
    **kwargs: Any,
) -> tuple[bool, str]:
    """
    Create the base project structure.

    Args:
        project_name: Name of the project
        project_dir: Directory where the project should be created
        project_type: Type of the project (web, cli, etc.)
        with_ai: Whether to include AI integration
        tech_stack: Dictionary containing AI-recommended technology stack
        **kwargs: Additional parameters for project creation

    Returns:
        Tuple containing success status and message
    """
    try:
        tech_stack = tech_stack or {}
        package_name = project_name.replace("-", "_").replace(" ", "_").lower()

        # Create project directory if it doesn't exist
        os.makedirs(project_dir, exist_ok=True)

        # Create package directory
        package_dir = os.path.join(project_dir, "src", package_name)
        os.makedirs(package_dir, exist_ok=True)

        # Create data analysis module for data projects
        if project_type == "data":
            # Create data-specific directories
            data_dir = os.path.join(package_dir, "data")
            notebooks_dir = os.path.join(project_dir, "notebooks")
            os.makedirs(data_dir, exist_ok=True)
            os.makedirs(notebooks_dir, exist_ok=True)

            # Create data analysis module
            data_file = os.path.join(package_dir, "analysis.py")
            with open(data_file, "w", encoding="utf-8") as file:
                file.write(
                    f'''"""Data analysis module for {project_name}."""

import os
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Any, Tuple

def load_data(file_path: str) -> pd.DataFrame:
    """Load data from a file into a pandas DataFrame."""
    _, file_ext = os.path.splitext(file_path)

    if file_ext.lower() == '.csv':
        return pd.read_csv(file_path)
    elif file_ext.lower() in ['.xls', '.xlsx']:
        return pd.read_excel(file_path)
    elif file_ext.lower() == '.json':
        return pd.read_json(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {file_ext}")

def analyze_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Perform basic data analysis."""
    results = {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "summary": df.describe().to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
    }
    return results

def visualize_data(df: pd.DataFrame, column: str, output_path: str = None) -> None:
    """Create a simple visualization for a column."""
    plt.figure(figsize=(10, 6))

    # Use the column parameter directly
    if pd.api.types.is_numeric_dtype(df[column]):  # type: ignore
        df[column].hist()  # type: ignore
        plt.title(f"Histogram of {column}")
    else:
        df[column].value_counts().plot(kind='bar')  # type: ignore
        plt.title(f"Value counts of {column}")

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path)
    else:
        plt.show()
'''
                )

            # Create a simple Jupyter notebook
            notebook_file = os.path.join(notebooks_dir, "data_exploration.ipynb")
            with open(notebook_file, "w", encoding="utf-8") as file:
                file.write(
                    """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Data Exploration Notebook"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\\n",
    "import matplotlib.pyplot as plt\\n",
    "import seaborn as sns\\n",
    "\\n",
    "# Set up plot styling\\n",
    "plt.style.use(\'ggplot\')\\n",
    "sns.set_theme()\\n",
    "%matplotlib inline"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Loading Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# TODO: Load your data\\n",
    "# df = pd.read_csv(\'data/your_data.csv\')\\n",
    "# df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Data Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# TODO: Analyze your data\\n",
    "# df.describe()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Data Visualization"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# TODO: Visualize your data\\n",
    "# plt.figure(figsize=(10, 6))\\n",
    "# sns.histplot(df[\'column_name\'])\\n",
    "# plt.title(\'Histogram of Column\')\\n",
    "# plt.show()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}"""
                )

        # Create utils directory in the project package
        utils_dir = os.path.join(package_dir, "utils")
        os.makedirs(utils_dir, exist_ok=True)
        with open(
            os.path.join(utils_dir, "__init__.py"), "w", encoding="utf-8"
        ) as file:
            file.write('"""Utility functions for the project."""\n')

        return True, f"Project structure created at {project_dir}"

    except Exception as e:
        return False, f"Failed to create project structure: {str(e)}"


def setup_virtual_environment(project_dir: str) -> tuple[bool, str]:
    """
    Set up a virtual environment using Poetry.

    Args:
        project_dir: The project directory where the dependencies should be installed

    Returns:
        Tuple containing success status and message
    """
    try:
        # Check if Poetry is installed
        if not shutil.which("poetry"):
            return False, "Poetry is not installed. Please install Poetry first."

        # Initialize Poetry project
        subprocess.run(
            ["poetry", "init", "--no-interaction"], cwd=project_dir, check=True
        )

        return True, "Virtual environment created successfully"

    except subprocess.CalledProcessError as e:
        return False, f"Failed to create virtual environment: {str(e)}"


def initialize_git_repo(
    project_dir: str,
    project_name: str,
    github_username: str | None = None,
    gitlab_username: str | None = None,
    with_github_config: bool = False,
    project_description: str = "",
    project_type: str = "",
    tech_stack: dict[str, Any] | None = None,
) -> tuple[bool, str]:
    """
    Initialize a Git repository for the project.

    Args:
        project_dir: Directory where the project is located
        project_name: Name of the project
        github_username: GitHub username for remote setup (optional)
        gitlab_username: GitLab username for remote setup (optional)
        with_github_config: Whether to include GitHub specific configuration
        project_description: Project description for repository
        project_type: Type of the project (web, cli, etc.)
        tech_stack: Dictionary containing technology stack information

    Returns:
        Tuple containing success status and message
    """
    try:
        # Initialize git repository
        subprocess.run(
            ["git", "init"], cwd=project_dir, check=True, capture_output=True
        )

        # Create .gitignore
        gitignore_content = """
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

# Virtual Environment
.env
.venv
env/
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Logs
logs/
*.log

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/

# Jupyter Notebook
.ipynb_checkpoints
"""
        with open(os.path.join(project_dir, ".gitignore"), "w", encoding="utf-8") as f:
            f.write(gitignore_content)

        # Add GitHub specific configuration if requested
        if with_github_config:
            os.makedirs(os.path.join(project_dir, ".github"), exist_ok=True)

            # Create GitHub Copilot configuration
            copilot_config = {
                "project_type": project_type,
                "tech_stack": tech_stack or {},
                "description": project_description,
            }

            with open(
                os.path.join(project_dir, ".github", "copilot-config.json"),
                "w",
                encoding="utf-8",
            ) as f:
                import json

                json.dump(copilot_config, f, indent=2)

        # Initial commit
        subprocess.run(
            ["git", "add", "."], cwd=project_dir, check=True, capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            cwd=project_dir,
            check=True,
            capture_output=True,
        )

        # Configure remote repositories if usernames are provided
        remote_urls = []

        if github_username:
            github_url = f"git@github.com:{github_username}/{project_name}.git"
            remote_urls.append(("github", github_url))

        if gitlab_username:
            gitlab_url = f"git@gitlab.com:{gitlab_username}/{project_name}.git"
            remote_urls.append(("gitlab", gitlab_url))

        for remote_name, url in remote_urls:
            subprocess.run(
                ["git", "remote", "add", remote_name, url],
                cwd=project_dir,
                check=True,
                capture_output=True,
            )

        return True, "Git repository initialized successfully"

    except subprocess.CalledProcessError as e:
        return False, f"Failed to initialize Git repository: {e.stderr.decode()}"
    except Exception as e:
        return False, f"Failed to initialize Git repository: {str(e)}"
