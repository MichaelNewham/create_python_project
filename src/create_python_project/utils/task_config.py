#!/usr/bin/env python3
"""
Task Configuration Generator

Generates VS Code/Cursor tasks.json based on project configuration.
"""

from typing import Any


def generate_tasks_json(
    project_type: str, tech_stack: dict[str, str]
) -> dict[str, Any]:
    """Create tasks.json appropriate for the project type and tech stack."""

    # Base tasks for all Python projects
    base_tasks: list[dict[str, Any]] = [
        {
            "label": "Install Dependencies",
            "type": "shell",
            "command": "poetry install --with dev",
            "group": "build",
            "problemMatcher": [],
        },
        {
            "label": "Format Code",
            "type": "shell",
            "command": "poetry run black src/ && poetry run ruff check --fix src/",
            "group": "build",
            "problemMatcher": [],
        },
        {
            "label": "Run Tests",
            "type": "shell",
            "command": "poetry run pytest",
            "group": {"kind": "test", "isDefault": True},
            "problemMatcher": [],
        },
        {
            "label": "Type Check",
            "type": "shell",
            "command": "poetry run mypy src/",
            "group": "test",
            "problemMatcher": [],
        },
        {
            "label": "Test Coverage",
            "type": "shell",
            "command": "poetry run pytest --cov=src --cov-report=html",
            "group": "test",
            "problemMatcher": [],
        },
    ]

    # Add project-specific tasks
    if project_type == "web":
        web_tasks = _get_web_tasks(tech_stack)
        base_tasks.extend(web_tasks)
    elif project_type == "cli":
        cli_tasks = _get_cli_tasks()
        base_tasks.extend(cli_tasks)
    elif project_type == "api":
        api_tasks = _get_api_tasks(tech_stack)
        base_tasks.extend(api_tasks)
    elif project_type == "data":
        data_tasks = _get_data_tasks()
        base_tasks.extend(data_tasks)

    return {"version": "2.0.0", "tasks": base_tasks, "inputs": _get_task_inputs()}


def _get_web_tasks(tech_stack: dict[str, str]) -> list[dict[str, Any]]:
    """Get web development specific tasks."""
    tasks = []

    # Django tasks
    if tech_stack.get("Backend Framework") == "Django":
        tasks.extend(
            [
                {
                    "label": "Run Django Server",
                    "type": "shell",
                    "command": "poetry run python manage.py runserver",
                    "group": "build",
                    "problemMatcher": [],
                    "options": {"cwd": "${workspaceFolder}"},
                },
                {
                    "label": "Django Migrations",
                    "type": "shell",
                    "command": "poetry run python manage.py makemigrations && poetry run python manage.py migrate",
                    "group": "build",
                    "problemMatcher": [],
                },
                {
                    "label": "Create Django Superuser",
                    "type": "shell",
                    "command": "poetry run python manage.py createsuperuser",
                    "group": "build",
                    "problemMatcher": [],
                },
            ]
        )

    # React frontend tasks
    if tech_stack.get("Frontend") == "React":
        tasks.extend(
            [
                {
                    "label": "Install Frontend Dependencies",
                    "type": "shell",
                    "command": "npm install",
                    "options": {"cwd": "${workspaceFolder}/frontend"},
                    "group": "build",
                    "problemMatcher": [],
                },
                {
                    "label": "Run React Dev Server",
                    "type": "shell",
                    "command": "npm run dev",
                    "options": {"cwd": "${workspaceFolder}/frontend"},
                    "group": "build",
                    "problemMatcher": [],
                },
                {
                    "label": "Build React App",
                    "type": "shell",
                    "command": "npm run build",
                    "options": {"cwd": "${workspaceFolder}/frontend"},
                    "group": "build",
                    "problemMatcher": [],
                },
            ]
        )

    return tasks


def _get_cli_tasks() -> list[dict[str, Any]]:
    """Get CLI application specific tasks."""
    return [
        {
            "label": "Run CLI App",
            "type": "shell",
            "command": "poetry run python -m ${workspaceFolderBasename}",
            "group": "build",
            "problemMatcher": [],
        },
        {
            "label": "CLI Help",
            "type": "shell",
            "command": "poetry run python -m ${workspaceFolderBasename} --help",
            "group": "build",
            "problemMatcher": [],
        },
    ]


def _get_api_tasks(tech_stack: dict[str, str]) -> list[dict[str, Any]]:
    """Get API development specific tasks."""
    tasks = []

    if tech_stack.get("API Framework") == "FastAPI":
        tasks.extend(
            [
                {
                    "label": "Run FastAPI Server",
                    "type": "shell",
                    "command": "poetry run uvicorn main:app --reload",
                    "group": "build",
                    "problemMatcher": [],
                },
                {
                    "label": "Generate OpenAPI Schema",
                    "type": "shell",
                    "command": 'poetry run python -c "import json; from main import app; print(json.dumps(app.openapi(), indent=2))" > openapi.json',
                    "group": "build",
                    "problemMatcher": [],
                },
            ]
        )

    return tasks


def _get_data_tasks() -> list[dict[str, Any]]:
    """Get data science specific tasks."""
    return [
        {
            "label": "Start Jupyter Lab",
            "type": "shell",
            "command": "poetry run jupyter lab",
            "group": "build",
            "problemMatcher": [],
        },
        {
            "label": "Run Analysis Script",
            "type": "shell",
            "command": "poetry run python src/${workspaceFolderBasename}/analysis.py",
            "group": "build",
            "problemMatcher": [],
        },
    ]


def _get_task_inputs() -> list[dict[str, Any]]:
    """Get input definitions for tasks."""
    return [
        {
            "id": "commitMessage",
            "description": "Commit message",
            "default": "Update project files",
            "type": "promptString",
        }
    ]
