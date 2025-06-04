#!/usr/bin/env python3
"""
Configuration Module

This module handles configuration for the Create Python Project application.
It manages .env files, project-specific settings, and default configurations.
Also provides dynamic dependency management based on AI recommendations.
"""

import os
from typing import Any


def load_env_file(env_file: str = ".env") -> dict[str, str]:
    """
    Load environment variables from a .env file.

    Args:
        env_file: Path to the .env file

    Returns:
        Dictionary containing environment variables
    """
    env_vars: dict[str, str] = {}

    if not os.path.exists(env_file):
        return env_vars

    try:
        with open(env_file, encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                # Parse key-value pairs
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    # Remove quotes if present
                    if (value.startswith('"') and value.endswith('"')) or (
                        value.startswith("'") and value.endswith("'")
                    ):
                        value = value[1:-1]

                    env_vars[key] = value

        return env_vars
    except Exception as e:
        print(f"Error loading .env file: {str(e)}")
        return {}


def create_env_file(project_dir: str, variables: dict[str, str]) -> tuple[bool, str]:
    """
    Create a .env file in the project directory.

    Args:
        project_dir: The project directory
        variables: Dictionary of environment variables

    Returns:
        Tuple containing success status and message
    """
    try:
        env_file_path = os.path.join(project_dir, ".env")

        with open(env_file_path, "w", encoding="utf-8") as file:
            file.write("# Environment variables for the project\n\n")

            for key, value in variables.items():
                # Check if value needs quotes
                if " " in value or "\n" in value or "\t" in value:
                    value = f'"{value}"'

                file.write(f"{key}={value}\n")

        # Create a .env.example file without sensitive values
        example_path = os.path.join(project_dir, ".env.example")
        with open(example_path, "w", encoding="utf-8") as file:
            file.write("# Example environment variables for the project\n")
            file.write("# Copy this file to .env and fill in the values\n\n")

            for key in variables:
                file.write(f"{key}=\n")

        # Add both files to .gitignore
        gitignore_path = os.path.join(project_dir, ".gitignore")

        # Check if .gitignore exists and if .env is already in it
        gitignore_content = ""
        if os.path.exists(gitignore_path):
            with open(gitignore_path, encoding="utf-8") as file:
                gitignore_content = file.read()

        # Add .env to .gitignore if not already present
        updated = False
        if ".env" not in gitignore_content:
            with open(gitignore_path, "a", encoding="utf-8") as file:
                if not gitignore_content.endswith("\n"):
                    file.write("\n")
                file.write("\n# Environment variables\n.env\n")
                updated = True

        return True, f"Created .env file at {env_file_path}" + (
            " and updated .gitignore" if updated else ""
        )

    except Exception as e:
        return False, f"Failed to create .env file: {str(e)}"


def get_project_dependencies(
    project_type: str, tech_stack: dict[str, Any] | None = None
) -> dict[str, list[str]]:
    """
    Get project dependencies based on project type and AI recommendations.

    This function dynamically determines project dependencies by analyzing the
    tech stack recommended by AI, falling back to defaults if no tech stack is provided.

    Args:
        project_type: The type of project (web, cli, data, etc.)
        tech_stack: Optional dictionary containing AI-recommended technologies

    Returns:
        Dictionary containing main and development dependencies
    """
    # Initialize dependency structure
    dependencies: dict[str, list[str]] = {
        "main": [],
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "mypy",
            "ruff",
            "pre-commit",
        ],
    }

    # Default dependencies by project type
    default_dependencies: dict[str, list[str]] = {
        "cli": ["click", "rich", "typer"],
        "web": ["flask", "gunicorn", "requests"],
        "api": ["fastapi", "uvicorn", "pydantic"],
        "data": ["pandas", "matplotlib", "jupyter"],
        "ai": ["scikit-learn", "tensorflow", "pandas"],
        "gui": ["pyside6", "pyqt6"],
        # Add other project types as needed
    }

    # Try to extract dependencies from tech stack if provided
    if tech_stack and isinstance(tech_stack, dict):
        extracted_deps = _extract_dependencies_from_tech_stack(tech_stack)
        if extracted_deps:
            dependencies["main"].extend(extracted_deps)
        else:
            # Fall back to defaults if tech stack didn't yield dependencies
            if project_type in default_dependencies:
                dependencies["main"].extend(default_dependencies[project_type])
    else:
        # Use defaults when no tech stack is provided
        if project_type in default_dependencies:
            dependencies["main"].extend(default_dependencies[project_type])

    # Ensure list items are unique
    dependencies["main"] = list(set(dependencies["main"]))
    dependencies["dev"] = list(set(dependencies["dev"]))

    return dependencies


