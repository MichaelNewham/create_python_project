#!/usr/bin/env python3
"""
Task Configuration Generator - REFACTORED

Generates VS Code/Cursor tasks.json with complete development workflow tasks.
Now includes all essential tasks and is driven by AI recommendations.
"""

from typing import Any


def generate_tasks_json(
    project_type: str, tech_stack: dict[str, str]
) -> dict[str, Any]:
    """Create comprehensive tasks.json based on project type and AI-recommended tech stack."""

    # Essential base tasks for ALL Python projects
    base_tasks: list[dict[str, Any]] = [
        # Primary Development Tasks
        {
            "label": "Commit Workflow",
            "type": "shell",
            "command": "poetry run python ${workspaceFolder}/scripts/commit_workflow.py",
            "problemMatcher": [],
            "group": {"kind": "build", "isDefault": True},
            "presentation": {
                "echo": True,
                "reveal": "always",
                "focus": True,
                "panel": "shared",
                "showReuseMessage": False,
                "clear": True,
            },
        },
        {
            "label": "Run Main App",
            "type": "shell",
            "command": "poetry run python ${workspaceFolder}/scripts/clean_run.py",
            "problemMatcher": [],
            "group": "build",
            "presentation": {"reveal": "always", "panel": "new", "clear": True},
        },
        # Dependency Management
        {
            "label": "Install Dependencies",
            "type": "shell",
            "command": "poetry install --with dev",
            "group": "build",
            "problemMatcher": [],
            "presentation": {"reveal": "always", "panel": "shared"},
        },
        {
            "label": "Update Dependencies",
            "type": "shell",
            "command": "poetry update",
            "group": "build",
            "problemMatcher": [],
        },
        {
            "label": "Export Requirements",
            "type": "shell",
            "command": "poetry export -f requirements.txt --output requirements.txt --without-hashes",
            "group": "build",
            "problemMatcher": [],
        },
        # Code Quality Tasks
        {
            "label": "Format Code",
            "type": "shell",
            "command": "poetry run black src/ tests/",
            "group": "build",
            "problemMatcher": [],
            "presentation": {"reveal": "silent", "panel": "shared"},
        },
        {
            "label": "Lint Code",
            "type": "shell",
            "command": "poetry run ruff check src/ tests/ --fix",
            "group": "build",
            "problemMatcher": [],
        },
        {
            "label": "Type Check",
            "type": "shell",
            "command": "poetry run mypy --config-file=.config/mypy.ini src/",
            "group": "test",
            "problemMatcher": [],
        },
        {
            "label": "Lint and Fix All",
            "type": "shell",
            "command": "poetry run black src/ tests/ && poetry run ruff check src/ tests/ --fix && poetry run mypy --config-file=.config/mypy.ini src/",
            "group": "build",
            "problemMatcher": [],
            "presentation": {"reveal": "always", "panel": "shared"},
        },
        # Testing Tasks
        {
            "label": "Run Tests",
            "type": "shell",
            "command": "poetry run pytest",
            "group": {"kind": "test", "isDefault": True},
            "problemMatcher": [],
            "presentation": {"reveal": "always", "panel": "shared"},
        },
        {
            "label": "Test with Coverage",
            "type": "shell",
            "command": "poetry run pytest --cov=src --cov-report=html --cov-report=term",
            "group": "test",
            "problemMatcher": [],
            "presentation": {"reveal": "always", "panel": "shared"},
        },
        {
            "label": "Test Watch Mode",
            "type": "shell",
            "command": "poetry run pytest-watch",
            "group": "test",
            "problemMatcher": [],
            "isBackground": True,
        },
        # Pre-commit Tasks
        {
            "label": "Install Pre-commit Hooks",
            "type": "shell",
            "command": "poetry run pre-commit install",
            "group": "build",
            "problemMatcher": [],
        },
        {
            "label": "Run Pre-commit Checks",
            "type": "shell",
            "command": "poetry run pre-commit run --all-files",
            "group": "test",
            "problemMatcher": [],
            "presentation": {"reveal": "always", "panel": "shared"},
        },
        {
            "label": "Update Pre-commit Hooks",
            "type": "shell",
            "command": "poetry run pre-commit autoupdate",
            "group": "build",
            "problemMatcher": [],
        },
        # Security Tasks
        {
            "label": "Security Scan",
            "type": "shell",
            "command": "poetry run detect-secrets scan --all-files",
            "group": "test",
            "problemMatcher": [],
        },
        {
            "label": "Create Secrets Baseline",
            "type": "shell",
            "command": "poetry run detect-secrets scan --all-files > .secrets.baseline",
            "group": "build",
            "problemMatcher": [],
        },
        # Documentation Tasks
        {
            "label": "Generate Documentation",
            "type": "shell",
            "command": "poetry run sphinx-build -b html docs docs/_build",
            "group": "build",
            "problemMatcher": [],
        },
        # Git Tasks
        {
            "label": "Git Status",
            "type": "shell",
            "command": "git status",
            "group": "none",
            "problemMatcher": [],
            "presentation": {"reveal": "always", "panel": "shared"},
        },
        {
            "label": "Git Push",
            "type": "shell",
            "command": "git push",
            "group": "none",
            "problemMatcher": [],
        },
        # MCP Server Tasks
        {
            "label": "Install MCP Servers",
            "type": "shell",
            "command": "npm install",
            "group": "build",
            "problemMatcher": [],
        },
        # Development Environment
        {
            "label": "Open Coverage Report",
            "type": "shell",
            "command": "${command:python.execInTerminal} -m webbrowser htmlcov/index.html",
            "group": "none",
            "problemMatcher": [],
            "dependsOn": "Test with Coverage",
        },
        {
            "label": "Clean Build Artifacts",
            "type": "shell",
            "command": "rm -rf build/ dist/ *.egg-info/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/ .ruff_cache/",
            "windows": {
                "command": "cmd /c rmdir /s /q build dist *.egg-info .coverage htmlcov .pytest_cache .mypy_cache .ruff_cache"
            },
            "group": "build",
            "problemMatcher": [],
        },
    ]

    # Add project-type specific tasks
    project_tasks = _get_project_specific_tasks(project_type, tech_stack)
    base_tasks.extend(project_tasks)

    # Add tech-stack specific tasks
    tech_tasks = _get_tech_stack_tasks(tech_stack)
    base_tasks.extend(tech_tasks)

    return {"version": "2.0.0", "tasks": base_tasks, "inputs": _get_task_inputs()}


