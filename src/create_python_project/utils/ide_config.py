#!/usr/bin/env python3
"""
IDE Configuration Manager

This module manages IDE-specific configurations for VS Code.
Creates appropriate settings, tasks, extensions, and MCP configurations.
"""

import json
import os
from typing import Any


class IDEConfigManager:
    """Manages IDE-specific configurations for VS Code."""

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
            self._create_keybindings_json(vscode_dir)
            self._create_mcp_template(vscode_dir)
            return True
        except Exception as e:
            print(f"Error creating VS Code configuration: {e}")
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

    def _create_keybindings_json(self, config_dir: str):
        """Create keybindings.json with project-specific shortcuts."""
        keybindings = [
            {
                "key": "ctrl+alt+r",
                "command": "workbench.action.tasks.runTask",
                "args": self._get_main_run_task(),
                "when": "editorFocus || terminalFocus",
            },
            {
                "key": "ctrl+alt+t",
                "command": "workbench.action.tasks.runTask",
                "args": "Run Tests",
                "when": "editorFocus || terminalFocus",
            },
            {
                "key": "ctrl+alt+f",
                "command": "workbench.action.tasks.runTask",
                "args": "Format Code",
                "when": "editorFocus || terminalFocus",
            },
        ]

        # Add project-specific shortcuts
        if self.project_type == "web":
            keybindings.append(
                {
                    "key": "ctrl+alt+s",
                    "command": "workbench.action.tasks.runTask",
                    "args": (
                        "Run Django Server"
                        if self._get_tech_choice("Backend Framework") == "Django"
                        else "Run Server"
                    ),
                    "when": "editorFocus || terminalFocus",
                }
            )
        elif self.project_type == "data":
            keybindings.append(
                {
                    "key": "ctrl+alt+j",
                    "command": "workbench.action.tasks.runTask",
                    "args": "Start Jupyter Lab",
                    "when": "editorFocus || terminalFocus",
                }
            )

        keybindings_path = os.path.join(config_dir, "keybindings.json")
        with open(keybindings_path, "w", encoding="utf-8") as f:
            json.dump(keybindings, f, indent=2)

    def _get_main_run_task(self) -> str:
        """Get the main run task name for this project type."""
        task_map = {
            "web": (
                "Run Django Server"
                if self._get_tech_choice("Backend Framework") == "Django"
                else "Run Server"
            ),
            "cli": "Run CLI App",
            "api": (
                "Run FastAPI Server"
                if self._get_tech_choice("API Framework") == "FastAPI"
                else "Run API Server"
            ),
            "data": "Start Jupyter Lab",
        }
        return task_map.get(self.project_type, "Run Tests")

    def _create_mcp_template(self, config_dir: str):
        """Create MCP configuration template only."""
        from .mcp_config import get_mcp_servers_for_project

        mcp_config = get_mcp_servers_for_project(
            self.project_type, self._extract_tech_choices()
        )

        # Create only mcp.json.template (without creating actual mcp.json)
        template_path = os.path.join(config_dir, "mcp.json.template")
        with open(template_path, "w", encoding="utf-8") as f:
            json.dump(mcp_config, f, indent=2)

        # Create MCP setup instructions
        readme_path = os.path.join(config_dir, "MCP_SETUP.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(
                """# MCP Server Setup Instructions

This project includes MCP (Model Context Protocol) server templates for enhanced AI development.

## Setup Steps

1. **Copy the template**: `cp mcp.json.template mcp.json`
2. **Update environment variables** in your .env file
3. **Install Node.js dependencies**: `npm install` (in project root)
4. **Restart VS Code** to activate MCP servers

## Configured Servers

The template includes servers for:
- **filesystem**: Browse and edit project files
- **github**: GitHub repository integration
- **context7**: Advanced context management

Additional project-specific servers may be included based on your tech stack.

## Important Notes

- The `mcp.json` file is gitignored to prevent sharing sensitive configurations
- MCP servers require active environment variables from your .env file
- Each project should have its own MCP configuration tailored to its needs

## Troubleshooting

If MCP servers aren't working:
1. Check that Node.js packages are installed
2. Verify environment variables are set in .env
3. Restart VS Code completely
4. Check VS Code output panel for MCP errors
"""
            )

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
