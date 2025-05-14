#!/usr/bin/env python3
"""
Configuration Module

This module handles configuration for the Create Python Project application.
It manages .env files, project-specific settings, and default configurations.
"""

import os
from typing import Dict, Tuple


def load_env_file(env_file: str = ".env") -> Dict[str, str]:
    """
    Load environment variables from a .env file.

    Args:
        env_file: Path to the .env file

    Returns:
        Dictionary containing environment variables
    """
    env_vars: Dict[str, str] = {}

    if not os.path.exists(env_file):
        return env_vars

    try:
        with open(env_file, "r") as file:
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


def create_env_file(project_dir: str, variables: Dict[str, str]) -> Tuple[bool, str]:
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

        with open(env_file_path, "w") as file:
            file.write("# Environment variables for the project\n\n")

            for key, value in variables.items():
                # Check if value needs quotes
                if " " in value or "\n" in value or "\t" in value:
                    value = f'"{value}"'

                file.write(f"{key}={value}\n")

        # Create a .env.example file without sensitive values
        example_path = os.path.join(project_dir, ".env.example")
        with open(example_path, "w") as file:
            file.write("# Example environment variables for the project\n")
            file.write("# Copy this file to .env and fill in the values\n\n")

            for key in variables:
                file.write(f"{key}=\n")

        # Add both files to .gitignore
        gitignore_path = os.path.join(project_dir, ".gitignore")

        # Check if .gitignore exists and if .env is already in it
        gitignore_content = ""
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r") as file:
                gitignore_content = file.read()

        # Add .env to .gitignore if not already present
        updated = False
        if ".env" not in gitignore_content:
            with open(gitignore_path, "a") as file:
                if not gitignore_content.endswith("\n"):
                    file.write("\n")
                file.write("\n# Environment variables\n.env\n")
                updated = True

        return True, f"Created .env file at {env_file_path}" + (
            " and updated .gitignore" if updated else ""
        )

    except Exception as e:
        return False, f"Failed to create .env file: {str(e)}"


def get_project_types() -> Dict[str, Dict[str, str]]:
    """
    Get the available project types and their configurations.

    Returns:
        Dictionary mapping project types to their configurations
    """
    return {
        "basic": {
            "name": "Basic Python Package",
            "description": "A simple Python package with minimal structure",
        },
        "cli": {
            "name": "Command-Line Interface",
            "description": "A Python package with a command-line interface",
        },
        "web": {
            "name": "Web Application",
            "description": "A web application using Flask or FastAPI",
        },
        "api": {"name": "API Service", "description": "A RESTful API service"},
        "data": {
            "name": "Data Analysis/Science",
            "description": "A data analysis or data science project",
        },
        "ai": {
            "name": "AI/ML Project",
            "description": "An AI or machine learning project",
        },
        "gui": {"name": "GUI Application", "description": "A desktop GUI application"},
    }