def _get_project_specific_tasks(
    project_type: str, tech_stack: dict[str, str]
) -> list[dict[str, Any]]:
    """Get tasks specific to the project type."""
    tasks = []

    if project_type == "web":
        tasks.extend(_get_web_tasks(tech_stack))
    elif project_type == "cli":
        tasks.extend(_get_cli_tasks())
    elif project_type == "api":
        tasks.extend(_get_api_tasks(tech_stack))
    elif project_type == "data":
        tasks.extend(_get_data_tasks())

    return tasks


def _get_web_tasks(tech_stack: dict[str, str]) -> list[dict[str, Any]]:
    """Get web development specific tasks."""
    tasks = []

    # Backend framework specific tasks
    backend = tech_stack.get("Backend Framework", "")

    if backend == "Django":
        tasks.extend(
            [
                {
                    "label": "Django: Run Server",
                    "type": "shell",
                    "command": "cd backend && poetry run python manage.py runserver",
                    "group": "build",
                    "problemMatcher": [],
                    "presentation": {"reveal": "always", "panel": "new"},
                },
                {
                    "label": "Django: Make Migrations",
                    "type": "shell",
                    "command": "cd backend && poetry run python manage.py makemigrations",
                    "group": "build",
                    "problemMatcher": [],
                },
                {
                    "label": "Django: Migrate",
                    "type": "shell",
                    "command": "cd backend && poetry run python manage.py migrate",
                    "group": "build",
                    "problemMatcher": [],
                },
                {
                    "label": "Django: Create Superuser",
                    "type": "shell",
                    "command": "cd backend && poetry run python manage.py createsuperuser",
                    "group": "build",
                    "problemMatcher": [],
                },
                {
                    "label": "Django: Collect Static",
                    "type": "shell",
                    "command": "cd backend && poetry run python manage.py collectstatic --noinput",
                    "group": "build",
                    "problemMatcher": [],
                },
                {
                    "label": "Django: Shell",
                    "type": "shell",
                    "command": "cd backend && poetry run python manage.py shell",
                    "group": "none",
                    "problemMatcher": [],
                    "presentation": {"reveal": "always", "panel": "new"},
                },
            ]
        )
    elif backend == "Flask":
        tasks.extend(
            [
                {
                    "label": "Flask: Run Server",
                    "type": "shell",
                    "command": "poetry run flask run --debug",
                    "group": "build",
                    "problemMatcher": [],
                    "options": {
                        "env": {"FLASK_APP": "app.py", "FLASK_ENV": "development"}
                    },
                    "presentation": {"reveal": "always", "panel": "new"},
                },
                {
                    "label": "Flask: Shell",
                    "type": "shell",
                    "command": "poetry run flask shell",
                    "group": "none",
                    "problemMatcher": [],
                    "presentation": {"reveal": "always", "panel": "new"},
                },
            ]
        )

    # Frontend tasks
    frontend = tech_stack.get("Frontend", "")
    if frontend and "React" in frontend:
        tasks.extend(
            [
                {
                    "label": "Frontend: Install Dependencies",
                    "type": "shell",
                    "command": "cd frontend && npm install",
                    "group": "build",
                    "problemMatcher": [],
                },
                {
                    "label": "Frontend: Dev Server",
                    "type": "shell",
                    "command": "cd frontend && npm run dev",
                    "group": "build",
                    "problemMatcher": [],
                    "isBackground": True,
                    "presentation": {"reveal": "always", "panel": "new"},
                },
                {
                    "label": "Frontend: Build",
                    "type": "shell",
                    "command": "cd frontend && npm run build",
                    "group": "build",
                    "problemMatcher": [],
                },
                {
                    "label": "Frontend: Test",
                    "type": "shell",
                    "command": "cd frontend && npm test",
                    "group": "test",
                    "problemMatcher": [],
                },
            ]
        )

    return tasks