def _extract_dependencies_from_tech_stack(tech_stack: dict[str, Any]) -> list[str]:
    """
    Extract Python dependencies from the AI-recommended tech stack.

    Args:
        tech_stack: Dictionary containing AI technology recommendations

    Returns:
        List of Python package dependencies
    """
    dependencies: list[str] = []

    # Check if we have the expected structure
    if not isinstance(tech_stack, dict) or "categories" not in tech_stack:
        return dependencies

    # Map common technology names to Python packages
    tech_to_package = {
        # Web frameworks
        "Flask": "flask",
        "Django": "django",
        "FastAPI": "fastapi",
        # Databases
        "PostgreSQL": "psycopg2-binary",
        "MongoDB": "pymongo",
        "SQLite": "sqlite3",  # Built-in, but added for completeness
        "Redis": "redis",
        # Authentication
        "PyJWT": "pyjwt",
        "OAuth": "authlib",
        "Passlib": "passlib",
        # Frontend
        "React": "react",  # This would be via npm, but included for mapping
        "Vue.js": "vue",  # This would be via npm, but included for mapping
        # Data processing
        "Pandas": "pandas",
        "NumPy": "numpy",
        "Matplotlib": "matplotlib",
        "Jupyter": "jupyter",
        # AI/ML
        "TensorFlow": "tensorflow",
        "PyTorch": "torch",
        "Scikit-learn": "scikit-learn",
        # CLI
        "Click": "click",
        "Typer": "typer",
        "ArgParse": "argparse",  # Built-in, but added for completeness
        # Utilities
        "Requests": "requests",
        "Beautiful Soup": "beautifulsoup4",
        "Celery": "celery",
    }

    # Examine each category and extract recommended technologies
    for category in tech_stack["categories"]:
        if "options" not in category:
            continue

        for option in category["options"]:
            # Check if this option is recommended
            if option.get("recommended", False):
                tech_name = option.get("name", "")

                # Add the corresponding Python package if we have a mapping
                if tech_name in tech_to_package:
                    dependencies.append(tech_to_package[tech_name])

                # Some technologies imply additional dependencies
                if tech_name == "FastAPI":
                    dependencies.append("uvicorn")
                    dependencies.append("pydantic")
                elif tech_name == "Django":
                    dependencies.append("django-environ")
                    dependencies.append("gunicorn")

    # Return unique dependencies
    return list(set(dependencies))


def get_project_types() -> dict[str, dict[str, str]]:
    """
    Get the available project types and their configurations.

    Returns:
        Dictionary mapping project types to their configurations
    """
    return {
        # Application Types
        "cli": {
            "name": "Command-Line Interface",
            "description": "Terminal tools and scripts for automation",
        },
        "web": {
            "name": "Web Application",
            "description": "Browser-based interfaces and full-stack applications",
        },
        "mobile-backend": {
            "name": "Mobile Backend",
            "description": "Server-side services specifically for mobile applications",
        },
        "gui": {
            "name": "Desktop GUI",
            "description": "Native desktop applications with graphical interfaces",
        },
        # Service Types
        "api": {
            "name": "API Service",
            "description": "RESTful/GraphQL endpoints for general consumption",
        },
        "microservice": {
            "name": "Microservice",
            "description": "Single-responsibility service in distributed architecture",
        },
        # Analysis Types
        "data": {
            "name": "Data Analysis",
            "description": "Data processing, analytics, and scientific computing",
        },
        "ai": {
            "name": "AI/ML Project",
            "description": "Machine learning models and AI applications",
        },
        # Development Types
        "library": {
            "name": "Library/SDK",
            "description": "Reusable packages and tools for other developers",
        },
        "automation": {
            "name": "Automation Tool",
            "description": "Workflow automation, bots, and system integration",
        },
    }
