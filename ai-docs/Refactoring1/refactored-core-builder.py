#!/usr/bin/env python3
# mypy: disable-error-code="name-defined"
"""
Core Project Builder Module - REFACTORED

This module contains the core functionality for creating Python projects.
Now fully AI-driven without hardcoded technology choices.
"""

import json
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
    Create the complete project structure with IDE configurations.

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

        # Extract AI analysis for intelligent structure creation
        ai_analysis = tech_stack.get("analysis", [])

        # Create basic package directory
        package_dir = os.path.join(project_dir, "src", package_name)
        os.makedirs(package_dir, exist_ok=True)

        # Create __init__.py
        with open(os.path.join(package_dir, "__init__.py"), "w", encoding="utf-8") as f:
            f.write(f'"""Package {package_name}."""\n__version__ = "0.1.0"\n')

        # NEW: Create workspace file FIRST for easy opening
        _create_workspace_file(project_dir, project_name, project_type, tech_stack)

        # NEW: Create scripts directory with automation tools
        _create_scripts_directory(project_dir, package_name)

        # NEW: Create config directory for linters
        _create_config_directory(project_dir)

        # NEW: Create package.json for MCP servers
        _create_package_json(project_dir, tech_stack)

        # Use new template manager for project-specific structure
        from .project_templates import ProjectTemplateManager

        template_manager = ProjectTemplateManager(project_dir, project_name, tech_stack)
        template_manager.create_project_structure(project_type)

        # Create IDE configurations for both VS Code and Cursor
        from .ide_config import IDEConfigManager

        ide_manager = IDEConfigManager(
            project_dir, project_name, project_type, tech_stack
        )
        ide_manager.create_vscode_config()
        ide_manager.create_cursor_config()

        # Create GitHub folder with Copilot configuration
        _create_github_folder(project_dir, project_name, project_type, tech_stack)

        # Create Poetry configuration with AI-driven dependencies
        _create_pyproject_toml(project_dir, project_name, project_type, tech_stack)

        # Create enhanced .env files based on tech stack
        _create_environment_files(project_dir, project_type, tech_stack)

        # Create project-specific structures based on AI analysis
        _create_ai_driven_structures(project_dir, package_name, tech_stack, ai_analysis)

        # Initialize git and pre-commit hooks
        _initialize_development_tools(project_dir)

        return True, f"Complete AI-driven project structure created at {project_dir}"

    except Exception as e:
        return False, f"Failed to create project structure: {str(e)}"


def _create_workspace_file(
    project_dir: str, project_name: str, project_type: str, tech_stack: dict[Any, Any]
):
    """Create VS Code workspace file for easy project opening."""
    workspace_config = {
        "folders": [{"name": project_name.replace("_", " ").title(), "path": "."}],
        "settings": {
            "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
            "python.terminal.activateEnvironment": True,
            "python.testing.pytestEnabled": True,
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.organizeImports": "explicit",
                "source.fixAll.ruff": "explicit",
            },
            "[python]": {"editor.defaultFormatter": "ms-python.black-formatter"},
            "files.exclude": {
                "**/__pycache__": True,
                "**/*.pyc": True,
                ".mypy_cache": True,
                ".pytest_cache": True,
                ".ruff_cache": True,
                "htmlcov": True,
                ".coverage": True,
            },
            "mcp.envFile": "${workspaceFolder}/.env",
        },
    }

    # Add project-specific folders based on tech stack
    backend_framework = _extract_tech_choice(tech_stack, "Backend Framework")
    frontend_framework = _extract_tech_choice(tech_stack, "Frontend")

    if backend_framework in ["Django", "Flask", "FastAPI"]:
        workspace_config["folders"].append({"name": "Backend", "path": "./backend"})

    if frontend_framework and "React" in frontend_framework:
        workspace_config["folders"].append({"name": "Frontend", "path": "./frontend"})

    # Add tests folder
    workspace_config["folders"].append({"name": "Tests", "path": "./tests"})

    # Add scripts folder
    workspace_config["folders"].append({"name": "Scripts", "path": "./scripts"})

    # For IoT/Hardware projects
    if any(
        keyword in project_name.lower()
        for keyword in ["esp32", "iot", "arduino", "sensor", "raspberry"]
    ):
        workspace_config["folders"].append({"name": "Firmware", "path": "./firmware"})
        workspace_config["settings"][
            "platformio-ide.activateOnlyOnPlatformIOProject"
        ] = True

    workspace_file = os.path.join(project_dir, f"{project_name}.code-workspace")
    with open(workspace_file, "w", encoding="utf-8") as f:
        json.dump(workspace_config, f, indent=2)