def _get_cli_tasks() -> list[dict[str, Any]]:
    """Get CLI application specific tasks."""
    return [
        {
            "label": "CLI: Run with Help",
            "type": "shell",
            "command": "poetry run python -m ${workspaceFolderBasename} --help",
            "group": "build",
            "problemMatcher": [],
        },
        {
            "label": "CLI: Build Executable",
            "type": "shell",
            "command": "poetry run pyinstaller --onefile src/${workspaceFolderBasename}/__main__.py",
            "group": "build",
            "problemMatcher": [],
        },
    ]


def _get_api_tasks(tech_stack: dict[str, str]) -> list[dict[str, Any]]:
    """Get API development specific tasks."""
    tasks = []

    api_framework = tech_stack.get("API Framework", "")

    if "FastAPI" in api_framework or tech_stack.get("Backend Framework") == "FastAPI":
        tasks.extend(
            [
                {
                    "label": "FastAPI: Run Server",
                    "type": "shell",
                    "command": "poetry run uvicorn src.${workspaceFolderBasename}.main:app --reload --host 0.0.0.0 --port 8000",
                    "group": "build",
                    "problemMatcher": [],
                    "presentation": {"reveal": "always", "panel": "new"},
                },
                {
                    "label": "FastAPI: Generate OpenAPI Schema",
                    "type": "shell",
                    "command": 'poetry run python -c "import json; from src.${workspaceFolderBasename}.main import app; print(json.dumps(app.openapi(), indent=2))" > openapi.json',
                    "group": "build",
                    "problemMatcher": [],
                },
            ]
        )
    elif "Django REST" in api_framework:
        tasks.extend(
            [
                {
                    "label": "DRF: Generate Schema",
                    "type": "shell",
                    "command": "cd backend && poetry run python manage.py spectacular --file schema.yml",
                    "group": "build",
                    "problemMatcher": [],
                }
            ]
        )

    return tasks


def _get_data_tasks() -> list[dict[str, Any]]:
    """Get data science specific tasks."""
    return [
        {
            "label": "Jupyter: Start Lab",
            "type": "shell",
            "command": "poetry run jupyter lab",
            "group": "build",
            "problemMatcher": [],
            "isBackground": True,
            "presentation": {"reveal": "always", "panel": "new"},
        },
        {
            "label": "Jupyter: Start Notebook",
            "type": "shell",
            "command": "poetry run jupyter notebook",
            "group": "build",
            "problemMatcher": [],
            "isBackground": True,
        },
        {
            "label": "Run Analysis Script",
            "type": "shell",
            "command": "poetry run python src/${workspaceFolderBasename}/analysis.py",
            "group": "build",
            "problemMatcher": [],
        },
        {
            "label": "Convert Notebook to Script",
            "type": "shell",
            "command": "poetry run jupyter nbconvert --to script notebooks/*.ipynb",
            "group": "build",
            "problemMatcher": [],
        },
    ]


