#!/usr/bin/env python3
"""
Workspace Configuration Module

Generates VS Code .code-workspace files for easy project opening.
"""

import json
import os
from typing import Any


def create_workspace_file(
    project_dir: str, project_name: str, project_type: str, tech_stack: dict[str, Any]
) -> tuple[bool, str]:
    """Create a comprehensive VS Code workspace file."""
    try:
        workspace_config = {
            "folders": _get_workspace_folders(project_dir, project_name, tech_stack),
            "settings": _get_workspace_settings(project_type, tech_stack),
            "extensions": _get_workspace_extensions(project_type, tech_stack),
            "tasks": _get_workspace_tasks(project_type, tech_stack),
            "launch": _get_workspace_launch_configs(
                project_name, project_type, tech_stack
            ),
        }

        workspace_file = os.path.join(project_dir, f"{project_name}.code-workspace")
        with open(workspace_file, "w", encoding="utf-8") as f:
            json.dump(workspace_config, f, indent=2)

        return True, f"Workspace file created: {workspace_file}"
    except Exception as e:
        return False, f"Failed to create workspace file: {str(e)}"


def _get_workspace_folders(
    project_dir: str, project_name: str, tech_stack: dict[str, Any]
) -> list[dict[str, str]]:
    """Get workspace folder configuration."""
    folders = [
        {"name": project_name.replace("_", " ").replace("-", " ").title(), "path": "."}
    ]

    # Add backend/frontend folders for web projects
    backend_framework = _extract_tech_choice(tech_stack, "Backend Framework")
    frontend_framework = _extract_tech_choice(tech_stack, "Frontend")

    if backend_framework in ["Django", "Flask"]:
        folders.append({"name": "Backend", "path": "./backend"})

    if frontend_framework and "React" in frontend_framework:
        folders.append({"name": "Frontend", "path": "./frontend"})

    # Add common project folders
    folders.extend(
        [
            {"name": "Tests", "path": "./tests"},
            {"name": "Scripts", "path": "./scripts"},
            {"name": "Documentation", "path": "./docs"},
        ]
    )

    # Add data science specific folders
    if "data" in str(tech_stack).lower():
        folders.extend(
            [
                {"name": "Data", "path": "./data"},
                {"name": "Notebooks", "path": "./notebooks"},
            ]
        )

    return folders


def _get_workspace_settings(
    project_type: str, tech_stack: dict[str, Any]
) -> dict[str, Any]:
    """Get workspace-specific settings."""
    settings = {
        # Python configuration
        "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
        "python.terminal.activateEnvironment": True,
        "python.testing.pytestEnabled": True,
        "python.testing.unittestEnabled": False,
        "python.analysis.extraPaths": ["${workspaceFolder}/src"],
        # Editor configuration
        "editor.formatOnSave": True,
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit",
            "source.fixAll.ruff": "explicit",
        },
        "editor.rulers": [88],
        # Language-specific formatting
        "[python]": {
            "editor.defaultFormatter": "ms-python.black-formatter",
            "editor.insertSpaces": True,
            "editor.tabSize": 4,
        },
        "[json]": {"editor.defaultFormatter": "esbenp.prettier-vscode"},
        "[yaml]": {"editor.defaultFormatter": "esbenp.prettier-vscode"},
        # File exclusions
        "files.exclude": {
            "**/__pycache__": True,
            "**/*.pyc": True,
            ".mypy_cache": True,
            ".pytest_cache": True,
            ".ruff_cache": True,
            "htmlcov": True,
            ".coverage": True,
            "node_modules": True,
            ".venv": True,
        },
        # Search exclusions
        "search.exclude": {
            "**/node_modules": True,
            "**/.venv": True,
            "**/htmlcov": True,
            "**/.mypy_cache": True,
            "**/.pytest_cache": True,
            "**/.ruff_cache": True,
        },
        # MCP configuration
        "mcp.envFile": "${workspaceFolder}/.env",
        "mcp.secretsFile": "${workspaceFolder}/.vscode/mcp-secrets.json",
    }

    # Add project-type specific settings
    if project_type == "web":
        backend = _extract_tech_choice(tech_stack, "Backend Framework")
        if backend == "Django":
            settings.update(
                {
                    "python.envFile": "${workspaceFolder}/backend/.env",
                    "django.managePyPath": "${workspaceFolder}/backend/manage.py",
                    "emmet.includeLanguages": {"django-html": "html"},
                    "files.associations": {"**/*.html": "django-html"},
                }
            )

        frontend = _extract_tech_choice(tech_stack, "Frontend")
        if frontend and "React" in frontend:
            settings.update(
                {
                    "typescript.preferences.includePackageJsonAutoImports": "auto",
                    "javascript.preferences.includePackageJsonAutoImports": "auto",
                    "emmet.includeLanguages": {"javascript": "javascriptreact"},
                }
            )

    elif project_type == "data":
        settings.update(
            {
                "jupyter.askForKernelRestart": False,
                "jupyter.interactiveWindowMode": "perFile",
                "python.dataScience.enableCellCodeLens": True,
                "notebook.cellToolbarLocation": {
                    "default": "right",
                    "jupyter-notebook": "left",
                },
            }
        )

    return settings