def _create_scripts_directory(project_dir: str, package_name: str):
    """Create scripts directory with essential automation tools."""
    scripts_dir = os.path.join(project_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    # Create commit workflow script
    commit_workflow = f"""#!/usr/bin/env python3
\"\"\"AI-powered commit workflow for {package_name}.\"\"\"

import subprocess
import sys
from pathlib import Path


def run_pre_commit_checks():
    \"\"\"Run all pre-commit checks.\"\"\"
    print("🔍 Running pre-commit checks...")
    result = subprocess.run(["pre-commit", "run", "--all-files"], capture_output=True)
    if result.returncode != 0:
        print("❌ Pre-commit checks failed!")
        print(result.stdout.decode())
        print(result.stderr.decode())
        return False
    print("✅ All checks passed!")
    return True


def generate_commit_message():
    \"\"\"Generate commit message based on changes.\"\"\"
    # Get staged changes
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-status"],
        capture_output=True,
        text=True
    )
    
    if not result.stdout:
        return "chore: update project files"
    
    changes = result.stdout.strip().split("\\n")
    
    # Analyze changes
    added = [f for f in changes if f.startswith("A")]
    modified = [f for f in changes if f.startswith("M")]
    deleted = [f for f in changes if f.startswith("D")]
    
    # Generate message based on changes
    if len(changes) == 1:
        action, file = changes[0].split("\\t")
        action_word = {{"A": "add", "M": "update", "D": "remove"}}.get(action, "change")
        return f"{{action_word}}: {{file}}"
    
    parts = []
    if added:
        parts.append(f"add {{len(added)}} file{'s' if len(added) > 1 else ''}")
    if modified:
        parts.append(f"update {{len(modified)}} file{'s' if len(modified) > 1 else ''}")
    if deleted:
        parts.append(f"remove {{len(deleted)}} file{'s' if len(deleted) > 1 else ''}")
    
    return "feat: " + ", ".join(parts)


def main():
    \"\"\"Main commit workflow.\"\"\"
    # Check if we're in a git repository
    if not Path(".git").exists():
        print("❌ Not in a git repository!")
        sys.exit(1)
    
    # Stage all changes
    print("📦 Staging all changes...")
    subprocess.run(["git", "add", "."])
    
    # Check if there are changes to commit
    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        capture_output=True
    )
    
    if result.returncode == 0:
        print("ℹ️  No changes to commit")
        sys.exit(0)
    
    # Run checks
    if not run_pre_commit_checks():
        print("\\n💡 Fix the issues above and run again")
        sys.exit(1)
    
    # Generate commit message
    message = generate_commit_message()
    print(f"\\n📝 Commit message: {{message}}")
    
    # Allow user to edit message
    user_message = input("Press Enter to use this message or type a new one: ").strip()
    if user_message:
        message = user_message
    
    # Commit
    subprocess.run(["git", "commit", "-m", message])
    print("\\n✅ Changes committed successfully!")
    
    # Ask about pushing
    push = input("\\nPush to remote? [y/N]: ").lower().strip()
    if push == 'y':
        subprocess.run(["git", "push"])
        print("✅ Pushed to remote!")


if __name__ == "__main__":
    main()
"""

    with open(os.path.join(scripts_dir, "commit_workflow.py"), "w") as f:
        f.write(commit_workflow)
    os.chmod(os.path.join(scripts_dir, "commit_workflow.py"), 0o755)

    # Create clean run script
    clean_run = f"""#!/usr/bin/env python3
\"\"\"Clean run script for {package_name}.\"\"\"

import os
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Clear terminal
os.system('clear' if os.name != 'nt' else 'cls')

# Run main module
from {package_name} import main

if __name__ == "__main__":
    main()
"""

    with open(os.path.join(scripts_dir, "clean_run.py"), "w") as f:
        f.write(clean_run)
    os.chmod(os.path.join(scripts_dir, "clean_run.py"), 0o755)


def _create_config_directory(project_dir: str):
    """Create .config directory with linting and type checking configs."""
    config_dir = os.path.join(project_dir, ".config")
    os.makedirs(config_dir, exist_ok=True)

    # Create mypy.ini
    mypy_content = """[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = False
disallow_incomplete_defs = False
check_untyped_defs = True
disallow_untyped_decorators = False
no_implicit_optional = True
strict_optional = True

# Ignore missing imports for common packages
[[mypy.overrides]]
module = [
    "flask.*",
    "django.*",
    "fastapi.*",
    "cv2.*",
    "kivy.*",
    "celery.*",
    "redis.*"
]
ignore_missing_imports = true
"""
    with open(os.path.join(config_dir, "mypy.ini"), "w") as f:
        f.write(mypy_content)

    # Create ruff.toml
    ruff_content = """target-version = "py311"
line-length = 88

[lint]
select = ["E", "F", "I", "N", "W", "B", "C4", "SIM", "UP"]
ignore = ["E501", "B008"]

[lint.per-file-ignores]
"tests/*" = ["E501"]
"migrations/*" = ["E501", "N806"]
"""
    with open(os.path.join(config_dir, "ruff.toml"), "w") as f:
        f.write(ruff_content)

    # Create .pre-commit-config.yaml in project root
    precommit_content = """default_stages: [pre-commit]
repos:
  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks:
      - id: black
        stages: [pre-commit]

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix, --config=.config/ruff.toml]
        stages: [pre-commit]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.2
    hooks:
      - id: mypy
        args: [--ignore-missing-imports, --config-file=.config/mypy.ini]
        stages: [pre-commit]
        additional_dependencies: [types-requests]

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
"""
    with open(os.path.join(project_dir, ".pre-commit-config.yaml"), "w") as f:
        f.write(precommit_content)


def _create_package_json(project_dir: str, tech_stack: dict[Any, Any]):
    """Create package.json for MCP server management."""
    package_json = {
        "name": os.path.basename(project_dir),
        "version": "1.0.0",
        "description": "MCP servers for enhanced development",
        "private": True,
        "dependencies": {
            "@upstash/context7-mcp": "latest",
            "server-perplexity-ask": "latest",
            "@modelcontextprotocol/server-filesystem": "latest",
        },
    }

    # Add GitHub MCP if version control is needed
    package_json["dependencies"]["@github/github-mcp-server"] = "latest"

    # Add project-specific MCP servers based on tech stack
    if "PostgreSQL" in str(tech_stack):
        package_json["dependencies"]["@modelcontextprotocol/server-postgres"] = "latest"

    if "Real-time" in str(tech_stack) or "WebSocket" in str(tech_stack):
        package_json["dependencies"]["websocket-debugger-mcp"] = "latest"

    with open(os.path.join(project_dir, "package.json"), "w") as f:
        json.dump(package_json, f, indent=2)


def _create_pyproject_toml(
    project_dir: str, project_name: str, project_type: str, tech_stack: dict[Any, Any]
):
    """Create Poetry configuration with AI-recommended dependencies."""
    package_name = project_name.replace("-", "_").replace(" ", "_").lower()

    # Get dynamic dependencies based on AI recommendations
    project_deps = _get_dynamic_project_dependencies(tech_stack)

    content = f"""[tool.poetry]
name = "{project_name}"
version = "0.1.0"
description = "AI-generated project with dynamic technology stack"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"
packages = [{{include = "{package_name}", from = "src"}}]

[tool.poetry.dependencies]
python = "^3.11"
{project_deps}

[tool.poetry.group.dev.dependencies]
# Essential development tools - ALWAYS included
pytest = "^8.3.3"
pytest-cov = "^5.0.0"
pytest-asyncio = "^0.24.0"
pytest-mock = "^3.14.0"
black = "^24.8.0"
ruff = "^0.6.9"
mypy = "^1.11.2"
pre-commit = "^3.8.0"
detect-secrets = "^1.5.0"
python-dotenv = "^1.0.1"
ipython = "^8.27.0"
rich = "^13.8.1"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 88
target-version = ['py311']

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "B", "C4", "SIM", "UP"]
ignore = ["E501", "B008"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-ra -q --strict-markers"

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/test_*"]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
"""

    with open(os.path.join(project_dir, "pyproject.toml"), "w", encoding="utf-8") as f:
        f.write(content)


def _get_dynamic_project_dependencies(tech_stack: dict[Any, Any]) -> str:
    """Extract dependencies from AI-recommended tech stack."""
    deps = []

    # Comprehensive technology to package mapping
    tech_to_packages = {
        # Backend Frameworks
        "Django": [
            'django = "^5.1.2"',
            'django-environ = "^0.11.2"',
            'django-extensions = "^3.2.3"',
        ],
        "Flask": [
            'flask = "^3.0.3"',
            'python-dotenv = "^1.0.1"',
            'flask-cors = "^4.0.1"',
        ],
        "FastAPI": [
            'fastapi = "^0.115.0"',
            'uvicorn = "^0.31.0"',
            'pydantic = "^2.9.2"',
            'pydantic-settings = "^2.5.2"',
        ],
        # Databases
        "PostgreSQL": ['psycopg2-binary = "^2.9.9"', 'sqlalchemy = "^2.0.35"'],
        "MongoDB": ['pymongo = "^4.8.0"', 'mongoengine = "^0.29.1"'],
        "SQLite": [],  # Built-in
        # Authentication
        "Django-Allauth": [
            'django-allauth = "^65.0.2"',
            'django-allauth-2fa = "^0.11.1"',
        ],
        "Flask-Login": ['flask-login = "^0.6.3"', 'werkzeug = "^3.0.4"'],
        "PyJWT": ['pyjwt = "^2.9.0"'],
        "Authlib": ['authlib = "^1.3.2"'],
        # API Frameworks
        "Django REST Framework": [
            'djangorestframework = "^3.15.2"',
            'django-cors-headers = "^4.4.0"',
            'drf-spectacular = "^0.27.2"',
        ],
        "Flask-RESTful": ['flask-restful = "^0.3.10"', 'marshmallow = "^3.22.0"'],
        # Geospatial
        "GeoDjango + Leaflet": [
            'django-leaflet = "^0.30.1"',
            'geopy = "^2.4.1"',
            'django-geojson = "^4.1.0"',
        ],
        # Real-time Communication
        "WebSockets": ['websockets = "^13.1"', 'channels = "^4.1.0"'],
        "Flask-SocketIO": [
            'flask-socketio = "^5.3.6"',
            'python-socketio = "^5.11.3"',
            'eventlet = "^0.36.1"',
        ],
        # Task Queues
        "Celery + Redis": [
            'celery = "^5.4.0"',
            'redis = "^5.1.0"',
            'flower = "^2.0.1"',
        ],
        # Data Science
        "Pandas": ['pandas = "^2.2.3"', 'numpy = "^2.1.2"'],
        "Matplotlib": ['matplotlib = "^3.9.2"', 'seaborn = "^0.13.2"'],
        # IoT/Hardware
        "MJPG-Streamer": ['opencv-python = "^4.10.0.84"', 'pillow = "^10.4.0"'],
        "Kivy": ['kivy = "^2.3.0"'],
        # Frontend Integration
        "React + TypeScript": ['whitenoise = "^6.7.0"'],
        "HTMX + Alpine.js": ['django-htmx = "^1.19.0"'],
        # Testing
        "Pytest": [],  # Already in dev dependencies
        # Documentation
        "Sphinx": ['sphinx = "^8.0.2"', 'sphinx-rtd-theme = "^2.0.0"'],
    }

    # Extract all recommended technologies from AI response
    recommended_techs = []
    if isinstance(tech_stack, dict) and "categories" in tech_stack:
        for category in tech_stack["categories"]:
            for option in category.get("options", []):
                if option.get("recommended", False):
                    recommended_techs.append(option["name"])

    # Build dependency list
    for tech in recommended_techs:
        if tech in tech_to_packages:
            deps.extend(tech_to_packages[tech])

    # Remove duplicates while preserving order
    seen = set()
    unique_deps = []
    for dep in deps:
        if dep not in seen:
            seen.add(dep)
            unique_deps.append(dep)

    return "\n".join(unique_deps) if unique_deps else ""


def _create_environment_files(
    project_dir: str, project_type: str, tech_stack: dict[Any, Any]
):
    """Create .env template and .gitignore based on tech stack."""
    env_lines = ["# Environment variables", "DEBUG=True", ""]

    # Extract technologies
    backend = _extract_tech_choice(tech_stack, "Backend Framework")
    database = _extract_tech_choice(tech_stack, "Database")
    auth = _extract_tech_choice(tech_stack, "Authentication")

    # Backend-specific env vars
    if backend == "Django":
        env_lines.extend(
            [
                "# Django",
                "SECRET_KEY=your-secret-key-here",
                "ALLOWED_HOSTS=localhost,127.0.0.1",
                "",
            ]
        )
    elif backend == "Flask":
        env_lines.extend(
            [
                "# Flask",
                "FLASK_APP=app.py",
                "FLASK_ENV=development",
                "SECRET_KEY=your-secret-key-here",
                "",
            ]
        )
    elif backend == "FastAPI":
        env_lines.extend(["# FastAPI", "APP_NAME=YourAppName", "API_VERSION=v1", ""])

    # Database configuration
    if database == "PostgreSQL":
        env_lines.extend(
            [
                "# Database",
                "DATABASE_URL=postgresql://user:password@localhost:5432/dbname",
                "DB_HOST=localhost",
                "DB_PORT=5432",
                "DB_NAME=your_db_name",
                "DB_USER=postgres",
                "DB_PASSWORD=postgres",
                "",
            ]
        )
    elif database == "MongoDB":
        env_lines.extend(
            ["# Database", "MONGODB_URI=mongodb://localhost:27017/your_db_name", ""]
        )
    elif database == "SQLite":
        env_lines.extend(["# Database", "DATABASE_URL=sqlite:///./app.db", ""])

    # OAuth configuration
    if "OAuth" in str(auth) or "Allauth" in str(auth):
        env_lines.extend(
            [
                "# OAuth",
                "GOOGLE_CLIENT_ID=your-google-client-id",
                "GOOGLE_CLIENT_SECRET=your-google-client-secret",
                "GITHUB_CLIENT_ID=your-github-client-id",
                "GITHUB_CLIENT_SECRET=your-github-client-secret",
                "",
            ]
        )

    # Redis/Celery configuration
    if "Celery" in str(tech_stack) or "Redis" in str(tech_stack):
        env_lines.extend(
            [
                "# Redis/Celery",
                "REDIS_URL=redis://localhost:6379/0",
                "CELERY_BROKER_URL=redis://localhost:6379/0",
                "CELERY_RESULT_BACKEND=redis://localhost:6379/0",
                "",
            ]
        )

    # MCP Configuration
    env_lines.extend(
        [
            "# MCP Configuration",
            "GITHUB_PERSONAL_ACCESS_TOKEN=your-github-pat",
            "PERPLEXITY_API_KEY=your-perplexity-key",
            "ANTHROPIC_API_KEY=your-anthropic-key",
            "",
        ]
    )

    # Write .env.example
    with open(os.path.join(project_dir, ".env.example"), "w", encoding="utf-8") as f:
        f.write("\n".join(env_lines))

    # Create .env.template (same content for now)
    with open(os.path.join(project_dir, ".env.template"), "w", encoding="utf-8") as f:
        f.write("\n".join(env_lines))

    # Enhanced .gitignore
    gitignore_content = """# Python
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
MANIFEST

# Virtual Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.idea/
.vscode/mcp.json
.cursor/mcp.json
*.swp
*.swo
*~

# Testing
.tox/
.coverage
.coverage.*
.cache
.pytest_cache/
nosetests.xml
coverage.xml
*.cover
.hypothesis/
htmlcov/
.mypy_cache/
.ruff_cache/

# Logs
logs/
*.log

# Database
*.sqlite3
*.db

# Environment files
.env
.env.local
.env.*.local

# macOS
.DS_Store

# Node (for MCP servers)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Distribution
dist/
build/

# Jupyter
.ipynb_checkpoints/

# Secrets
.secrets.baseline
"""

    with open(os.path.join(project_dir, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(gitignore_content)


def _create_ai_driven_structures(
    project_dir: str,
    package_name: str,
    tech_stack: dict[Any, Any],
    ai_analysis: list[str],
):
    """Create additional project structures based on AI analysis."""

    # Parse AI analysis for specific needs
    analysis_text = " ".join(ai_analysis).lower()

    # Create Docker configuration if mentioned
    if "docker" in analysis_text or "container" in analysis_text:
        _create_docker_config(project_dir, tech_stack)

    # Create CI/CD configuration
    if "ci/cd" in analysis_text or "continuous" in analysis_text:
        _create_cicd_config(project_dir)

    # Create documentation structure
    docs_dir = os.path.join(project_dir, "docs")
    os.makedirs(docs_dir, exist_ok=True)

    # Create tests structure
    tests_dir = os.path.join(project_dir, "tests")
    os.makedirs(tests_dir, exist_ok=True)
    os.makedirs(os.path.join(tests_dir, "unit"), exist_ok=True)
    os.makedirs(os.path.join(tests_dir, "integration"), exist_ok=True)

    # Create test configuration
    with open(os.path.join(tests_dir, "conftest.py"), "w") as f:
        f.write(
            '''"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
import sys

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {
        "test": True,
        "data": [1, 2, 3]
    }
'''
        )


def _create_docker_config(project_dir: str, tech_stack: dict[Any, Any]):
    """Create Docker configuration files."""
    docker_dir = os.path.join(project_dir, "docker")
    os.makedirs(docker_dir, exist_ok=True)

    backend = _extract_tech_choice(tech_stack, "Backend Framework")

    # Create Dockerfile
    dockerfile_content = f"""FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \\
    && poetry install --no-interaction --no-ansi

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "-m", "{backend.lower()}", "run", "--host", "0.0.0.0"]
"""

    with open(os.path.join(docker_dir, "Dockerfile"), "w") as f:
        f.write(dockerfile_content)

    # Create docker-compose.yml
    compose_content = """version: '3.8'

services:
  app:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
    volumes:
      - ../src:/app/src
    depends_on:
      - db
      - redis

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: app_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
"""

    with open(os.path.join(docker_dir, "docker-compose.yml"), "w") as f:
        f.write(compose_content)


def _create_cicd_config(project_dir: str):
    """Create CI/CD configuration."""
    github_dir = os.path.join(project_dir, ".github", "workflows")
    os.makedirs(github_dir, exist_ok=True)

    # Create GitHub Actions workflow
    workflow_content = """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install Poetry
      uses: snok/install-poetry@v1
      with:
        version: latest
        virtualenvs-create: true
        virtualenvs-in-project: true
    
    - name: Load cached dependencies
      uses: actions/cache@v4
      with:
        path: .venv
        key: venv-${{ runner.os }}-${{ hashFiles('**/poetry.lock') }}
    
    - name: Install dependencies
      run: poetry install --no-interaction --no-root
    
    - name: Run linting
      run: |
        poetry run black --check src/
        poetry run ruff check src/
        poetry run mypy src/
    
    - name: Run tests
      run: poetry run pytest tests/ -v --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml
"""

    with open(os.path.join(github_dir, "ci.yml"), "w") as f:
        f.write(workflow_content)


def _initialize_development_tools(project_dir: str):
    """Initialize git and pre-commit hooks."""
    try:
        # Initialize git if not already initialized
        if not os.path.exists(os.path.join(project_dir, ".git")):
            subprocess.run(["git", "init"], cwd=project_dir, capture_output=True)

        # Create initial commit
        subprocess.run(["git", "add", "."], cwd=project_dir, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial project structure"],
            cwd=project_dir,
            capture_output=True,
        )
    except Exception:
        pass  # Git initialization is optional


def _extract_tech_choice(tech_stack: dict[Any, Any], category_name: str) -> str:
    """Extract the recommended technology for a given category."""
    if isinstance(tech_stack, dict) and "categories" in tech_stack:
        for category in tech_stack["categories"]:
            if category.get("name") == category_name:
                for option in category.get("options", []):
                    if option.get("recommended", False):
                        return option["name"]
    return ""


def setup_virtual_environment(project_dir: str) -> tuple[bool, str]:
    """Set up Poetry environment and install dependencies."""
    try:
        # Check if Poetry is installed
        if not shutil.which("poetry"):
            return False, "Poetry is not installed. Please install Poetry first."

        # Configure Poetry to create venv in project
        subprocess.run(
            ["poetry", "config", "virtualenvs.in-project", "true"],
            cwd=project_dir,
            check=True,
            capture_output=True,
        )

        # Install dependencies
        result = subprocess.run(
            ["poetry", "install"],
            cwd=project_dir,
            check=True,
            capture_output=True,
            text=True,
        )

        # Generate requirements.txt for compatibility
        subprocess.run(
            [
                "poetry",
                "export",
                "-f",
                "requirements.txt",
                "--output",
                "requirements.txt",
            ],
            cwd=project_dir,
            capture_output=True,
        )

        # Install pre-commit hooks
        subprocess.run(
            ["poetry", "run", "pre-commit", "install"],
            cwd=project_dir,
            capture_output=True,
        )

        # Install Node dependencies for MCP servers
        if os.path.exists(os.path.join(project_dir, "package.json")):
            if shutil.which("npm"):
                subprocess.run(
                    ["npm", "install"],
                    cwd=project_dir,
                    capture_output=True,
                )

        return (
            True,
            "Poetry environment created and all dependencies installed successfully",
        )

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
    """Initialize a Git repository with enhanced configuration."""
    try:
        # Initialize git repository if not already done
        if not os.path.exists(os.path.join(project_dir, ".git")):
            subprocess.run(
                ["git", "init"], cwd=project_dir, check=True, capture_output=True
            )

        # Configure remote repositories if usernames are provided
        if github_username:
            github_url = f"git@github.com:{github_username}/{project_name}.git"
            subprocess.run(
                ["git", "remote", "add", "origin", github_url],
                cwd=project_dir,
                capture_output=True,
            )

        if gitlab_username:
            gitlab_url = f"git@gitlab.com:{gitlab_username}/{project_name}.git"
            remote_name = "gitlab" if github_username else "origin"
            subprocess.run(
                ["git", "remote", "add", remote_name, gitlab_url],
                cwd=project_dir,
                capture_output=True,
            )

        # Create comprehensive README
        readme_content = f"""# {project_name.replace('_', ' ').replace('-', ' ').title()}

{project_description}

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Poetry
- Git

### Installation

1. Clone the repository:
```bash
git clone {"git@github.com:" + github_username + "/" + project_name + ".git" if github_username else "<repository-url>"}
cd {project_name}
```

2. Install dependencies:
```bash
poetry install
```

3. Set up pre-commit hooks:
```bash
poetry run pre-commit install
```

4. Copy environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
poetry run python -m {project_name.replace('-', '_')}
```

## 🧪 Testing

Run tests with coverage:
```bash
poetry run pytest --cov
```

## 🔧 Development

### Code Quality
```bash
# Format code
poetry run black src/

# Lint code
poetry run ruff check src/ --fix

# Type check
poetry run mypy src/
```

### Commit Workflow
```bash
poetry run python scripts/commit_workflow.py
```

## 📚 Documentation

Documentation is available in the `docs/` directory.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes using the commit workflow
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.
"""

        with open(os.path.join(project_dir, "README.md"), "w") as f:
            f.write(readme_content)

        return True, "Git repository initialized with enhanced configuration"

    except subprocess.CalledProcessError as e:
        return (
            False,
            f"Failed to initialize Git repository: {e.stderr.decode() if e.stderr else str(e)}",
        )
    except Exception as e:
        return False, f"Failed to initialize Git repository: {str(e)}"


def _create_github_folder(
    project_dir: str, project_name: str, project_type: str, tech_stack: dict[str, Any]
) -> bool:
    """Create .github folder with Copilot and workflow configuration."""
    github_dir = os.path.join(project_dir, ".github")
    os.makedirs(github_dir, exist_ok=True)

    # Extract technologies for documentation
    tech_summary = []
    if isinstance(tech_stack, dict) and "categories" in tech_stack:
        for category in tech_stack["categories"]:
            for option in category.get("options", []):
                if option.get("recommended", False):
                    tech_summary.append(f"- **{category['name']}**: {option['name']}")

    # Create copilot instructions
    copilot_content = f"""# {project_name} - GitHub Copilot Instructions

## Project Overview
{project_type.capitalize()} project built with an AI-curated technology stack.

## Technology Stack
{chr(10).join(tech_summary) if tech_summary else "Standard Python project"}

## Coding Standards
- Follow PEP 8 conventions
- Use type hints for all function signatures
- Write comprehensive docstrings (Google style)
- Include unit tests for all new functionality
- Maintain test coverage above 80%
- Use meaningful variable and function names

## Project Structure
- `src/`: Source code
- `tests/`: Test files (mirror src structure)
- `docs/`: Documentation
- `scripts/`: Automation scripts
- Use Poetry for dependency management
- Configuration through environment variables

## Development Workflow
1. Create feature branch from develop
2. Write tests first (TDD approach)
3. Implement functionality
4. Run linting and tests
5. Use commit workflow script
6. Create pull request

## Security Guidelines
- Never commit secrets or credentials
- Use environment variables for configuration
- Validate all user inputs
- Follow OWASP guidelines for web applications
"""

    with open(os.path.join(github_dir, "copilot-instructions.md"), "w") as f:
        f.write(copilot_content)

    return True