def _get_tech_stack_tasks(tech_stack: dict[str, str]) -> list[dict[str, Any]]:
    """Get tasks specific to the technology stack."""
    tasks = []

    # Database tasks
    database = tech_stack.get("Database", "")
    if database == "PostgreSQL":
        tasks.extend(
            [
                {
                    "label": "DB: Start PostgreSQL",
                    "type": "shell",
                    "command": "docker run --name postgres-dev -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:16",
                    "group": "none",
                    "problemMatcher": [],
                },
                {
                    "label": "DB: Connect to PostgreSQL",
                    "type": "shell",
                    "command": "docker exec -it postgres-dev psql -U postgres",
                    "group": "none",
                    "problemMatcher": [],
                    "presentation": {"reveal": "always", "panel": "new"},
                },
            ]
        )
    elif database == "MongoDB":
        tasks.extend(
            [
                {
                    "label": "DB: Start MongoDB",
                    "type": "shell",
                    "command": "docker run --name mongo-dev -p 27017:27017 -d mongo:7",
                    "group": "none",
                    "problemMatcher": [],
                },
                {
                    "label": "DB: Connect to MongoDB",
                    "type": "shell",
                    "command": "docker exec -it mongo-dev mongosh",
                    "group": "none",
                    "problemMatcher": [],
                    "presentation": {"reveal": "always", "panel": "new"},
                },
            ]
        )

    # Celery/Redis tasks
    if "Celery" in str(tech_stack) or "Redis" in str(tech_stack):
        tasks.extend(
            [
                {
                    "label": "Redis: Start Server",
                    "type": "shell",
                    "command": "docker run --name redis-dev -p 6379:6379 -d redis:7-alpine",
                    "group": "none",
                    "problemMatcher": [],
                },
                {
                    "label": "Celery: Start Worker",
                    "type": "shell",
                    "command": "poetry run celery -A ${workspaceFolderBasename} worker -l info",
                    "group": "none",
                    "problemMatcher": [],
                    "isBackground": True,
                    "presentation": {"reveal": "always", "panel": "new"},
                },
                {
                    "label": "Celery: Start Beat",
                    "type": "shell",
                    "command": "poetry run celery -A ${workspaceFolderBasename} beat -l info",
                    "group": "none",
                    "problemMatcher": [],
                    "isBackground": True,
                },
                {
                    "label": "Celery: Flower Monitor",
                    "type": "shell",
                    "command": "poetry run celery -A ${workspaceFolderBasename} flower",
                    "group": "none",
                    "problemMatcher": [],
                    "isBackground": True,
                },
            ]
        )

    # Docker tasks
    if "Docker" in str(tech_stack):
        tasks.extend(
            [
                {
                    "label": "Docker: Build",
                    "type": "shell",
                    "command": "docker build -f docker/Dockerfile -t ${workspaceFolderBasename} .",
                    "group": "build",
                    "problemMatcher": [],
                },
                {
                    "label": "Docker: Run",
                    "type": "shell",
                    "command": "docker run -p 8000:8000 ${workspaceFolderBasename}",
                    "group": "build",
                    "problemMatcher": [],
                },
                {
                    "label": "Docker Compose: Up",
                    "type": "shell",
                    "command": "docker-compose -f docker/docker-compose.yml up",
                    "group": "build",
                    "problemMatcher": [],
                    "presentation": {"reveal": "always", "panel": "new"},
                },
                {
                    "label": "Docker Compose: Down",
                    "type": "shell",
                    "command": "docker-compose -f docker/docker-compose.yml down",
                    "group": "build",
                    "problemMatcher": [],
                },
            ]
        )

    return tasks


def _get_task_inputs() -> list[dict[str, Any]]:
    """Get input definitions for tasks."""
    return [
        {
            "id": "commitMessage",
            "description": "Commit message",
            "default": "Update project files",
            "type": "promptString",
        },
        {
            "id": "testPath",
            "description": "Test file or directory path",
            "default": "tests/",
            "type": "promptString",
        },
        {
            "id": "migrationName",
            "description": "Migration name",
            "default": "update_models",
            "type": "promptString",
        },
    ]