def _get_workspace_extensions(
    project_type: str, tech_stack: dict[str, Any]
) -> dict[str, list[str]]:
    """Get recommended extensions for the workspace."""
    base_extensions = [
        # Python essentials
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "charliermarsh.ruff",
        # Development tools
        "njpwerner.autodocstring",
        "ms-python.debugpy",
        "GitHub.copilot",
        "GitHub.copilot-chat",
        "eamodio.gitlens",
        # Code quality
        "streetsidesoftware.code-spell-checker",
        "tamasfe.even-better-toml",
        "redhat.vscode-yaml",
        # MCP and AI
        "f1e.mcp",
    ]

    # Add project-type specific extensions
    if project_type == "web":
        backend = _extract_tech_choice(tech_stack, "Backend Framework")
        if backend == "Django":
            base_extensions.extend(["batisteo.vscode-django", "wholroyd.jinja"])
        elif backend == "Flask":
            base_extensions.extend(["wholroyd.jinja", "alexcvzz.vscode-flask-snippets"])

        frontend = _extract_tech_choice(tech_stack, "Frontend")
        if frontend and "React" in frontend:
            base_extensions.extend(
                [
                    "dsznajder.es7-react-js-snippets",
                    "dbaeumer.vscode-eslint",
                    "esbenp.prettier-vscode",
                    "bradlc.vscode-tailwindcss",
                    "formulahendry.auto-rename-tag",
                ]
            )

            if "TypeScript" in frontend:
                base_extensions.append("ms-vscode.vscode-typescript-next")

    elif project_type == "data":
        base_extensions.extend(
            [
                "ms-toolsai.jupyter",
                "ms-python.vscode-jupyter-cell-tags",
                "mechatroner.rainbow-csv",
                "randomfractalsinc.vscode-data-preview",
            ]
        )

    elif project_type == "api":
        base_extensions.extend(
            [
                "humao.rest-client",
                "42crunch.vscode-openapi",
                "rangav.vscode-thunder-client",
            ]
        )

    # Add database-specific extensions
    database = _extract_tech_choice(tech_stack, "Database")
    if database == "PostgreSQL":
        base_extensions.append("ckolkman.vscode-postgres")
    elif database == "MongoDB":
        base_extensions.append("mongodb.mongodb-vscode")

    # Add Docker extension if needed
    if "Docker" in str(tech_stack):
        base_extensions.append("ms-azuretools.vscode-docker")

    return {"recommendations": base_extensions}


def _get_workspace_tasks(
    project_type: str, tech_stack: dict[str, Any]
) -> dict[str, str]:
    """Get task configuration reference."""
    return {"version": "2.0.0", "tasks": "${workspaceFolder}/.vscode/tasks.json"}


def _get_workspace_launch_configs(
    project_name: str, project_type: str, tech_stack: dict[str, Any]
) -> dict[str, Any]:
    """Get debug launch configurations."""
    package_name = project_name.replace("-", "_").replace(" ", "_").lower()

    configurations = [
        {
            "name": f"Run {project_name}",
            "type": "python",
            "request": "launch",
            "module": package_name,
            "console": "integratedTerminal",
            "justMyCode": True,
            "env": {"PYTHONPATH": "${workspaceFolder}/src"},
        }
    ]

    # Add project-specific debug configurations
    if project_type == "web":
        backend = _extract_tech_choice(tech_stack, "Backend Framework")
        if backend == "Django":
            configurations.append(
                {
                    "name": "Django Debug Server",
                    "type": "python",
                    "request": "launch",
                    "program": "${workspaceFolder}/backend/manage.py",
                    "args": ["runserver", "0.0.0.0:8000"],
                    "django": True,
                    "console": "integratedTerminal",
                    "justMyCode": True,
                }
            )
        elif backend == "FastAPI":
            configurations.append(
                {
                    "name": "FastAPI Debug Server",
                    "type": "python",
                    "request": "launch",
                    "module": "uvicorn",
                    "args": [
                        f"src.{package_name}.main:app",
                        "--reload",
                        "--host",
                        "0.0.0.0",
                        "--port",
                        "8000",
                    ],
                    "console": "integratedTerminal",
                    "justMyCode": True,
                }
            )

    elif project_type == "cli":
        configurations.append(
            {
                "name": "CLI with Arguments",
                "type": "python",
                "request": "launch",
                "module": package_name,
                "args": ["--help"],
                "console": "integratedTerminal",
                "justMyCode": True,
            }
        )

    elif project_type == "data":
        configurations.append(
            {
                "name": "Run Analysis",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/src/" + package_name + "/analysis.py",
                "console": "integratedTerminal",
                "justMyCode": True,
            }
        )

    return {"version": "0.2.0", "configurations": configurations}


def _extract_tech_choice(tech_stack: dict[str, Any], category_name: str) -> str:
    """Extract the recommended technology for a given category."""
    if isinstance(tech_stack, dict) and "categories" in tech_stack:
        for category in tech_stack["categories"]:
            if category.get("name") == category_name:
                for option in category.get("options", []):
                    if option.get("recommended", False):
                        return str(option["name"])
    return ""
