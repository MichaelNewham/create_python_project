#!/usr/bin/env python3
"""
IDE Configuration Manager

This module manages IDE-specific configurations for VS Code and Cursor.
Creates appropriate settings, tasks, extensions, and MCP configurations.
"""

import json
import os
import shutil
from typing import Any


class IDEConfigManager:
    """Manages IDE-specific configurations for VS Code and Cursor."""

    def __init__(
        self,
        project_dir: str,
        project_name: str,
        project_type: str,
        tech_stack: dict[str, Any],
    ):
        self.project_dir = project_dir
        self.project_name = project_name
        self.project_type = project_type
        self.tech_stack = tech_stack
        self.package_name = project_name.replace("-", "_").replace(" ", "_").lower()

    def create_vscode_config(self) -> bool:
        """Create complete .vscode folder with all configurations."""
        vscode_dir = os.path.join(self.project_dir, ".vscode")
        os.makedirs(vscode_dir, exist_ok=True)

        try:
            self._create_settings_json(vscode_dir)
            self._create_tasks_json(vscode_dir)
            self._create_extensions_json(vscode_dir)
            self._create_launch_json(vscode_dir)
            self._create_mcp_template(vscode_dir)
            return True
        except Exception as e:
            print(f"Error creating VS Code configuration: {e}")
            return False

    def create_cursor_config(self) -> bool:
        """Create .cursor folder mirroring .vscode with Cursor-specific additions."""
        cursor_dir = os.path.join(self.project_dir, ".cursor")
        os.makedirs(cursor_dir, exist_ok=True)

        try:
            # Copy VS Code configurations to Cursor
            self._copy_vscode_to_cursor()

            # Add Cursor-specific files
            rules_dir = os.path.join(cursor_dir, "rules")
            os.makedirs(rules_dir, exist_ok=True)
            self._create_cursor_instructions(rules_dir)

            return True
        except Exception as e:
            print(f"Error creating Cursor configuration: {e}")
            return False

    def _create_settings_json(self, config_dir: str):
        """Create VS Code settings.json with project-specific configurations."""
        settings = {
            "python.defaultInterpreterPath": "./.venv/bin/python",
            "python.terminal.activateEnvironment": True,
            "python.linting.enabled": True,
            "python.linting.pylintEnabled": False,
            "python.linting.flake8Enabled": False,
            "python.formatting.provider": "black",
            "python.testing.pytestEnabled": True,
            "python.testing.unittestEnabled": False,
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.organizeImports": "explicit",
                "source.fixAll.ruff": "explicit",
            },
            "files.exclude": {
                "**/__pycache__": True,
                "**/*.pyc": True,
                "**/.pytest_cache": True,
                "**/.mypy_cache": True,
                "**/.ruff_cache": True,
                "**/htmlcov": True,
                "**/.coverage": True,
            },
            "mcp.envFile": "${workspaceFolder}/.env",
        }

        # Add project-type specific settings
        if self.project_type == "web":
            settings.update(
                {
                    "emmet.includeLanguages": {"django-html": "html"},
                    "files.associations": {"**/*.html": "django-html"},
                }
            )

            # Add React-specific settings if frontend is React
            if self._get_tech_choice("Frontend") == "React":
                settings.update(
                    {
                        "typescript.preferences.includePackageJsonAutoImports": "auto",
                        "javascript.preferences.includePackageJsonAutoImports": "auto",
                    }
                )

        elif self.project_type == "data":
            settings.update(
                {
                    "jupyter.askForKernelRestart": False,
                    "jupyter.interactiveWindowMode": "perFile",
                }
            )

        settings_path = os.path.join(config_dir, "settings.json")
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)

    def _create_tasks_json(self, config_dir: str):
        """Create tasks.json with project-specific tasks."""
        from .task_config import generate_tasks_json

        tasks = generate_tasks_json(self.project_type, self._extract_tech_choices())

        tasks_path = os.path.join(config_dir, "tasks.json")
        with open(tasks_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)

    def _create_extensions_json(self, config_dir: str):
        """Create extensions.json with recommended extensions."""
        from .extension_config import get_extensions_for_project

        extensions = get_extensions_for_project(
            self.project_type, self._extract_tech_choices()
        )

        extensions_config = {"recommendations": extensions}

        extensions_path = os.path.join(config_dir, "extensions.json")
        with open(extensions_path, "w", encoding="utf-8") as f:
            json.dump(extensions_config, f, indent=2)

    def _create_launch_json(self, config_dir: str):
        """Create launch.json for debugging configurations."""
        configurations = [
            {
                "name": f"Run {self.project_name}",
                "type": "python",
                "request": "launch",
                "module": self.package_name,
                "console": "integratedTerminal",
                "justMyCode": True,
                "env": {"PYTHONPATH": "${workspaceFolder}"},
            }
        ]

        # Add project-specific debug configurations
        if self.project_type == "web":
            configurations.append(
                {
                    "name": "Django Debug",
                    "type": "python",
                    "request": "launch",
                    "program": "${workspaceFolder}/manage.py",
                    "args": ["runserver", "0.0.0.0:8000"],
                    "django": True,
                    "console": "integratedTerminal",
                    "justMyCode": True,
                }
            )

        elif self.project_type == "cli":
            configurations.append(
                {
                    "name": "CLI with Arguments",
                    "type": "python",
                    "request": "launch",
                    "module": self.package_name,
                    "console": "integratedTerminal",
                    "args": ["--help"],
                    "justMyCode": True,
                }
            )

        launch_config = {"version": "0.2.0", "configurations": configurations}

        launch_path = os.path.join(config_dir, "launch.json")
        with open(launch_path, "w", encoding="utf-8") as f:
            json.dump(launch_config, f, indent=2)

    def _create_mcp_template(self, config_dir: str):
        """Create MCP configuration templates."""
        from .mcp_config import get_mcp_servers_for_project

        mcp_config = get_mcp_servers_for_project(
            self.project_type, self._extract_tech_choices()
        )

        # Create mcp.json.template (without sensitive data)
        template_path = os.path.join(config_dir, "mcp.json.template")
        with open(template_path, "w", encoding="utf-8") as f:
            json.dump(mcp_config, f, indent=2)

        # Create actual mcp.json (will be gitignored)
        mcp_path = os.path.join(config_dir, "mcp.json")
        with open(mcp_path, "w", encoding="utf-8") as f:
            json.dump(mcp_config, f, indent=2)

    def _copy_vscode_to_cursor(self):
        """Copy VS Code configurations to Cursor directory."""
        vscode_dir = os.path.join(self.project_dir, ".vscode")
        cursor_dir = os.path.join(self.project_dir, ".cursor")

        if os.path.exists(vscode_dir):
            for file_name in os.listdir(vscode_dir):
                if file_name.endswith(".json"):
                    src = os.path.join(vscode_dir, file_name)
                    dst = os.path.join(cursor_dir, file_name)
                    shutil.copy2(src, dst)

    def _create_cursor_instructions(self, rules_dir: str):
        """Create Cursor-specific instruction files."""

        # Main instructions file
        instructions_content = f"""# {self.project_name} - Cursor Instructions

## Project Overview
{self.project_type.capitalize()} project created with Create Python Project tool.

## Technology Stack
{self._format_tech_stack()}

## Development Guidelines
- Use Poetry for dependency management
- Follow PEP 8 style guidelines with Black formatting
- Write tests for all new functionality
- Use type hints throughout the codebase
- Keep functions focused and well-documented

## Project Structure
- `src/{self.package_name}/`: Main package source code
- `tests/`: Test files mirroring source structure
- `docs/`: Project documentation
- `scripts/`: Development and deployment scripts

## Common Tasks
- Install dependencies: `poetry install`
- Run tests: `poetry run pytest`
- Format code: `poetry run black src/`
- Type check: `poetry run mypy src/`
"""

        instructions_path = os.path.join(rules_dir, "instructions.md")
        with open(instructions_path, "w", encoding="utf-8") as f:
            f.write(instructions_content)

        # Project-specific rules
        if self.project_type == "web":
            web_rules = """
## Web Development Specific

### Django Guidelines
- Use class-based views for complex logic
- Keep models focused and normalized
- Write custom managers for complex queries
- Use Django's built-in authentication system

### API Development
- Return consistent JSON responses
- Implement proper error handling
- Use DRF serializers for validation
- Add comprehensive API documentation
"""
            with open(
                os.path.join(rules_dir, "web_rules.md"), "w", encoding="utf-8"
            ) as f:
                f.write(web_rules)

    def _extract_tech_choices(self) -> dict[str, str]:
        """Extract technology choices from tech_stack for easier access."""
        choices = {}

        if isinstance(self.tech_stack, dict) and "categories" in self.tech_stack:
            for category in self.tech_stack["categories"]:
                for option in category.get("options", []):
                    if option.get("recommended", False):
                        choices[category["name"]] = option["name"]

        return choices

    def _get_tech_choice(self, category_name: str) -> str:
        """Get the chosen technology for a specific category."""
        return self._extract_tech_choices().get(category_name, "")

    def _format_tech_stack(self) -> str:
        """Format technology stack for documentation."""
        choices = self._extract_tech_choices()
        if not choices:
            return "Standard Python project configuration"

        lines = []
        for category, tech in choices.items():
            lines.append(f"- **{category}**: {tech}")

        return "\n".join(lines)
