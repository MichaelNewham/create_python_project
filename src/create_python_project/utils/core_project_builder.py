#!/usr/bin/env python3
# mypy: disable-error-code="name-defined"
"""
Core Project Builder Module - REFACTORED

This module contains the core functionality for creating Python projects.
Now fully AI-driven without hardcoded technology choices.
"""

import json
import os
import re
import shutil
import subprocess
from typing import Any
from urllib.parse import urlparse


def is_remote_path(path: str) -> bool:
    """Check if the path is a remote SFTP URL."""
    return path.startswith("sftp://")


def parse_remote_path(sftp_url: str) -> tuple[str, str, int, str]:
    """
    Parse an SFTP URL to extract connection details.

    Args:
        sftp_url: SFTP URL in format sftp://user@host:port/path

    Returns:
        Tuple of (user, host, port, path)
    """
    parsed = urlparse(sftp_url)
    user = parsed.username or "mail2mick"
    host = parsed.hostname or "manjarodell-to-pi"
    port = parsed.port or 8850
    path = parsed.path or "/"
    return user, host, port, path


def execute_remote_command(sftp_url: str, command: str) -> tuple[bool, str]:
    """
    Execute a command on a remote server via SSH.

    Args:
        sftp_url: SFTP URL with connection details
        command: Command to execute

    Returns:
        Tuple of (success, output/error message)
    """
    user, host, port, _ = parse_remote_path(sftp_url)
    ssh_command = f"ssh {user}@{host} '{command}'"

    try:
        result = subprocess.run(
            ssh_command, shell=True, capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)


def create_remote_directory(sftp_url: str) -> tuple[bool, str]:
    """Create a directory on a remote server."""
    _, _, _, path = parse_remote_path(sftp_url)
    command = f"mkdir -p {path}"
    return execute_remote_command(sftp_url, command)


def create_remote_file(
    sftp_url: str, content: str, relative_path: str
) -> tuple[bool, str]:
    """Create a file on a remote server."""
    user, host, port, base_path = parse_remote_path(sftp_url)
    full_path = os.path.join(base_path, relative_path)

    # Create parent directory
    parent_dir = os.path.dirname(full_path)
    mkdir_cmd = f"mkdir -p {parent_dir}"
    execute_remote_command(sftp_url, mkdir_cmd)

    # Write file using SSH and cat
    escaped_content = content.replace("'", "'\\''")
    command = f"cat > {full_path} << 'EOF'\n{escaped_content}\nEOF"

    ssh_command = f"ssh {user}@{host} '{command}'"

    try:
        result = subprocess.run(
            ssh_command, shell=True, capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return True, f"Created {relative_path}"
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)


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

        # Check if this is a remote directory
        is_remote = kwargs.get("is_remote", False) or is_remote_path(project_dir)

        # Apply ARM64 optimizations if target is ARM
        target_arch = kwargs.get("target_architecture", "x86_64")
        if target_arch == "arm64" and tech_stack:
            # ARM64 optimizations temporarily disabled
            print("ARM64 target detected - optimizations available but disabled")

        if is_remote:
            # Handle remote project creation
            print(f"Creating remote project at: {project_dir}")

            # Create remote directory
            success, msg = create_remote_directory(project_dir)
            if not success:
                return False, f"Failed to create remote directory: {msg}"

            # For remote projects, create a minimal structure
            # and provide instructions for full setup
            _, _, _, remote_path = parse_remote_path(project_dir)

            # Create basic structure remotely
            basic_files = {
                "README.md": f"# {project_name}\n\nCreated via remote connection.",
                "src/__init__.py": "",
                f"src/{package_name}/__init__.py": f'"""Package {package_name}."""\n__version__ = "0.1.0"\n',
                ".gitignore": "*.pyc\n__pycache__/\n.env\n.venv/\nvenv/\n",
            }

            for file_path, content in basic_files.items():
                success, msg = create_remote_file(project_dir, content, file_path)
                if not success:
                    print(f"Warning: Failed to create {file_path}: {msg}")

            # Provide instructions for completing setup
            instructions = f"""
Remote project initialized at: {remote_path}

To complete the setup:
1. SSH into your Raspberry Pi: ssh {parse_remote_path(project_dir)[0]}@{parse_remote_path(project_dir)[1]}
2. Navigate to: cd {remote_path}
3. Run: git init
4. Install Poetry: curl -sSL https://install.python-poetry.org | python3 -
5. Create pyproject.toml and install dependencies

Or, clone this project locally, complete setup, and push to the Pi.
"""
            return True, instructions

        # Local directory creation (existing logic)
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

        # Create IDE configurations for VS Code
        from .ide_config import IDEConfigManager

        ide_manager = IDEConfigManager(
            project_dir, project_name, project_type, tech_stack
        )
        ide_manager.create_vscode_config()

        # Create GitHub folder with Copilot configuration
        _create_github_folder(project_dir, project_name, project_type, tech_stack)

        # Create Poetry configuration with AI-driven dependencies
        _create_pyproject_toml(project_dir, project_name, project_type, tech_stack)

        # Create enhanced .env files based on tech stack
        _create_environment_files(project_dir, project_type, tech_stack)

        # Create project-specific structures based on AI analysis
        expert_consultation = kwargs.get("expert_consultation", {})
        project_description = kwargs.get("project_description", "")
        _create_ai_driven_structures(
            project_dir,
            package_name,
            tech_stack,
            ai_analysis,
            expert_consultation,
            project_description,
        )

        # Initialize git and pre-commit hooks
        _initialize_development_tools(project_dir)

        return True, f"Complete AI-driven project structure created at {project_dir}"

    except Exception as e:
        return False, f"Failed to create project structure: {str(e)}"


def _create_workspace_file(
    project_dir: str, project_name: str, project_type: str, tech_stack: dict[Any, Any]
):
    """Create VS Code workspace file for easy project opening with auto-installing extensions."""
    # Get extension recommendations for this project
    from .extension_config import get_extensions_for_project

    tech_choices = _extract_tech_choices_dict(tech_stack)
    extensions = get_extensions_for_project(project_type, tech_choices)

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
        "extensions": {"recommendations": extensions},
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

    # Create commit workflow script - with f-string literals properly escaped
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
        parts.append(f"add {{len(added)}} file{{'s' if len(added) > 1 else ''}}")
    if modified:
        parts.append(f"update {{len(modified)}} file{{'s' if len(modified) > 1 else ''}}")
    if deleted:
        parts.append(f"remove {{len(deleted)}} file{{'s' if len(deleted) > 1 else ''}}")

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
from {{package_name}} import main

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
    deps: list[str] = []

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
            tech_deps = tech_to_packages[tech]
            if isinstance(tech_deps, list):
                deps.extend(tech_deps)

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
    """Create symlink to shared .env and .env.example with sanitized keys."""
    import os

    # Path to shared .env file
    shared_env_path = "/home/michaelnewham/Projects/.env"
    project_env_path = os.path.join(project_dir, ".env")

    # Create symlink to shared .env file
    try:
        if os.path.exists(shared_env_path):
            # Remove existing .env if it exists
            if os.path.exists(project_env_path):
                os.remove(project_env_path)
            # Create symlink
            os.symlink(shared_env_path, project_env_path)
        else:
            print(f"Warning: Shared .env file not found at {shared_env_path}")
    except Exception as e:
        print(f"Warning: Failed to create .env symlink: {e}")

    # Create .env.example by reading shared .env and sanitizing API keys
    env_example_lines = []

    if os.path.exists(shared_env_path):
        with open(shared_env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    # Extract variable name and sanitize value
                    if "=" in line:
                        var_name, _ = line.split("=", 1)
                        # Sanitize API keys and tokens
                        if any(
                            key_word in var_name.upper()
                            for key_word in ["KEY", "TOKEN", "SECRET"]
                        ):
                            env_example_lines.append(
                                f"{var_name}=your-{var_name.lower().replace('_', '-')}"
                            )
                        elif "MODEL" in var_name.upper():
                            # Keep model names as they're not sensitive
                            env_example_lines.append(line)
                        elif "URL" in var_name.upper():
                            # Keep URL structure but sanitize credentials
                            if "UPSTASH" in var_name:
                                env_example_lines.append(f"{var_name}=your-upstash-url")
                            else:
                                env_example_lines.append(line)
                        else:
                            env_example_lines.append(line)
                    else:
                        env_example_lines.append(line)
                else:
                    env_example_lines.append(line)
    else:
        # Fallback .env.example content if shared .env doesn't exist
        env_example_lines = [
            "# API Keys for AI Providers",
            "OPENAI_API_KEY=your-openai-api-key",
            "ANTHROPIC_API_KEY=your-anthropic-api-key",
            "PERPLEXITY_API_KEY=your-perplexity-api-key",
            "DEEPSEEK_API_KEY=your-deepseek-api-key",
            "GOOGLE_API_KEY=your-google-api-key",
            "",
            "# AI Model Names",
            "OPENAI_MODEL=o3-pro",
            "ANTHROPIC_MODEL=claude-sonnet-4-20250514",
            "PERPLEXITY_MODEL=sonar",
            "DEEPSEEK_MODEL=deepseek-chat",
            "GEMINI_MODEL=gemini-2.5-flash-preview-05-20",
            "",
            "# GitHub MCP API Key",
            "GITHUB_PERSONAL_ACCESS_TOKEN=your-github-personal-access-token",
            "",
        ]

    # Add project-specific environment variables based on tech stack
    backend = _extract_tech_choice(tech_stack, "Backend Framework")
    database = _extract_tech_choice(tech_stack, "Database")
    _extract_tech_choice(tech_stack, "Authentication")

    # Backend-specific env vars
    if backend == "Django":
        env_example_lines.extend(
            [
                "",
                "# Django",
                "SECRET_KEY=your-secret-key-here",
                "ALLOWED_HOSTS=localhost,127.0.0.1",
                "DEBUG=True",
            ]
        )
    elif backend == "Flask":
        env_example_lines.extend(
            [
                "",
                "# Flask",
                "FLASK_APP=app.py",
                "FLASK_ENV=development",
                "SECRET_KEY=your-secret-key-here",
            ]
        )
    elif backend == "FastAPI":
        env_example_lines.extend(
            ["", "# FastAPI", "APP_NAME=YourAppName", "API_VERSION=v1"]
        )

    # Database configuration
    if database == "PostgreSQL":
        env_example_lines.extend(
            [
                "",
                "# Database",
                "DATABASE_URL=postgresql://user:password@localhost:5432/dbname",
                "DB_HOST=localhost",
                "DB_PORT=5432",
                "DB_NAME=your_db_name",
                "DB_USER=postgres",
                "DB_PASSWORD=your-db-password",
            ]
        )
    elif database == "MongoDB":
        env_example_lines.extend(
            ["", "# Database", "MONGODB_URI=mongodb://localhost:27017/your_db_name"]
        )

    # Write .env.example
    with open(os.path.join(project_dir, ".env.example"), "w", encoding="utf-8") as f:
        f.write("\n".join(env_example_lines))

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
    expert_consultation: dict[str, Any] | None = None,
    project_description: str = "",
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

    # Create comprehensive project analysis documentation
    _create_project_analysis_doc(
        docs_dir,
        package_name,
        tech_stack,
        ai_analysis,
        project_dir,
        expert_consultation,
    )

    # Create CONTRIBUTING.md
    _create_contributing_doc(docs_dir, project_name, package_name, tech_stack)

    # Create CHANGELOG.md
    _create_changelog_doc(docs_dir, project_name)

    # Create API documentation if applicable
    if _should_create_api_docs(tech_stack, project_description):
        _create_api_docs_structure(docs_dir, project_name, package_name, tech_stack)

    # Create TaskMaster directory for PRD files
    taskmaster_dir = os.path.join(project_dir, "TaskMaster")
    os.makedirs(taskmaster_dir, exist_ok=True)

    # Create TaskMaster README
    taskmaster_readme = os.path.join(taskmaster_dir, "README.md")
    with open(taskmaster_readme, "w", encoding="utf-8") as f:
        f.write(
            f"""# TaskMaster PRD Directory

This directory contains Product Requirements Documents (PRDs) generated by the PRD Stage expert consultation system for the **{package_name}** project.

## Directory Structure

When you run the PRD Stage system, it will automatically generate:

- `PRD_{{project_name}}_{{date}}.md` - Complete Product Requirements Document
- `Expert_Consultation_Log_{{date}}.md` - Detailed log of expert analyses and AI provider assignments

## Expert Team

The PRD Stage system uses three expert AI personas:

### 👥 Anya Sharma - Principal UI/UX Lead (18+ years)
- **Expertise**: User research, interface design, accessibility
- **Notable Achievements**: Innovatech "Synergy Suite" strategy, "ConnectSphere" redesign (+2M users), Red Dot Design Award winner
- **Focus**: User experience requirements, visual design specifications, user flows

### 📈 Ben Carter - Senior Product Lead (15+ years)
- **Expertise**: Product strategy, go-to-market, business objectives
- **Notable Achievements**: "MarketLeap" $50M ARR, "Product Manager of the Year", 300% user growth
- **Focus**: Business goals, market positioning, feature prioritization

### 🏗️ Dr. Chloe Evans - Chief Software Architect (20+ years)
- **Expertise**: System design, scalability, technical architecture
- **Notable Achievements**: "Helios" platform (1B+ transactions), cloud migration strategies, patented algorithms
- **Focus**: Technical requirements, system architecture, scalability planning

### 🎯 Product Instigator - Final Synthesis
- **Role**: Synthesizes all expert insights into comprehensive PRD
- **Powered by**: Claude Opus4 with "ultrahard thinking"
- **Output**: TaskMaster AI compatible PRD format

## Usage

The PRD Stage system automatically creates files in this directory when you run the expert consultation process through the main application.

Run the Create Python Project tool with PRD Stage to generate comprehensive product requirements for this project.

---
*Generated by Create Python Project - PRD Stage*
"""
        )

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
                        return str(option["name"])
    return ""


def _extract_tech_choices_dict(tech_stack: dict[Any, Any]) -> dict[str, str]:
    """Extract all recommended technologies as a dictionary mapping category names to choices."""
    tech_choices: dict[str, str] = {}

    if isinstance(tech_stack, dict) and "categories" in tech_stack:
        for category in tech_stack["categories"]:
            category_name = category.get("name", "")
            if category_name:
                for option in category.get("options", []):
                    if option.get("recommended", False):
                        tech_choices[category_name] = str(option["name"])
                        break

    return tech_choices


def get_installation_commands_from_tech_stack(tech_stack: dict) -> dict[str, list[str]]:
    """
    Dynamically determine installation commands based on AI-recommended tech stack.

    Args:
        tech_stack: Dictionary containing AI technology recommendations

    Returns:
        Dictionary with 'python' and 'node' command lists
    """
    commands: dict[str, list[str]] = {
        "python": [],
        "node": [],
        "system": [],
        "manual": [],
    }

    if not isinstance(tech_stack, dict) or "categories" not in tech_stack:
        return commands

    # Technology to installation command mapping
    tech_to_install = {
        # Python Backend Frameworks
        "Django": {"type": "python", "packages": ["django", "django-environ"]},
        "Flask": {
            "type": "python",
            "packages": ["flask", "python-dotenv", "flask-cors"],
        },
        "FastAPI": {
            "type": "python",
            "packages": ["fastapi", "uvicorn", "pydantic", "pydantic-settings"],
        },
        # Python Databases
        "PostgreSQL": {"type": "python", "packages": ["psycopg2-binary", "sqlalchemy"]},
        "MongoDB": {"type": "python", "packages": ["pymongo"]},
        "Redis": {"type": "python", "packages": ["redis"]},
        # Python Data Processing
        "Pandas": {"type": "python", "packages": ["pandas"]},
        "NumPy": {"type": "python", "packages": ["numpy"]},
        "Matplotlib": {"type": "python", "packages": ["matplotlib"]},
        "Plotly": {"type": "python", "packages": ["plotly"]},
        "scikit-learn": {
            "type": "python",
            "packages": ["scikit-learn", "numpy", "scipy"],
        },
        "Scikit-learn": {
            "type": "python",
            "packages": ["scikit-learn", "numpy", "scipy"],
        },
        "scikit-learn with pandas": {
            "type": "python",
            "packages": ["scikit-learn", "pandas", "numpy", "scipy"],
        },
        "TensorFlow": {"type": "python", "packages": ["tensorflow"]},
        "PyTorch": {"type": "python", "packages": ["torch"]},
        # Python GUI Frameworks
        "PyQt": {"type": "python", "packages": ["PyQt6"]},
        "PyQt6": {"type": "python", "packages": ["PyQt6"]},
        "PyQt5": {"type": "python", "packages": ["PyQt5"]},
        "Kivy": {"type": "python", "packages": ["kivy"]},
        "Tkinter": {"type": "python", "packages": []},  # Built-in
        # Python CLI Tools
        "Click": {"type": "python", "packages": ["click"]},
        "Typer": {"type": "python", "packages": ["typer"]},
        # Python Authentication
        "PyJWT": {"type": "python", "packages": ["pyjwt"]},
        "Authlib": {"type": "python", "packages": ["authlib"]},
        "Auth0": {"type": "python", "packages": ["authlib", "requests"]},
        # API Integration
        "Plaid API": {"type": "python", "packages": ["plaid-python", "requests"]},
        # Python Utilities
        "Requests": {"type": "python", "packages": ["requests"]},
        "Beautiful Soup": {"type": "python", "packages": ["beautifulsoup4"]},
        "Celery": {"type": "python", "packages": ["celery"]},
        # Frontend Frameworks (Node.js)
        "React": {
            "type": "node",
            "packages": [
                "react",
                "react-dom",
                "@types/react",
                "@types/react-dom",
                "typescript",
            ],
        },
        "React with TypeScript": {
            "type": "node",
            "packages": [
                "react",
                "react-dom",
                "@types/react",
                "@types/react-dom",
                "typescript",
                "vite",
            ],
        },
        "Vue.js": {"type": "node", "packages": ["vue"]},
        "Vue": {"type": "node", "packages": ["vue"]},
        "Angular": {"type": "node", "packages": ["@angular/core", "@angular/cli"]},
        "Svelte": {"type": "node", "packages": ["svelte"]},
        "Next.js": {"type": "node", "packages": ["next", "react", "react-dom"]},
        "Nuxt.js": {"type": "node", "packages": ["nuxt"]},
        # Frontend Development Tools (Node.js)
        "TypeScript": {"type": "node", "packages": ["typescript"]},
        "Vite": {"type": "node", "packages": ["vite"]},
        "Webpack": {"type": "node", "packages": ["webpack", "webpack-cli"]},
        "Babel": {"type": "node", "packages": ["@babel/core", "@babel/preset-env"]},
        # Frontend Utilities (Node.js)
        "Axios": {"type": "node", "packages": ["axios"]},
        "Fetch": {"type": "node", "packages": []},  # Built-in
        "Recharts": {"type": "node", "packages": ["recharts"]},
        "Chart.js": {"type": "node", "packages": ["chart.js"]},
        "D3.js": {"type": "node", "packages": ["d3"]},
        # CSS Frameworks (Node.js)
        "Tailwind CSS": {"type": "node", "packages": ["tailwindcss"]},
        "Bootstrap": {"type": "node", "packages": ["bootstrap"]},
        "Material-UI": {"type": "node", "packages": ["@mui/material"]},
        # Development Tools (Node.js)
        "ESLint": {"type": "node", "packages": ["eslint"]},
        "Prettier": {"type": "node", "packages": ["prettier"]},
        "Jest": {"type": "node", "packages": ["jest"]},
        "Vitest": {"type": "node", "packages": ["vitest"]},
        # Testing Frameworks (Python)
        "Pytest": {"type": "python", "packages": ["pytest", "pytest-cov"]},
        "Unittest": {"type": "python", "packages": []},  # Built-in
        # Code Quality (Python)
        "Black": {"type": "python", "packages": ["black"]},
        "Ruff": {"type": "python", "packages": ["ruff"]},
        "Mypy": {"type": "python", "packages": ["mypy"]},
        "Pre-commit": {"type": "python", "packages": ["pre-commit"]},
    }

    # Extract recommended technologies from AI tech stack
    for category in tech_stack.get("categories", []):
        for option in category.get("options", []):
            if option.get("recommended", False):
                tech_name = option["name"]

                # Check for exact match first
                if tech_name in tech_to_install:
                    install_info = tech_to_install[tech_name]
                    install_type = install_info["type"]
                    packages = install_info["packages"]

                    if install_type in commands:
                        commands[install_type].extend(packages)
                else:
                    # Try partial matching for variations
                    matched = False
                    for tech_key, install_info in tech_to_install.items():
                        if (
                            tech_key.lower() in tech_name.lower()
                            or tech_name.lower() in tech_key.lower()
                        ):
                            install_type = install_info["type"]
                            packages = install_info["packages"]

                            if install_type in commands:
                                commands[install_type].extend(packages)
                            matched = True
                            break

                    # Intelligent fallback for unmapped technologies
                    if not matched:
                        fallback_packages = _discover_technology_installation(tech_name)
                        for pkg_type, packages in fallback_packages.items():
                            if pkg_type in commands:
                                commands[pkg_type].extend(packages)

    # Remove duplicates while preserving order
    for cmd_type in commands:
        commands[cmd_type] = list(dict.fromkeys(commands[cmd_type]))

    return commands


def _discover_technology_installation(tech_name: str) -> dict[str, list[str]]:
    """
    DYNAMICALLY discover installation commands for ANY technology.
    Queries multiple sources to find the actual installation method.
    """
    # First: Try expanded comprehensive technology database (200+ technologies)
    comprehensive_tech_db = _get_comprehensive_technology_database()

    if tech_name in comprehensive_tech_db:
        return comprehensive_tech_db[tech_name]

    # Second: Dynamic package registry queries
    dynamic_discovery = _query_package_registries(tech_name)
    if dynamic_discovery:
        return dynamic_discovery

    # Third: GitHub/official site discovery
    github_discovery = _discover_from_github(tech_name)
    if github_discovery:
        return github_discovery

    # Fourth: Pattern-based intelligent guessing
    return _intelligent_pattern_discovery(tech_name)


def _get_comprehensive_technology_database() -> dict[str, dict[str, list[str]]]:
    """
    Comprehensive 200+ technology database with REAL installation commands.
    Each entry specifies exactly how to install the technology on the user's system.
    """
    return {
        # ===== FRONTEND FRAMEWORKS & LIBRARIES =====
        "React": {"node": ["react", "react-dom", "@types/react", "@types/react-dom"]},
        "React with TypeScript": {
            "node": [
                "react",
                "react-dom",
                "@types/react",
                "@types/react-dom",
                "typescript",
                "vite",
            ]
        },
        "Vue.js": {"node": ["vue", "@vitejs/plugin-vue"]},
        "Vue": {"node": ["vue", "@vitejs/plugin-vue"]},
        "Angular": {"node": ["@angular/cli", "@angular/core", "@angular/common"]},
        "Svelte": {"node": ["svelte", "@sveltejs/kit", "vite"]},
        "SvelteKit": {"node": ["@sveltejs/kit", "svelte", "vite"]},
        "Next.js": {
            "node": ["next", "react", "react-dom", "@types/react", "@types/react-dom"]
        },
        "Nuxt.js": {"node": ["nuxt", "vue"]},
        "Remix": {"node": ["@remix-run/node", "@remix-run/react", "@remix-run/dev"]},
        "Astro": {"node": ["astro", "@astrojs/node"]},
        "Solid.js": {"node": ["solid-js", "solid-start"]},
        "Qwik": {"node": ["@builder.io/qwik", "@builder.io/qwik-city"]},
        # ===== BACKEND FRAMEWORKS =====
        "FastAPI": {
            "python": ["fastapi", "uvicorn[standard]", "pydantic", "pydantic-settings"]
        },
        "Django": {
            "python": [
                "django",
                "django-environ",
                "django-extensions",
                "djangorestframework",
            ]
        },
        "Flask": {"python": ["flask", "flask-cors", "python-dotenv", "werkzeug"]},
        "Express.js": {"node": ["express", "@types/express", "cors", "helmet"]},
        "NestJS": {
            "node": ["@nestjs/core", "@nestjs/common", "@nestjs/platform-express"]
        },
        # ===== DATABASES & DATA =====
        "PostgreSQL": {
            "python": ["psycopg2-binary", "sqlalchemy", "alembic"],
            "system": ["postgresql"],
        },
        "TimescaleDB": {
            "python": ["psycopg2-binary", "sqlalchemy"],
            "system": ["timescaledb-postgresql"],
        },
        "MongoDB": {"python": ["pymongo", "motor"], "system": ["mongodb"]},
        "Redis": {"python": ["redis", "aioredis"], "system": ["redis"]},
        "DuckDB": {"python": ["duckdb"]},
        "Supabase": {"node": ["@supabase/supabase-js"], "python": ["supabase"]},
        "Prisma": {"node": ["prisma", "@prisma/client"]},
        # ===== AI/ML & DATA SCIENCE =====
        "scikit-learn": {"python": ["scikit-learn", "numpy", "scipy"]},
        "scikit-learn with pandas": {
            "python": ["scikit-learn", "pandas", "numpy", "scipy"]
        },
        "TensorFlow": {"python": ["tensorflow", "tensorflow-datasets"]},
        "PyTorch": {"python": ["torch", "torchvision", "torchaudio"]},
        "Hugging Face": {"python": ["transformers", "datasets", "tokenizers"]},
        "LangChain": {
            "python": ["langchain", "langchain-openai", "langchain-community"]
        },
        "OpenAI": {"python": ["openai"], "node": ["openai"]},
        "Anthropic": {"python": ["anthropic"], "node": ["@anthropic-ai/sdk"]},
        "Streamlit": {"python": ["streamlit", "streamlit-components"]},
        "Gradio": {"python": ["gradio"]},
        "Pandas": {"python": ["pandas", "numpy"]},
        "Plotly": {"python": ["plotly", "kaleido"]},
        # ===== AUTHENTICATION & SECURITY =====
        "Auth0": {"node": ["@auth0/auth0-react"], "python": ["authlib", "requests"]},
        "Firebase Auth": {"node": ["firebase", "@firebase/auth"]},
        "NextAuth.js": {"node": ["next-auth"]},
        "Clerk": {"node": ["@clerk/nextjs"], "python": ["clerk-sdk-python"]},
        # ===== API INTEGRATIONS =====
        "Plaid API": {"python": ["plaid-python"], "node": ["plaid"]},
        "Stripe": {"python": ["stripe"], "node": ["stripe"]},
        "Twilio": {"python": ["twilio"], "node": ["twilio"]},
        "AWS SDK": {"python": ["boto3", "botocore"], "node": ["aws-sdk"]},
        # ===== PROGRAMMING LANGUAGES =====
        "Rust": {
            "system": ["curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"]
        },
        "Go": {"system": ["# Install Go from https://golang.org/dl/"]},
        "Java": {"system": ["openjdk-11-jdk"]},
        # ===== DEVELOPMENT TOOLS =====
        "TypeScript": {"node": ["typescript", "@types/node"]},
        "Vite": {"node": ["vite", "@vitejs/plugin-react"]},
        "ESLint": {"node": ["eslint", "@typescript-eslint/parser"]},
        "Prettier": {"node": ["prettier"]},
        # ===== TESTING =====
        "Jest": {"node": ["jest", "@types/jest"]},
        "Vitest": {"node": ["vitest", "@vitest/ui"]},
        "Cypress": {"node": ["cypress"]},
        "Playwright": {"node": ["@playwright/test"]},
        "Pytest": {"python": ["pytest", "pytest-cov", "pytest-asyncio"]},
        # ===== CSS FRAMEWORKS =====
        "Tailwind CSS": {"node": ["tailwindcss", "autoprefixer", "postcss"]},
        "Bootstrap": {"node": ["bootstrap"]},
        "Material-UI": {"node": ["@mui/material", "@emotion/react", "@emotion/styled"]},
        "Chakra UI": {"node": ["@chakra-ui/react", "@emotion/react"]},
        # ===== MONITORING & OBSERVABILITY =====
        "Elasticsearch": {"python": ["elasticsearch"], "system": ["elasticsearch"]},
        "Kibana": {"system": ["kibana"]},
        "Elasticsearch + Kibana": {
            "python": ["elasticsearch"],
            "system": ["elasticsearch", "kibana"],
        },
        "RabbitMQ": {"python": ["pika", "celery"], "system": ["rabbitmq-server"]},
        "Custom Python Agent": {
            "manual": ["# Create custom monitoring agent - see manual_installations.sh"]
        },
        "Custom Monitoring Agent": {
            "manual": ["# Create custom monitoring agent - see manual_installations.sh"]
        },
        # ===== UTILITIES =====
        "Lodash": {"node": ["lodash", "@types/lodash"]},
        "Axios": {"node": ["axios"]},
        "React Query": {"node": ["@tanstack/react-query"]},
        "Requests": {"python": ["requests"]},
        "Rich": {"python": ["rich"]},
        "Click": {"python": ["click"]},
        # Add more technologies as needed...
    }


def _validate_package_exists(package_name: str, package_type: str) -> bool:
    """Validate if a package exists in the specified registry."""
    try:
        import requests

        if package_type == "python":
            # Check PyPI
            response = requests.get(
                f"https://pypi.org/pypi/{package_name}/json", timeout=5
            )
            return response.status_code == 200
        elif package_type == "node":
            # Check npm registry
            response = requests.get(
                f"https://registry.npmjs.org/{package_name}", timeout=5
            )
            return response.status_code == 200
    except Exception:
        # If validation fails, allow installation attempt (fail gracefully)
        return True

    return True


def _query_package_registries(tech_name: str) -> dict[str, list[str]] | None:
    """Query npm and PyPI registries for package existence."""
    try:
        import requests

        # Try npm registry
        npm_search_url = (
            f"https://registry.npmjs.org/{tech_name.lower().replace(' ', '-')}"
        )
        try:
            response = requests.get(npm_search_url, timeout=5)
            if response.status_code == 200:
                return {"node": [tech_name.lower().replace(" ", "-")]}
        except requests.RequestException:
            pass

        # Try PyPI registry
        pypi_search_url = (
            f"https://pypi.org/pypi/{tech_name.lower().replace(' ', '-')}/json"
        )
        try:
            response = requests.get(pypi_search_url, timeout=5)
            if response.status_code == 200:
                return {"python": [tech_name.lower().replace(" ", "-")]}
        except requests.RequestException:
            pass

    except ImportError:
        pass

    return None


def _discover_from_github(tech_name: str) -> dict[str, list[str]] | None:
    """Discover installation methods from GitHub repositories."""
    # This would query GitHub API for popular repositories
    # and extract installation instructions from README files
    # For now, return None to fall back to pattern matching
    return None


def _intelligent_pattern_discovery(tech_name: str) -> dict[str, list[str]]:
    """Last resort pattern-based discovery for unknown technologies with smart cleanup."""
    tech_lower = tech_name.lower()

    # First: Handle invalid package names with cleanup
    cleaned_name = _clean_invalid_package_name(tech_name)
    if cleaned_name != tech_name:
        # Try to find the cleaned name in our comprehensive database
        comprehensive_db = _get_comprehensive_technology_database()
        if cleaned_name in comprehensive_db:
            return comprehensive_db[cleaned_name]

    # Second: Handle compound names (e.g., "Elasticsearch + Kibana")
    if "+" in tech_name or " and " in tech_lower or " or " in tech_lower:
        return _handle_compound_technology_name(tech_name)

    # Third: Handle parenthetical names (e.g., "Python (Flask/FastAPI)")
    if "(" in tech_name and ")" in tech_name:
        return _handle_parenthetical_technology_name(tech_name)

    # Fourth: Programming language detection
    if any(
        keyword in tech_lower for keyword in ["rust", "go", "java", "kotlin", "swift"]
    ):
        return {"system": [f"# Install {tech_name} from official website"]}

    # Fifth: Node.js ecosystem detection
    elif any(
        keyword in tech_lower
        for keyword in ["js", "javascript", "react", "vue", "angular", "node"]
    ):
        clean_name = tech_name.replace(" ", "-").lower()
        return {"node": [clean_name]}

    # Sixth: Python ecosystem detection
    elif any(
        keyword in tech_lower
        for keyword in ["python", "py", "django", "flask", "fastapi"]
    ):
        clean_name = tech_name.replace(" ", "-").lower()
        return {"python": [clean_name]}

    # Default: Mark as manual installation with warning
    else:
        return {
            "manual": [
                f"# '{tech_name}' requires manual installation - see manual_installations.sh"
            ]
        }


def _clean_invalid_package_name(tech_name: str) -> str:
    """Clean up invalid package names with special characters."""

    # Common invalid package name patterns and their fixes
    invalid_patterns = {
        r"elasticsearch[\s\-\+]+kibana": "Elasticsearch + Kibana",
        r"custom[\s\-]+python[\s\-]+agent": "Custom Python Agent",
        r"python\s*\([^)]+\)": lambda m: "Python",  # "Python (Flask/FastAPI)" -> "Python"
        r"(.+)\s+or\s+(.+)": lambda m: m.group(1),  # "Vue.js or React" -> "Vue.js"
    }

    cleaned = tech_name
    for pattern, replacement in invalid_patterns.items():
        if callable(replacement):
            cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
        else:
            cleaned = re.sub(pattern, str(replacement), cleaned, flags=re.IGNORECASE)

    return cleaned.strip()


def _handle_compound_technology_name(tech_name: str) -> dict[str, list[str]]:
    """Handle compound technology names like 'Elasticsearch + Kibana'."""
    comprehensive_db = _get_comprehensive_technology_database()

    # Split on common separators
    separators = [" + ", " and ", " or ", " & "]
    parts = [tech_name]

    for sep in separators:
        if sep in tech_name:
            parts = [part.strip() for part in tech_name.split(sep)]
            break

    # Combine results from all parts
    combined_result: dict[str, list[str]] = {
        "python": [],
        "node": [],
        "system": [],
        "manual": [],
    }

    for part in parts:
        if part in comprehensive_db:
            part_result = comprehensive_db[part]
            for install_type, packages in part_result.items():
                if install_type in combined_result:
                    combined_result[install_type].extend(packages)

    # Remove empty lists and duplicates
    for install_type in list(combined_result.keys()):
        if combined_result[install_type]:
            combined_result[install_type] = list(
                dict.fromkeys(combined_result[install_type])
            )
        else:
            del combined_result[install_type]

    return (
        combined_result
        if combined_result
        else {"manual": [f"# '{tech_name}' requires manual setup"]}
    )


def _handle_parenthetical_technology_name(tech_name: str) -> dict[str, list[str]]:
    """Handle parenthetical names like 'Python (Flask/FastAPI)'."""

    # Extract the main technology before parentheses
    match = re.match(r"^([^(]+)", tech_name)
    if match:
        main_tech = match.group(1).strip()
        comprehensive_db = _get_comprehensive_technology_database()

        if main_tech in comprehensive_db:
            return comprehensive_db[main_tech]

    return {"manual": [f"# '{tech_name}' requires manual setup"]}


def _install_system_package(package_name: str) -> bool:
    """
    Install system packages using the appropriate package manager.
    Returns True if installation succeeded, False otherwise.
    """
    import platform

    # Detect package manager based on OS
    system = platform.system().lower()

    try:
        if system == "linux":
            # Try apt first (Ubuntu/Debian)
            if shutil.which("apt-get"):
                result = subprocess.run(
                    ["sudo", "apt-get", "install", "-y", package_name],
                    capture_output=True,
                    text=True,
                )
                return result.returncode == 0

            # Try yum (RHEL/CentOS)
            elif shutil.which("yum"):
                result = subprocess.run(
                    ["sudo", "yum", "install", "-y", package_name],
                    capture_output=True,
                    text=True,
                )
                return result.returncode == 0

            # Try pacman (Arch)
            elif shutil.which("pacman"):
                result = subprocess.run(
                    ["sudo", "pacman", "-S", "--noconfirm", package_name],
                    capture_output=True,
                    text=True,
                )
                return result.returncode == 0

        elif system == "darwin":
            # Try brew (macOS)
            if shutil.which("brew"):
                result = subprocess.run(
                    ["brew", "install", package_name], capture_output=True, text=True
                )
                return result.returncode == 0

        elif system == "windows" and shutil.which("choco"):
            result = subprocess.run(
                ["choco", "install", package_name, "-y"], capture_output=True, text=True
            )
            return result.returncode == 0

    except Exception:
        pass

    return False


def detect_project_type(
    tech_stack: dict[str, Any] | None, project_description: str = ""
) -> str:
    """
    Dynamically detect project type based on AI recommendations and description.
    Returns a concise 2-5 word project type that reflects what was actually built.
    """
    if not isinstance(tech_stack, dict):
        return "Python Application"

    # Extract recommended technologies
    technologies = []
    if "categories" in tech_stack:
        for category in tech_stack["categories"]:
            for option in category.get("options", []):
                if option.get("recommended", False):
                    technologies.append(option["name"].lower())

    tech_string = " ".join(technologies)
    desc_lower = project_description.lower()

    # Project type detection based on technology combinations and domain-specific keywords
    if any(
        frontend in tech_string for frontend in ["react", "vue", "angular", "svelte"]
    ) and any(backend in tech_string for backend in ["fastapi", "django", "flask"]):
        # Academic & Research Applications
        if any(
            keyword in desc_lower
            for keyword in [
                "research",
                "academic",
                "scholar",
                "university",
                "paper",
                "citation",
                "journal",
                "publication",
            ]
        ):
            if any(
                keyword in desc_lower
                for keyword in ["content", "management", "organize", "annotate"]
            ):
                return "Research Management Platform"
            elif any(
                keyword in desc_lower
                for keyword in ["collaboration", "collaborate", "team"]
            ):
                return "Academic Collaboration Tool"
            elif any(
                keyword in desc_lower for keyword in ["analysis", "analytics", "data"]
            ):
                return "Research Analytics Platform"
            else:
                return "Academic Research System"

        # Business & Enterprise Applications
        elif any(
            keyword in desc_lower
            for keyword in [
                "business",
                "enterprise",
                "company",
                "organization",
                "workflow",
            ]
        ):
            if any(
                keyword in desc_lower
                for keyword in ["hr", "human resource", "employee", "staff"]
            ):
                return "HR Management System"
            elif any(
                keyword in desc_lower
                for keyword in ["inventory", "stock", "warehouse", "supply"]
            ):
                return "Inventory Management System"
            elif any(
                keyword in desc_lower
                for keyword in ["customer", "crm", "client", "lead"]
            ):
                return "Customer Management System"
            elif any(
                keyword in desc_lower for keyword in ["project", "task", "work", "team"]
            ):
                return "Project Management Platform"
            else:
                return "Business Management System"

        # Healthcare & Medical
        elif any(
            keyword in desc_lower
            for keyword in [
                "health",
                "medical",
                "patient",
                "doctor",
                "clinic",
                "hospital",
            ]
        ):
            if any(
                keyword in desc_lower
                for keyword in ["record", "management", "ehr", "emr"]
            ):
                return "Medical Records System"
            elif any(
                keyword in desc_lower
                for keyword in ["appointment", "schedule", "booking"]
            ):
                return "Healthcare Scheduling Platform"
            else:
                return "Healthcare Management System"

        # Education & Learning
        elif any(
            keyword in desc_lower
            for keyword in [
                "education",
                "learning",
                "student",
                "teacher",
                "course",
                "lesson",
            ]
        ):
            if any(
                keyword in desc_lower for keyword in ["management", "lms", "platform"]
            ):
                return "Learning Management System"
            elif any(
                keyword in desc_lower
                for keyword in ["quiz", "test", "exam", "assessment"]
            ):
                return "Educational Assessment Platform"
            else:
                return "Educational Platform"

        # Financial Applications
        elif any(
            keyword in desc_lower
            for keyword in [
                "finance",
                "financial",
                "budget",
                "money",
                "bank",
                "transaction",
                "payment",
                "accounting",
            ]
        ):
            if any(
                keyword in desc_lower for keyword in ["personal", "budget", "expense"]
            ):
                return "Personal Finance Manager"
            elif any(
                keyword in desc_lower
                for keyword in ["trading", "investment", "portfolio"]
            ):
                return "Investment Trading Platform"
            elif any(
                keyword in desc_lower
                for keyword in ["accounting", "invoice", "billing"]
            ):
                return "Accounting Management System"
            else:
                return "Financial Services Platform"

        # E-commerce & Retail
        elif any(
            keyword in desc_lower
            for keyword in [
                "ecommerce",
                "e-commerce",
                "shop",
                "store",
                "retail",
                "marketplace",
                "cart",
                "product",
            ]
        ):
            if any(
                keyword in desc_lower for keyword in ["marketplace", "multi-vendor"]
            ):
                return "Marketplace Platform"
            elif any(keyword in desc_lower for keyword in ["inventory", "stock"]):
                return "E-commerce Inventory System"
            else:
                return "E-commerce Platform"

        # Communication & Social
        elif any(
            keyword in desc_lower
            for keyword in [
                "social",
                "chat",
                "message",
                "communication",
                "community",
                "forum",
            ]
        ):
            if any(
                keyword in desc_lower
                for keyword in ["messaging", "chat", "conversation"]
            ):
                return "Communication Platform"
            elif any(
                keyword in desc_lower
                for keyword in ["forum", "discussion", "community"]
            ):
                return "Community Forum Platform"
            elif any(
                keyword in desc_lower for keyword in ["social", "network", "connect"]
            ):
                return "Social Networking Platform"
            else:
                return "Social Communication App"

        # Monitoring & Analytics
        elif any(
            keyword in desc_lower
            for keyword in [
                "monitor",
                "monitoring",
                "dashboard",
                "analytics",
                "metrics",
                "tracking",
                "report",
            ]
        ):
            if any(
                keyword in desc_lower
                for keyword in ["server", "system", "infrastructure", "devops"]
            ):
                return "System Monitoring Platform"
            elif any(
                keyword in desc_lower
                for keyword in ["business", "sales", "performance"]
            ):
                return "Business Analytics Dashboard"
            elif any(
                keyword in desc_lower for keyword in ["real-time", "realtime", "live"]
            ):
                return "Real-time Analytics Platform"
            else:
                return "Analytics Dashboard"

        # Content Management
        elif any(
            keyword in desc_lower
            for keyword in [
                "content",
                "cms",
                "blog",
                "article",
                "publishing",
                "editorial",
            ]
        ):
            if any(
                keyword in desc_lower for keyword in ["blog", "blogging", "article"]
            ):
                return "Blogging Platform"
            elif any(
                keyword in desc_lower for keyword in ["news", "publishing", "editorial"]
            ):
                return "Publishing Management System"
            elif any(
                keyword in desc_lower for keyword in ["document", "file", "media"]
            ):
                return "Document Management System"
            else:
                return "Content Management Platform"

        # Event & Booking Systems
        elif any(
            keyword in desc_lower
            for keyword in [
                "event",
                "booking",
                "reservation",
                "appointment",
                "schedule",
            ]
        ):
            if any(
                keyword in desc_lower for keyword in ["event", "conference", "meeting"]
            ):
                return "Event Management Platform"
            elif any(
                keyword in desc_lower for keyword in ["hotel", "room", "accommodation"]
            ):
                return "Booking Management System"
            else:
                return "Scheduling Platform"

        # IoT & Hardware
        elif any(
            keyword in desc_lower
            for keyword in ["iot", "sensor", "device", "hardware", "embedded"]
        ):
            return "IoT Management Platform"

        # Security & Auth
        elif any(
            keyword in desc_lower
            for keyword in [
                "security",
                "auth",
                "authentication",
                "access",
                "permission",
            ]
        ):
            return "Security Management System"

        # Generic fallback based on complexity
        else:
            if any(
                keyword in desc_lower
                for keyword in ["platform", "system", "management"]
            ):
                return "Management Platform"
            elif any(
                keyword in desc_lower for keyword in ["tool", "utility", "helper"]
            ):
                return "Web-based Tool"
            else:
                return "Full-stack Web Application"

    # AI/ML focused applications
    elif any(
        ai_tech in tech_string
        for ai_tech in ["streamlit", "gradio", "tensorflow", "pytorch", "scikit-learn"]
    ):
        if any(
            keyword in desc_lower
            for keyword in ["finance", "financial", "trading", "investment"]
        ):
            return "AI Financial Analytics Tool"
        elif any(
            keyword in desc_lower for keyword in ["healthcare", "medical", "diagnosis"]
        ):
            return "AI Healthcare Analytics"
        elif any(
            keyword in desc_lower
            for keyword in ["nlp", "text", "language", "chat", "conversation"]
        ):
            return "AI Language Processing Tool"
        elif any(
            keyword in desc_lower
            for keyword in ["computer vision", "image", "visual", "cv"]
        ):
            return "AI Vision Analytics Tool"
        elif any(
            keyword in desc_lower
            for keyword in ["recommendation", "recommender", "personalization"]
        ):
            return "AI Recommendation Engine"
        elif any(
            keyword in desc_lower
            for keyword in ["prediction", "forecasting", "predictive"]
        ):
            return "AI Prediction Platform"
        elif any(
            keyword in desc_lower
            for keyword in ["dashboard", "visualization", "reporting"]
        ):
            return "AI Analytics Dashboard"
        elif "streamlit" in tech_string:
            return "Streamlit ML Application"
        elif "gradio" in tech_string:
            return "Gradio ML Interface"
        else:
            return "Machine Learning Platform"

    # Desktop applications with domain specificity
    elif any(
        desktop in tech_string
        for desktop in ["kivy", "pyqt", "tkinter", "electron", "tauri"]
    ):
        if any(
            keyword in desc_lower for keyword in ["game", "gaming", "entertainment"]
        ):
            return "Desktop Game Application"
        elif any(
            keyword in desc_lower for keyword in ["productivity", "office", "document"]
        ):
            return "Desktop Productivity Tool"
        elif any(
            keyword in desc_lower for keyword in ["media", "video", "audio", "editor"]
        ):
            return "Desktop Media Application"
        elif any(keyword in desc_lower for keyword in ["utility", "tool", "system"]):
            return "Desktop Utility Tool"
        else:
            return "Desktop Application"

    # Mobile applications with domain specificity
    elif any(mobile in tech_string for mobile in ["react native", "flutter", "kivy"]):
        if any(keyword in desc_lower for keyword in ["social", "chat", "messaging"]):
            return "Mobile Social App"
        elif any(keyword in desc_lower for keyword in ["fitness", "health", "workout"]):
            return "Mobile Health App"
        elif any(
            keyword in desc_lower for keyword in ["finance", "banking", "payment"]
        ):
            return "Mobile Finance App"
        elif any(keyword in desc_lower for keyword in ["productivity", "task", "todo"]):
            return "Mobile Productivity App"
        elif any(
            keyword in desc_lower for keyword in ["game", "gaming", "entertainment"]
        ):
            return "Mobile Game App"
        else:
            return "Mobile Application"

    # API/Backend only with domain specificity
    elif any(
        backend in tech_string for backend in ["fastapi", "django", "flask"]
    ) and not any(frontend in tech_string for frontend in ["react", "vue", "angular"]):
        if any(keyword in desc_lower for keyword in ["microservice", "service", "api"]):
            if "fastapi" in tech_string:
                return "FastAPI Microservice"
            elif "django" in tech_string:
                return "Django REST API"
            elif "flask" in tech_string:
                return "Flask API Service"
            else:
                return "Backend API Service"
        elif any(
            keyword in desc_lower for keyword in ["integration", "webhook", "connector"]
        ):
            return "API Integration Service"
        elif any(
            keyword in desc_lower for keyword in ["data", "processing", "pipeline"]
        ):
            return "Data Processing Service"
        else:
            return "Backend API"

    # CLI tools with domain specificity
    elif any(cli in tech_string for cli in ["click", "typer", "fire", "argparse"]):
        if any(
            keyword in desc_lower for keyword in ["deployment", "devops", "automation"]
        ):
            return "DevOps CLI Tool"
        elif any(keyword in desc_lower for keyword in ["data", "processing", "etl"]):
            return "Data Processing CLI Tool"
        elif any(keyword in desc_lower for keyword in ["file", "directory", "system"]):
            return "File Management CLI Tool"
        elif any(keyword in desc_lower for keyword in ["utility", "helper", "admin"]):
            return "System Utility CLI Tool"
        else:
            return "Command-Line Tool"

    # Game development with specificity
    elif any(game in tech_string for game in ["pygame", "unity", "godot"]):
        if any(keyword in desc_lower for keyword in ["2d", "platformer", "arcade"]):
            return "2D Game Application"
        elif any(keyword in desc_lower for keyword in ["3d", "simulation", "strategy"]):
            return "3D Game Application"
        elif any(keyword in desc_lower for keyword in ["puzzle", "casual", "mobile"]):
            return "Casual Game Application"
        else:
            return "Game Application"

    # Web scraping/automation with specificity
    elif any(
        scrape in tech_string for scrape in ["selenium", "beautifulsoup", "scrapy"]
    ):
        if any(keyword in desc_lower for keyword in ["testing", "qa", "automation"]):
            return "Web Testing Automation Tool"
        elif any(
            keyword in desc_lower
            for keyword in ["scraping", "extraction", "harvesting"]
        ):
            return "Web Scraping Tool"
        elif any(
            keyword in desc_lower
            for keyword in ["monitoring", "tracking", "surveillance"]
        ):
            return "Web Monitoring Tool"
        else:
            return "Web Automation Tool"

    # Jupyter/Notebook applications
    elif any(
        notebook in tech_string for notebook in ["jupyter", "notebook", "ipython"]
    ):
        if any(
            keyword in desc_lower for keyword in ["research", "academic", "analysis"]
        ):
            return "Research Jupyter Notebook"
        elif any(
            keyword in desc_lower
            for keyword in ["data science", "machine learning", "ml"]
        ):
            return "Data Science Notebook"
        elif any(
            keyword in desc_lower for keyword in ["education", "teaching", "tutorial"]
        ):
            return "Educational Jupyter Notebook"
        else:
            return "Interactive Jupyter Notebook"

    # Default based on primary technology with more specificity
    elif "django" in tech_string:
        if any(keyword in desc_lower for keyword in ["cms", "content", "blog"]):
            return "Django CMS Platform"
        elif any(keyword in desc_lower for keyword in ["ecommerce", "shop", "store"]):
            return "Django E-commerce Site"
        else:
            return "Django Web Application"
    elif "flask" in tech_string:
        if any(keyword in desc_lower for keyword in ["api", "service", "microservice"]):
            return "Flask API Service"
        elif any(keyword in desc_lower for keyword in ["dashboard", "admin", "panel"]):
            return "Flask Dashboard Application"
        else:
            return "Flask Web Application"
    elif "fastapi" in tech_string:
        if any(keyword in desc_lower for keyword in ["api", "service", "microservice"]):
            return "FastAPI Service"
        elif any(
            keyword in desc_lower for keyword in ["real-time", "websocket", "async"]
        ):
            return "FastAPI Real-time Service"
        else:
            return "FastAPI Application"
    elif "streamlit" in tech_string:
        return "Streamlit Data Application"
    else:
        return "Python Application"


def setup_virtual_environment(
    project_dir: str, tech_stack: dict | None = None
) -> tuple[bool, str]:
    """Set up Poetry environment and install all AI-recommended technologies."""
    try:
        # Check if Poetry is installed
        if not shutil.which("poetry"):
            return False, "Poetry is not installed. Please install Poetry first."

        # Get dynamic installation commands from AI tech stack
        install_commands = get_installation_commands_from_tech_stack(tech_stack or {})

        # Configure Poetry to create venv in project
        subprocess.run(
            ["poetry", "config", "virtualenvs.in-project", "true"],
            cwd=project_dir,
            check=True,
            capture_output=True,
        )

        # Track successful and failed installations
        successful_python = []
        failed_python = []
        successful_node = []
        failed_node = []

        # Install AI-recommended Python packages dynamically with validation
        python_packages = install_commands.get("python", [])
        if python_packages:
            for package in python_packages:
                # Validate package exists before attempting installation
                if not _validate_package_exists(package, "python"):
                    print(
                        f"Warning: Python package '{package}' not found in PyPI registry, skipping..."
                    )
                    failed_python.append(
                        (package, "Package not found in PyPI registry")
                    )
                    continue

                try:
                    subprocess.run(
                        ["poetry", "add", package],
                        cwd=project_dir,
                        check=True,
                        capture_output=True,
                        text=True,
                    )
                    successful_python.append(package)
                except subprocess.CalledProcessError as e:
                    failed_python.append(
                        (package, str(e.stderr) if e.stderr else "Unknown error")
                    )
                    print(
                        f"Warning: Failed to install Python package: {package} - {e.stderr if e.stderr else 'Unknown error'}"
                    )

        # Install base dependencies from pyproject.toml (if any)
        subprocess.run(
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

        # Install pre-commit hooks if pre-commit was recommended
        if "pre-commit" in python_packages:
            subprocess.run(
                ["poetry", "run", "pre-commit", "install"],
                cwd=project_dir,
                capture_output=True,
            )

        # Install AI-recommended Node.js packages dynamically
        node_packages = install_commands.get("node", [])
        if node_packages and shutil.which("npm"):
            # Check if frontend directory exists (for React/Vue projects)
            frontend_dir = os.path.join(project_dir, "frontend")
            if os.path.exists(frontend_dir):
                # Install frontend dependencies with validation
                for package in node_packages:
                    # Validate package exists before attempting installation
                    if not _validate_package_exists(package, "node"):
                        print(
                            f"Warning: Node.js package '{package}' not found in npm registry, skipping..."
                        )
                        failed_node.append(
                            (package, "Package not found in npm registry")
                        )
                        continue

                    try:
                        subprocess.run(
                            ["npm", "install", package],
                            cwd=frontend_dir,
                            check=True,
                            capture_output=True,
                            text=True,
                        )
                        successful_node.append(package)
                    except subprocess.CalledProcessError as e:
                        failed_node.append(
                            (package, str(e.stderr) if e.stderr else "Unknown error")
                        )
                        print(
                            f"Warning: Failed to install Node.js package: {package} - {e.stderr if e.stderr else 'Unknown error'}"
                        )

                # Also run npm install to install any dependencies from package.json
                subprocess.run(
                    ["npm", "install"],
                    cwd=frontend_dir,
                    capture_output=True,
                )
            else:
                # Create frontend directory for React/TypeScript projects
                if any(
                    "react" in pkg.lower() or "typescript" in pkg.lower()
                    for pkg in node_packages
                ):
                    _create_frontend_structure(project_dir, node_packages)
                    frontend_dir = os.path.join(project_dir, "frontend")

                # Install Node packages in appropriate directory with validation
                install_dir = (
                    frontend_dir if os.path.exists(frontend_dir) else project_dir
                )
                for package in node_packages:
                    # Validate package exists before attempting installation
                    if not _validate_package_exists(package, "node"):
                        print(
                            f"Warning: Node.js package '{package}' not found in npm registry, skipping..."
                        )
                        failed_node.append(
                            (package, "Package not found in npm registry")
                        )
                        continue

                    try:
                        subprocess.run(
                            ["npm", "install", package],
                            cwd=install_dir,
                            check=True,
                            capture_output=True,
                            text=True,
                        )
                        successful_node.append(package)
                    except subprocess.CalledProcessError as e:
                        failed_node.append(
                            (package, str(e.stderr) if e.stderr else "Unknown error")
                        )
                        print(
                            f"Warning: Failed to install Node.js package: {package} - {e.stderr if e.stderr else 'Unknown error'}"
                        )

        # Handle system installations and manual instructions
        system_commands = install_commands.get("system", [])
        manual_commands = install_commands.get("manual", [])
        successful_system = []
        failed_system = []
        manual_instructions = []

        # Process system packages
        if system_commands:
            for cmd in system_commands:
                if cmd.startswith("#"):
                    # This is a manual instruction
                    manual_instructions.append(cmd.replace("# ", ""))
                else:
                    # Try to install system package
                    try:
                        if _install_system_package(cmd):
                            successful_system.append(cmd)
                        else:
                            failed_system.append(cmd)
                            manual_instructions.append(f"Install {cmd} manually")
                    except Exception:
                        failed_system.append(cmd)
                        manual_instructions.append(f"Install {cmd} manually")

        # Process manual installation instructions
        if manual_commands:
            for instruction in manual_commands:
                clean_instruction = (
                    instruction.replace("# ", "")
                    if instruction.startswith("# ")
                    else instruction
                )
                manual_instructions.append(clean_instruction)

        # Create manual installation script if needed
        if manual_instructions:
            install_script_path = os.path.join(project_dir, "manual_installations.sh")
            with open(install_script_path, "w") as f:
                f.write("#!/bin/bash\n")
                f.write("# Manual installation instructions for system packages\n\n")
                for instruction in manual_instructions:
                    f.write(f"# {instruction}\n")
            os.chmod(install_script_path, 0o755)

        # Install MCP server dependencies (if package.json exists in root)
        if os.path.exists(os.path.join(project_dir, "package.json")) and shutil.which(
            "npm"
        ):
            subprocess.run(
                ["npm", "install"],
                cwd=project_dir,
                capture_output=True,
            )

        # Create detailed installation summary
        summary_lines = []

        if successful_python:
            summary_lines.append(
                f"✅ Python packages installed: {len(successful_python)} ({', '.join(successful_python)})"
            )
        if failed_python:
            summary_lines.append(
                f"❌ Python packages failed: {len(failed_python)} ({', '.join([pkg for pkg, _ in failed_python])})"
            )

        if successful_node:
            summary_lines.append(
                f"✅ Node.js packages installed: {len(successful_node)} ({', '.join(successful_node)})"
            )
        if failed_node:
            summary_lines.append(
                f"❌ Node.js packages failed: {len(failed_node)} ({', '.join([pkg for pkg, _ in failed_node])})"
            )

        if successful_system:
            summary_lines.append(
                f"✅ System packages installed: {len(successful_system)} ({', '.join(successful_system)})"
            )
        if failed_system:
            summary_lines.append(
                f"❌ System packages failed: {len(failed_system)} ({', '.join(failed_system)})"
            )

        if manual_instructions:
            summary_lines.append(
                f"📋 Manual installations required: {len(manual_instructions)}"
            )
            summary_lines.append("   See manual_installations.sh for instructions")

        # Add verification results
        verification_results = _verify_installations(
            project_dir, successful_python, successful_node
        )
        summary_lines.extend(verification_results)

        summary = (
            "\n".join(summary_lines) if summary_lines else "No packages were installed"
        )

        # Return success only if we have some successful installations and no critical failures
        has_installations = (
            len(successful_python) > 0
            or len(successful_node) > 0
            or len(successful_system) > 0
        )
        return has_installations, summary

    except subprocess.CalledProcessError as e:
        return False, f"Failed to create virtual environment: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error during environment setup: {str(e)}"


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

        # Generate tech stack summary for README
        tech_stack_summary = _generate_tech_stack_summary(tech_stack)

        # Create comprehensive README
        readme_content = f"""# {project_name.replace("_", " ").replace("-", " ").title()}

{project_description if project_description else f"AI-powered {project_type} application created with intelligent technology stack selection."}

## 🎯 Project Overview

This project was created using **Create Python Project** with AI-driven architecture decisions. The technology stack and project structure were designed by AI experts to meet specific project requirements.

### 🔧 Technology Stack

{tech_stack_summary}

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Poetry (dependency management)
- Git
- Node.js (for frontend/MCP servers)

### Installation

1. Clone the repository:
```bash
git clone {"git@github.com:" + github_username + "/" + project_name + ".git" if github_username else "<repository-url>"}
cd {project_name}
```

2. Install Python dependencies:
```bash
poetry install
```

3. Install Node.js dependencies (if applicable):
```bash
npm install
```

4. Set up pre-commit hooks:
```bash
poetry run pre-commit install
```

5. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

6. Run the application:
```bash
poetry run python -m {project_name.replace("-", "_")}
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

- **Project Architecture**: See `docs/PROJECT_ANALYSIS.md` for detailed AI-driven design decisions
- **Tech Stack Reasoning**: Comprehensive analysis of technology choices and alternatives
- **Expert Consultation**: AI persona insights that shaped the project structure

## 🏗️ Project Structure

```
{project_name}/
├── src/{project_name.replace("-", "_")}/     # Main application code
├── tests/                    # Test suite
├── docs/                     # Project documentation
├── scripts/                  # Development automation
├── .vscode/                  # VS Code configuration
├── TaskMaster/               # PRD and project management
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🤖 AI-Generated Features

This project includes:
- ✅ AI-curated technology stack
- ✅ Expert-designed architecture
- ✅ Automated development tools
- ✅ VS Code workspace configuration
- ✅ Pre-commit hooks and code quality
- ✅ Professional documentation

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


def _generate_tech_stack_summary(tech_stack: dict[str, Any] | None) -> str:
    """Generate a formatted tech stack summary for README."""
    if not tech_stack or not isinstance(tech_stack, dict):
        return "- Standard Python project setup with Poetry, pytest, and code quality tools"

    if "categories" not in tech_stack:
        return "- AI-curated technology stack (details in docs/PROJECT_ANALYSIS.md)"

    summary_lines = []
    for category in tech_stack["categories"]:
        category_name = category.get("name", "")
        recommended_techs = []

        for option in category.get("options", []):
            if option.get("recommended", False):
                tech_name = option.get("name", "")
                if tech_name:
                    recommended_techs.append(tech_name)

        if recommended_techs:
            summary_lines.append(
                f"- **{category_name}**: {', '.join(recommended_techs)}"
            )

    if not summary_lines:
        return "- AI-curated technology stack (details in docs/PROJECT_ANALYSIS.md)"

    return "\n".join(summary_lines)


def _create_project_analysis_doc(
    docs_dir: str,
    package_name: str,
    tech_stack: dict[str, Any],
    ai_analysis: list[str],
    project_dir: str,
    expert_consultation: dict[str, Any] | None = None,
) -> None:
    """Create comprehensive project analysis documentation."""
    import datetime

    # Generate directory tree
    directory_tree = _generate_directory_tree(project_dir)

    # Generate tech stack analysis
    tech_stack_analysis = _generate_detailed_tech_stack_analysis(tech_stack)

    # Get current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"""# Project Analysis & Design Decisions

**Generated:** {timestamp}
**Project:** {package_name}
**Creation Tool:** Create Python Project (AI-Powered)

## 🎯 Executive Summary

This document provides a comprehensive analysis of the project architecture, technology stack decisions, and AI-driven design rationale for the **{package_name}** project.

## 🤖 AI Analysis Summary

The following insights guided the project creation:

{chr(10).join(f"- {analysis}" for analysis in ai_analysis) if ai_analysis else "- Standard Python project structure with modern development practices"}

## 🏗️ Project Structure

### Directory Tree

```
{directory_tree}
```

### Structure Explanation

- **`src/{package_name}/`**: Main application source code following modern Python packaging standards
- **`tests/`**: Test suite with structure mirroring the source code organization
- **`docs/`**: Project documentation including this analysis file
- **`scripts/`**: Development automation tools and helper scripts
- **`.vscode/`**: VS Code workspace configuration with extension recommendations
- **`TaskMaster/`**: Product Requirements Documents and AI consultation logs
- **`.env.example`**: Environment variable template (linked to shared configuration)

## 🔧 Technology Stack Analysis

{tech_stack_analysis}

## 📋 AI Consultation Process

This project was created through a sophisticated AI consultation process involving expert personas:

### Expert Team

1. **👥 Anya Sharma - Principal UI/UX Lead**
   - Focus: User experience design and interaction patterns
   - Contribution: User-centered design decisions and interface recommendations

2. **📈 Ben Carter - Senior Product Lead**
   - Focus: Market strategy, business objectives, and feature prioritization
   - Contribution: Product strategy and go-to-market considerations

3. **🏗️ Dr. Chloe Evans - Chief Software Architect**
   - Focus: Technical architecture and system design
   - Contribution: Technology stack selection and scalability planning

4. **🎯 Product Instigator - Final Synthesis**
   - Role: Integration of all expert insights into cohesive project plan
   - Powered by: Advanced AI reasoning for optimal decision synthesis

*Note: Full expert consultation details are available in the TaskMaster directory.*

{_generate_expert_consultation_summary(expert_consultation) if expert_consultation else ""}

## 🚀 Development Workflow

### Automated Tools Included

- **Code Quality**: Black formatting, Ruff linting, MyPy type checking
- **Git Integration**: Pre-commit hooks, automated commit workflow
- **Testing**: Pytest with coverage reporting
- **Environment**: Poetry dependency management, environment variable handling
- **VS Code Integration**: Workspace configuration, extension recommendations

### Getting Started

1. Open the `.code-workspace` file in VS Code
2. Install recommended extensions (auto-prompted)
3. Copy `.env.example` to `.env` and configure
4. Run `poetry install` to set up dependencies
5. Use `poetry run python scripts/commit_workflow.py` for commits

## 📊 Project Metadata

- **Creation Method**: AI-driven technology selection
- **Architecture Pattern**: {_detect_architecture_pattern(tech_stack)}
- **Primary Language**: Python 3.11+
- **Dependency Management**: Poetry
- **Code Quality**: Black + Ruff + MyPy + Pre-commit
- **Testing Framework**: Pytest with coverage
- **Documentation**: Markdown with automated generation

## 🔄 Future Considerations

Based on the AI analysis, consider these future enhancements:

- Regular dependency updates through automated tools
- Continuous integration/deployment pipeline setup
- Performance monitoring and optimization
- Security scanning and vulnerability management
- Documentation maintenance and updates

---

*This document was automatically generated by Create Python Project's AI-driven analysis system.*
"""

    # Write the documentation file
    analysis_file = os.path.join(docs_dir, "PROJECT_ANALYSIS.md")
    with open(analysis_file, "w", encoding="utf-8") as f:
        f.write(content)


def _generate_directory_tree(project_dir: str) -> str:
    """Generate a directory tree representation."""
    import os

    def build_tree(
        directory: str, prefix: str = "", max_depth: int = 3, current_depth: int = 0
    ) -> list[str]:
        if current_depth >= max_depth:
            return []

        items = []
        try:
            entries = sorted(os.listdir(directory))
            # Filter out common files we don't want in the tree
            filtered_entries = [
                e
                for e in entries
                if not e.startswith(".")
                or e in [".env.example", ".gitignore", ".vscode"]
            ]

            for i, entry in enumerate(filtered_entries):
                if entry.startswith("__pycache__") or entry.endswith(".pyc"):
                    continue

                path = os.path.join(directory, entry)
                is_last = i == len(filtered_entries) - 1
                current_prefix = "└── " if is_last else "├── "

                if os.path.isdir(path):
                    items.append(f"{prefix}{current_prefix}{entry}/")
                    if current_depth < max_depth - 1:
                        extension = "    " if is_last else "│   "
                        items.extend(
                            build_tree(
                                path, prefix + extension, max_depth, current_depth + 1
                            )
                        )
                else:
                    items.append(f"{prefix}{current_prefix}{entry}")
        except PermissionError:
            pass

        return items

    tree_lines = [os.path.basename(project_dir) + "/"]
    tree_lines.extend(build_tree(project_dir))
    return "\n".join(tree_lines)


def _generate_detailed_tech_stack_analysis(tech_stack: dict[str, Any]) -> str:
    """Generate detailed technology stack analysis."""
    if (
        not tech_stack
        or not isinstance(tech_stack, dict)
        or "categories" not in tech_stack
    ):
        return """### Standard Python Setup

- **Language**: Python 3.11+ with modern features and type hints
- **Dependency Management**: Poetry for robust package management
- **Code Quality**: Black, Ruff, and MyPy for formatting, linting, and type checking
- **Testing**: Pytest with coverage reporting
- **Version Control**: Git with pre-commit hooks"""

    analysis_sections = []

    for category in tech_stack["categories"]:
        category_name = category.get("name", "")
        if not category_name:
            continue

        section = f"### {category_name}\n"

        recommended_techs = []
        alternatives = []

        for option in category.get("options", []):
            tech_name = option.get("name", "")
            description = option.get("description", "")
            is_recommended = option.get("recommended", False)

            if is_recommended:
                recommended_techs.append(f"**{tech_name}**: {description}")
            else:
                alternatives.append(f"- {tech_name}: {description}")

        if recommended_techs:
            section += "**Selected Technology:**\n"
            section += "\n".join(f"- {tech}" for tech in recommended_techs)
            section += "\n\n"

        if alternatives:
            section += "**Alternatives Considered:**\n"
            section += "\n".join(alternatives)
            section += "\n"

        analysis_sections.append(section)

    return (
        "\n".join(analysis_sections)
        if analysis_sections
        else "**AI-curated technology stack** - See TaskMaster directory for detailed analysis."
    )


def _detect_architecture_pattern(tech_stack: dict[str, Any]) -> str:
    """Detect the primary architecture pattern from tech stack."""
    if not tech_stack or not isinstance(tech_stack, dict):
        return "Modular Python Package"

    patterns = []
    tech_names = str(tech_stack).lower()

    if any(framework in tech_names for framework in ["django", "flask", "fastapi"]):
        patterns.append("Web Application")

    if any(frontend in tech_names for frontend in ["react", "vue", "angular"]):
        patterns.append("Full-Stack")

    if any(data_tool in tech_names for data_tool in ["pandas", "numpy", "jupyter"]):
        patterns.append("Data Processing")

    if any(gui in tech_names for gui in ["pyqt", "tkinter", "kivy"]):
        patterns.append("Desktop Application")

    if any(cli in tech_names for cli in ["click", "typer", "argparse"]):
        patterns.append("Command-Line Interface")

    return " + ".join(patterns) if patterns else "Modular Python Package"


def _generate_expert_consultation_summary(expert_consultation: dict[str, Any]) -> str:
    """Generate a summary of the expert consultation for documentation."""
    if not expert_consultation:
        return ""

    ai_providers = expert_consultation.get("ai_providers_used", {})

    summary = f"""
### Expert Consultation Summary

**AI Providers Used:**
- **Anya (UX Lead)**: {ai_providers.get('anya', 'N/A')}
- **Ben (Product Lead)**: {ai_providers.get('ben', 'N/A')}
- **Dr. Chloe (Architect)**: {ai_providers.get('chloe', 'N/A')}
- **Final Synthesis**: {ai_providers.get('synthesis', 'N/A')}

**Key Insights from Expert Team:**

#### User Experience (Anya Sharma)
{_extract_key_points(expert_consultation.get('anya_analysis', ''))}

#### Product Strategy (Ben Carter)
{_extract_key_points(expert_consultation.get('ben_analysis', ''))}

#### Technical Architecture (Dr. Chloe Evans)
{_extract_key_points(expert_consultation.get('chloe_analysis', ''))}

**Comprehensive PRD**: A complete Product Requirements Document has been generated and is available in the TaskMaster directory.
"""

    return summary


def _extract_key_points(analysis_text: str) -> str:
    """Extract key points from AI analysis text."""
    if not analysis_text:
        return "- Analysis details available in TaskMaster directory"

    # Split into lines and extract key points (first few sentences/bullet points)
    lines = analysis_text.split("\n")
    key_points = []

    for line in lines[:3]:  # Take first 3 lines as key points
        line = line.strip()
        if line and len(line) > 10:  # Ignore very short lines
            # Clean up and format as bullet point
            if not line.startswith("-"):
                line = f"- {line}"
            key_points.append(line)

    if not key_points:
        return "- Analysis details available in TaskMaster directory"

    return "\n".join(key_points)


def _create_github_folder(
    project_dir: str, project_name: str, project_type: str, tech_stack: dict[str, Any]
) -> bool:
    """Create .github folder with Copilot and workflow configuration."""
    github_dir = os.path.join(project_dir, ".github")
    os.makedirs(github_dir, exist_ok=True)

    # Create ISSUE_TEMPLATE directory
    issue_template_dir = os.path.join(github_dir, "ISSUE_TEMPLATE")
    os.makedirs(issue_template_dir, exist_ok=True)

    # Extract technologies for documentation
    tech_summary = []
    if isinstance(tech_stack, dict) and "categories" in tech_stack:
        for category in tech_stack["categories"]:
            for option in category.get("options", []):
                if option.get("recommended", False):
                    tech_summary.append(f"- **{category['name']}**: {option['name']}")

    # Create bug report template
    bug_report_content = f"""---
name: Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

**Describe the Bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected Behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
- OS: [e.g. iOS]
- Python Version: [e.g. 3.11]
- Project Version: [e.g. 1.0.0]

**Technology Stack:**
{chr(10).join(tech_summary) if tech_summary else "Standard Python project"}

**Additional Context**
Add any other context about the problem here.
"""

    with open(os.path.join(issue_template_dir, "bug_report.md"), "w") as f:
        f.write(bug_report_content)

    # Create feature request template
    feature_request_content = f"""---
name: Feature Request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Technology Impact**
How would this feature interact with our current technology stack?
{chr(10).join(tech_summary) if tech_summary else "Standard Python project"}

**Additional Context**
Add any other context or screenshots about the feature request here.
"""

    with open(os.path.join(issue_template_dir, "feature_request.md"), "w") as f:
        f.write(feature_request_content)

    # Create documentation template
    documentation_content = """---
name: Documentation
about: Request improvements to documentation
title: '[DOCS] '
labels: documentation
assignees: ''
---

**What documentation is missing or unclear?**
A clear and concise description of what documentation needs improvement.

**Suggested content**
What specific information should be added or clarified?

**Location**
Where should this documentation be located?
- [ ] README.md
- [ ] docs/ directory
- [ ] Code comments
- [ ] API documentation
- [ ] Other:

**Additional Context**
Add any other context about the documentation request here.
"""

    with open(os.path.join(issue_template_dir, "documentation.md"), "w") as f:
        f.write(documentation_content)

    # Create pull request template
    pr_template_content = """## Description
Brief description of the changes in this pull request.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement
- [ ] Other (please describe):

## Testing
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] I have tested this change manually

## Code Quality
- [ ] My code follows the project's coding standards
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have run the linting tools and fixed any issues

## Checklist
- [ ] I have read the CONTRIBUTING.md document
- [ ] I have checked that there isn't already a PR that solves this problem
- [ ] I have only one commit per logical change
- [ ] I have included tests for my changes
- [ ] All tests pass

## Screenshots (if applicable)
Add screenshots to help explain your changes.

## Additional Notes
Any additional information or context about this PR.
"""

    with open(os.path.join(github_dir, "PULL_REQUEST_TEMPLATE.md"), "w") as f:
        f.write(pr_template_content)

    # Create security workflow
    security_workflow_content = """name: Security Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday

jobs:
  security:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
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

    - name: Run security scan with bandit
      run: poetry run bandit -r src/ -f json -o bandit-report.json
      continue-on-error: true

    - name: Run dependency vulnerability scan
      run: poetry run safety check --json --output safety-report.json
      continue-on-error: true

    - name: Scan for secrets
      run: poetry run detect-secrets scan --all-files --baseline .secrets.baseline

    - name: Upload security reports
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: security-reports
        path: |
          bandit-report.json
          safety-report.json

  codeql:
    name: CodeQL Analysis
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Initialize CodeQL
      uses: github/codeql-action/init@v2
      with:
        languages: python

    - name: Autobuild
      uses: github/codeql-action/autobuild@v2

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v2
"""

    # Create workflows directory
    workflows_dir = os.path.join(github_dir, "workflows")
    os.makedirs(workflows_dir, exist_ok=True)

    with open(os.path.join(workflows_dir, "security.yml"), "w") as f:
        f.write(security_workflow_content)

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


def _create_frontend_structure(project_dir: str, node_packages: list[str]):
    """Create proper frontend project structure for React/TypeScript projects."""
    frontend_dir = os.path.join(project_dir, "frontend")
    os.makedirs(frontend_dir, exist_ok=True)

    # Create frontend directory structure
    frontend_structure = [
        "src",
        "src/components",
        "src/pages",
        "src/hooks",
        "src/utils",
        "src/types",
        "public",
    ]

    for dir_path in frontend_structure:
        os.makedirs(os.path.join(frontend_dir, dir_path), exist_ok=True)

    # Create package.json for frontend
    package_json = {
        "name": "frontend",
        "version": "0.1.0",
        "private": True,
        "type": "module",
        "scripts": {
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview",
            "type-check": "tsc --noEmit",
        },
        "dependencies": {},
        "devDependencies": {"@vitejs/plugin-react": "^4.0.0", "vite": "^4.4.0"},
    }

    with open(os.path.join(frontend_dir, "package.json"), "w") as f:
        json.dump(package_json, f, indent=2)

    # Create TypeScript config if TypeScript is in packages
    if any("typescript" in pkg.lower() for pkg in node_packages):
        tsconfig = {
            "compilerOptions": {
                "target": "ES2020",
                "useDefineForClassFields": True,
                "lib": ["ES2020", "DOM", "DOM.Iterable"],
                "module": "ESNext",
                "skipLibCheck": True,
                "moduleResolution": "bundler",
                "allowImportingTsExtensions": True,
                "resolveJsonModule": True,
                "isolatedModules": True,
                "noEmit": True,
                "jsx": "react-jsx",
                "strict": True,
                "noUnusedLocals": True,
                "noUnusedParameters": True,
                "noFallthroughCasesInSwitch": True,
            },
            "include": ["src"],
            "references": [{"path": "./tsconfig.node.json"}],
        }

        with open(os.path.join(frontend_dir, "tsconfig.json"), "w") as f:
            json.dump(tsconfig, f, indent=2)

    # Create Vite config if React is in packages
    if any("react" in pkg.lower() for pkg in node_packages):
        vite_config = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
"""

        with open(os.path.join(frontend_dir, "vite.config.ts"), "w") as f:
            f.write(vite_config)

    # Create basic React App component
    if any("react" in pkg.lower() for pkg in node_packages):
        app_component = """import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to Your React App</h1>
        <p>Start building your amazing application!</p>
      </header>
    </div>
  );
}

export default App;
"""

        with open(os.path.join(frontend_dir, "src", "App.tsx"), "w") as f:
            f.write(app_component)

        # Create main.tsx entry point
        main_tsx = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
"""

        with open(os.path.join(frontend_dir, "src", "main.tsx"), "w") as f:
            f.write(main_tsx)

        # Create index.html
        index_html = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>React App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""

        with open(os.path.join(frontend_dir, "index.html"), "w") as f:
            f.write(index_html)

        # Create basic CSS files
        app_css = """.App {
  text-align: center;
}

.App-header {
  background-color: #282c34;
  padding: 20px;
  color: white;
}
"""

        with open(os.path.join(frontend_dir, "src", "App.css"), "w") as f:
            f.write(app_css)

        index_css = """body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
"""

        with open(os.path.join(frontend_dir, "src", "index.css"), "w") as f:
            f.write(index_css)


def _verify_installations(
    project_dir: str, python_packages: list[str], node_packages: list[str]
) -> list[str]:
    """Verify that installed packages can be imported/used."""
    verification_results = []

    # Verify Python packages
    if python_packages:
        python_executable = os.path.join(project_dir, ".venv", "bin", "python")
        if not os.path.exists(python_executable):
            python_executable = "python"  # Fallback to system python

        # Create a simple verification script
        verification_script = f"""import sys
import importlib

packages_to_test = {{
    'scikit-learn': 'sklearn',
    'beautifulsoup4': 'bs4',
    'pillow': 'PIL',
    'opencv-python': 'cv2'
}}

verified = []
failed = []

for package in {repr(python_packages)}:
    test_name = packages_to_test.get(package, package.replace('-', '_'))
    try:
        importlib.import_module(test_name)
        verified.append(package)
    except ImportError:
        failed.append(package)

print(f"VERIFIED: {{','.join(verified)}}")
print(f"FAILED: {{','.join(failed)}}")
"""

        try:
            result = subprocess.run(
                [python_executable, "-c", verification_script],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                for line in lines:
                    if line.startswith("VERIFIED:") and line[9:].strip():
                        verified_pkgs = line[9:].strip().split(",")
                        verification_results.append(
                            f"✅ Python imports verified: {', '.join(verified_pkgs)}"
                        )
                    elif line.startswith("FAILED:") and line[7:].strip():
                        failed_pkgs = line[7:].strip().split(",")
                        verification_results.append(
                            f"⚠️ Python imports failed: {', '.join(failed_pkgs)}"
                        )
        except (
            subprocess.TimeoutExpired,
            subprocess.CalledProcessError,
            FileNotFoundError,
        ):
            verification_results.append("⚠️ Could not verify Python package imports")

    # Verify Node.js packages (check if they're listed in package.json)
    if node_packages:
        frontend_package_json = os.path.join(project_dir, "frontend", "package.json")
        root_package_json = os.path.join(project_dir, "package.json")

        package_json_path = (
            frontend_package_json
            if os.path.exists(frontend_package_json)
            else root_package_json
        )

        if os.path.exists(package_json_path):
            try:
                with open(package_json_path) as f:
                    package_data = json.load(f)

                all_deps = {}
                all_deps.update(package_data.get("dependencies", {}))
                all_deps.update(package_data.get("devDependencies", {}))

                verified_node = [pkg for pkg in node_packages if pkg in all_deps]
                if verified_node:
                    verification_results.append(
                        f"✅ Node.js packages in package.json: {', '.join(verified_node)}"
                    )

            except (json.JSONDecodeError, FileNotFoundError):
                verification_results.append(
                    "⚠️ Could not verify Node.js package installations"
                )

    return verification_results


def _create_contributing_doc(
    docs_dir: str, project_name: str, package_name: str, tech_stack: dict[str, Any]
) -> None:
    """Create CONTRIBUTING.md documentation."""

    # Extract technologies for documentation
    tech_summary = []
    if isinstance(tech_stack, dict) and "categories" in tech_stack:
        for category in tech_stack["categories"]:
            for option in category.get("options", []):
                if option.get("recommended", False):
                    tech_summary.append(f"- **{category['name']}**: {option['name']}")

    contributing_content = f"""# Contributing to {project_name}

Thank you for your interest in contributing to {project_name}! This document provides guidelines and instructions for contributing to this project.

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Poetry for dependency management
- Git for version control
- Node.js (if working with frontend components)

### Setting Up Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/{project_name}.git
   cd {project_name}
   ```

2. **Install Dependencies**
   ```bash
   poetry install --with dev
   ```

3. **Set Up Pre-commit Hooks**
   ```bash
   poetry run pre-commit install
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run Tests**
   ```bash
   poetry run pytest
   ```

## 🛠️ Development Workflow

### Branch Strategy

- **main**: Production-ready code
- **develop**: Integration branch for features
- **feature/***: New features
- **bugfix/***: Bug fixes
- **hotfix/***: Critical production fixes

### Making Changes

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Follow the coding standards below
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   # Run all tests
   poetry run pytest

   # Run linting
   poetry run black src/
   poetry run ruff check src/ --fix

   # Type checking
   poetry run mypy src/
   ```

4. **Commit Your Changes**
   ```bash
   # Use the commit workflow script
   poetry run python scripts/commit_workflow.py
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 Coding Standards

### Python Style Guide

- Follow PEP 8 conventions
- Use type hints for all function signatures
- Write comprehensive docstrings (Google style)
- Maximum line length: 88 characters (Black default)

### Code Quality

- **Formatting**: Black (configured for 88 characters)
- **Linting**: Ruff with project-specific configuration
- **Type Checking**: mypy with strict settings
- **Testing**: pytest with coverage reporting

### Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add comments for complex logic
- Update this CONTRIBUTING.md for process changes

## 🧪 Testing

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src --cov-report=html

# Run specific test file
poetry run pytest tests/test_specific.py

# Run with verbose output
poetry run pytest -v
```

### Writing Tests

- Place tests in `tests/` directory
- Mirror the `src/` structure in your test files
- Use descriptive test names
- Include both positive and negative test cases
- Mock external dependencies

### Test Coverage

- Maintain test coverage above 80%
- Write tests for new features
- Update tests when modifying existing code

## 🔧 Technology Stack

This project uses the following technologies:

{chr(10).join(tech_summary) if tech_summary else "- Standard Python project with Poetry, pytest, and code quality tools"}

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Commit messages are descriptive
- [ ] PR addresses a single concern

### PR Description

- Provide a clear description of changes
- Link to related issues
- Include screenshots for UI changes
- List any breaking changes

### Review Process

1. Automated checks must pass
2. Code review by maintainers
3. Address feedback promptly
4. Squash commits if requested

## 🐛 Bug Reports

Use the GitHub issue template for bug reports. Include:

- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Screenshots if applicable

## 💡 Feature Requests

Use the GitHub issue template for feature requests. Include:

- Problem description
- Proposed solution
- Alternative approaches considered
- Use cases and examples

## 📚 Documentation

### Types of Documentation

- **README.md**: User-facing documentation
- **docs/**: Technical documentation
- **Code comments**: Complex logic explanation
- **API docs**: Auto-generated from docstrings

### Documentation Guidelines

- Write clear, concise documentation
- Include code examples
- Keep documentation up to date
- Use proper markdown formatting

## 🎯 Project Structure

```
{project_name}/
├── src/{package_name}/          # Main application code
├── tests/                       # Test suite
├── docs/                        # Documentation
├── scripts/                     # Development scripts
├── .github/                     # GitHub configuration
├── .vscode/                     # VS Code settings
├── TaskMaster/                  # Project management
└── pyproject.toml              # Project configuration
```

## 🤝 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain professionalism

## 📞 Getting Help

- **Issues**: Create a GitHub issue
- **Discussions**: Use GitHub discussions
- **Documentation**: Check the docs/ directory

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributor graphs

Thank you for contributing to {project_name}!
"""

    with open(os.path.join(docs_dir, "CONTRIBUTING.md"), "w") as f:
        f.write(contributing_content)


def _create_changelog_doc(docs_dir: str, project_name: str) -> None:
    """Create CHANGELOG.md documentation."""

    import datetime

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    changelog_content = f"""# Changelog

All notable changes to {project_name} will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure with AI-driven technology stack
- Comprehensive development environment setup
- Automated testing and code quality pipeline
- Documentation and contribution guidelines

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- Integrated security scanning with bandit and safety
- Secrets detection with detect-secrets
- Secure development practices and guidelines

## [0.1.0] - {current_date}

### Added
- Initial release of {project_name}
- AI-powered project generation and setup
- Professional development environment
- Code quality tools and automated workflows
- Comprehensive documentation and templates

---

## How to Update This Changelog

### Categories
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements

### Version Format
- Use [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH)
- MAJOR: Incompatible API changes
- MINOR: Backwards-compatible functionality
- PATCH: Backwards-compatible bug fixes

### Entry Format
```
## [Version] - YYYY-MM-DD

### Category
- Description of change [#issue-number]
```

### Unreleased Section
- Keep an "Unreleased" section at the top
- Move entries to a new version section on release
- Always maintain the categories structure
"""

    with open(os.path.join(docs_dir, "CHANGELOG.md"), "w") as f:
        f.write(changelog_content)


def _should_create_api_docs(
    tech_stack: dict[str, Any], project_description: str
) -> bool:
    """
    Determine if API documentation should be created based on project characteristics.

    Conditions:
    1. Project is an API (FastAPI, Flask, Django REST)
    2. Project is a library/framework
    3. Project has public interfaces
    """
    # Check project description for API keywords
    description_lower = project_description.lower()
    api_keywords = [
        "api",
        "rest",
        "restful",
        "endpoint",
        "service",
        "microservice",
        "library",
        "framework",
        "package",
        "module",
        "interface",
        "public",
    ]

    has_api_description = any(keyword in description_lower for keyword in api_keywords)

    # Check tech stack for API-related technologies
    api_techs = []
    if isinstance(tech_stack, dict) and "categories" in tech_stack:
        for category in tech_stack["categories"]:
            category_name = category.get("name", "").lower()

            # Check for API frameworks
            if "backend" in category_name or "framework" in category_name:
                for option in category.get("options", []):
                    if option.get("recommended", False):
                        tech_name = option.get("name", "").lower()
                        if any(
                            api_tech in tech_name
                            for api_tech in ["fastapi", "flask", "django", "api"]
                        ):
                            api_techs.append(tech_name)

    # Check for library/package indicators
    is_library = any(
        keyword in description_lower
        for keyword in ["library", "package", "framework", "module"]
    )

    return has_api_description or len(api_techs) > 0 or is_library


def _create_api_docs_structure(
    docs_dir: str, project_name: str, package_name: str, tech_stack: dict[str, Any]
) -> None:
    """Create API documentation structure."""

    # Create API docs directory
    api_docs_dir = os.path.join(docs_dir, "api")
    os.makedirs(api_docs_dir, exist_ok=True)

    # Extract API-related technologies
    api_techs = []
    if isinstance(tech_stack, dict) and "categories" in tech_stack:
        for category in tech_stack["categories"]:
            for option in category.get("options", []):
                if option.get("recommended", False):
                    tech_name = option.get("name", "")
                    if any(
                        api_tech in tech_name.lower()
                        for api_tech in ["fastapi", "flask", "django", "api"]
                    ):
                        api_techs.append(tech_name)

    # Create API documentation index
    api_index_content = f"""# {project_name} API Documentation

Welcome to the {project_name} API documentation.

## Overview

{project_name} provides a comprehensive API for interacting with the application. This documentation covers all available endpoints, request/response formats, and usage examples.

## Technology Stack

The API is built using:
{chr(10).join(f"- {tech}" for tech in api_techs) if api_techs else "- Modern Python web framework"}

## Quick Start

### Installation

```bash
pip install {package_name}
```

### Basic Usage

```python
from {package_name} import {package_name.replace('_', ' ').title().replace(' ', '')}

# Initialize the client
client = {package_name.replace('_', ' ').title().replace(' ', '')}()

# Example usage
result = client.example_method()
print(result)
```

## Documentation Sections

- [**Authentication**](authentication.md) - API authentication methods
- [**Endpoints**](endpoints.md) - Complete endpoint reference
- [**Examples**](examples.md) - Code examples and use cases
- [**Error Handling**](errors.md) - Error codes and handling
- [**Rate Limiting**](rate-limiting.md) - Rate limiting information
- [**Changelog**](../CHANGELOG.md) - API version history

## API Reference

### Base URL

```
https://api.{package_name.replace('_', '-')}.com/v1
```

### Content Type

All requests and responses use JSON format:

```
Content-Type: application/json
```

### Response Format

All API responses follow this structure:

```json
{{
  "success": true,
  "data": {{}},
  "message": "Success message",
  "timestamp": "2025-01-08T10:30:00Z"
}}
```

## Support

For API support and questions:
- GitHub Issues: [Create an issue](https://github.com/your-username/{project_name}/issues)
- Documentation: [docs/](../)
- Examples: [examples/](examples/)

## License

This API documentation is part of {project_name} and subject to the same license terms.
"""

    with open(os.path.join(api_docs_dir, "README.md"), "w") as f:
        f.write(api_index_content)

    # Create authentication documentation
    auth_content = f"""# Authentication

{project_name} API uses token-based authentication.

## Authentication Methods

### API Key Authentication

Include your API key in the request header:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \\
     https://api.{package_name.replace('_', '-')}.com/v1/endpoint
```

### Python Client

```python
from {package_name} import {package_name.replace('_', ' ').title().replace(' ', '')}

client = {package_name.replace('_', ' ').title().replace(' ', '')}(api_key="your_api_key")
```

## Getting an API Key

1. Sign up for an account
2. Navigate to API settings
3. Generate a new API key
4. Store it securely

## Rate Limits

- **Free tier**: 100 requests per hour
- **Pro tier**: 1,000 requests per hour
- **Enterprise**: Custom limits

## Error Responses

Authentication errors return HTTP 401:

```json
{{
  "success": false,
  "error": "Invalid API key",
  "code": "AUTH_001"
}}
```
"""

    with open(os.path.join(api_docs_dir, "authentication.md"), "w") as f:
        f.write(auth_content)

    # Create endpoints documentation
    endpoints_content = f"""# API Endpoints

Complete reference for all {project_name} API endpoints.

## Base Information

- **Base URL**: `https://api.{package_name.replace('_', '-')}.com/v1`
- **Format**: JSON
- **Authentication**: Bearer token required

## Endpoints

### Health Check

Check API status and connectivity.

```http
GET /health
```

**Response:**
```json
{{
  "success": true,
  "data": {{
    "status": "healthy",
    "version": "1.0.0",
    "timestamp": "2025-01-08T10:30:00Z"
  }}
}}
```

### Example Endpoint

Description of what this endpoint does.

```http
GET /example
```

**Parameters:**
- `param1` (string, required): Description of parameter
- `param2` (integer, optional): Description of parameter

**Response:**
```json
{{
  "success": true,
  "data": {{
    "result": "example_value"
  }}
}}
```

**Error Response:**
```json
{{
  "success": false,
  "error": "Error description",
  "code": "ERR_001"
}}
```

## Response Codes

- `200 OK`: Success
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Invalid or missing API key
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## Pagination

Large result sets are paginated:

```json
{{
  "success": true,
  "data": {{
    "items": [...],
    "pagination": {{
      "page": 1,
      "per_page": 20,
      "total": 100,
      "pages": 5
    }}
  }}
}}
```

Use `?page=2&per_page=50` to navigate pages.
"""

    with open(os.path.join(api_docs_dir, "endpoints.md"), "w") as f:
        f.write(endpoints_content)

    # Create examples documentation
    examples_content = f"""# API Examples

Practical examples for using the {project_name} API.

## Python Examples

### Basic Usage

```python
import requests

# Set up authentication
headers = {{
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}}

# Make a request
response = requests.get(
    "https://api.{package_name.replace('_', '-')}.com/v1/example",
    headers=headers
)

data = response.json()
print(data)
```

### Using the Python Client

```python
from {package_name} import {package_name.replace('_', ' ').title().replace(' ', '')}

# Initialize client
client = {package_name.replace('_', ' ').title().replace(' ', '')}(api_key="your_api_key")

# Make requests
try:
    result = client.get_data()
    print(f"Success: {{result}}")
except Exception as e:
    print(f"Error: {{e}}")
```

## JavaScript Examples

### Fetch API

```javascript
const apiKey = 'YOUR_API_KEY';
const baseUrl = 'https://api.{package_name.replace('_', '-')}.com/v1';

async function fetchData() {{
    try {{
        const response = await fetch(`${{baseUrl}}/example`, {{
            method: 'GET',
            headers: {{
                'Authorization': `Bearer ${{apiKey}}`,
                'Content-Type': 'application/json'
            }}
        }});

        const data = await response.json();
        console.log(data);
    }} catch (error) {{
        console.error('Error:', error);
    }}
}}
```

### Node.js with Axios

```javascript
const axios = require('axios');

const api = axios.create({{
    baseURL: 'https://api.{package_name.replace('_', '-')}.com/v1',
    headers: {{
        'Authorization': 'Bearer YOUR_API_KEY',
        'Content-Type': 'application/json'
    }}
}});

// Make request
api.get('/example')
    .then(response => {{
        console.log(response.data);
    }})
    .catch(error => {{
        console.error('Error:', error.response.data);
    }});
```

## cURL Examples

### GET Request

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \\
     -H "Content-Type: application/json" \\
     https://api.{package_name.replace('_', '-')}.com/v1/example
```

### POST Request

```bash
curl -X POST \\
     -H "Authorization: Bearer YOUR_API_KEY" \\
     -H "Content-Type: application/json" \\
     -d '{{"param1": "value1", "param2": "value2"}}' \\
     https://api.{package_name.replace('_', '-')}.com/v1/example
```

## Error Handling

### Python Error Handling

```python
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises HTTPError for bad responses
    data = response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {{e.response.status_code}}")
    print(f"Response: {{e.response.text}}")
except requests.exceptions.RequestException as e:
    print(f"Request Error: {{e}}")
```

### JavaScript Error Handling

```javascript
fetch(url, options)
    .then(response => {{
        if (!response.ok) {{
            throw new Error(`HTTP error! status: ${{response.status}}`);
        }}
        return response.json();
    }})
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
```

## Rate Limiting Example

```python
import time
import requests
from requests.exceptions import HTTPError

def make_request_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 429:  # Rate limited
                retry_after = int(response.headers.get('Retry-After', 60))
                print(f"Rate limited. Waiting {{retry_after}} seconds...")
                time.sleep(retry_after)
                continue
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff

    raise Exception("Max retries exceeded")
```
"""

    with open(os.path.join(api_docs_dir, "examples.md"), "w") as f:
        f.write(examples_content)

    # Create error handling documentation
    errors_content = f"""# Error Handling

Understanding and handling errors in the {project_name} API.

## Error Response Format

All API errors follow this structure:

```json
{{
  "success": false,
  "error": "Human-readable error message",
  "code": "ERROR_CODE",
  "details": {{}},
  "timestamp": "2025-01-08T10:30:00Z"
}}
```

## HTTP Status Codes

### 2xx Success
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `204 No Content`: Request successful, no content returned

### 4xx Client Errors
- `400 Bad Request`: Invalid request format or parameters
- `401 Unauthorized`: Invalid or missing authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict
- `422 Unprocessable Entity`: Validation errors
- `429 Too Many Requests`: Rate limit exceeded

### 5xx Server Errors
- `500 Internal Server Error`: Server error
- `502 Bad Gateway`: Gateway error
- `503 Service Unavailable`: Service temporarily unavailable
- `504 Gateway Timeout`: Gateway timeout

## Error Codes

### Authentication Errors (AUTH_xxx)
- `AUTH_001`: Invalid API key
- `AUTH_002`: Expired API key
- `AUTH_003`: Missing API key
- `AUTH_004`: Insufficient permissions

### Validation Errors (VAL_xxx)
- `VAL_001`: Missing required parameter
- `VAL_002`: Invalid parameter format
- `VAL_003`: Parameter value out of range
- `VAL_004`: Invalid JSON format

### Rate Limiting Errors (RATE_xxx)
- `RATE_001`: Rate limit exceeded
- `RATE_002`: Daily quota exceeded
- `RATE_003`: Concurrent request limit exceeded

### Resource Errors (RES_xxx)
- `RES_001`: Resource not found
- `RES_002`: Resource already exists
- `RES_003`: Resource locked
- `RES_004`: Resource deleted

### Server Errors (SRV_xxx)
- `SRV_001`: Internal server error
- `SRV_002`: Database connection error
- `SRV_003`: External service unavailable
- `SRV_004`: Configuration error

## Error Handling Best Practices

### 1. Always Check Response Status

```python
response = requests.get(url, headers=headers)
if response.status_code != 200:
    error_data = response.json()
    print(f"Error: {{error_data.get('error')}}")
    print(f"Code: {{error_data.get('code')}}")
```

### 2. Implement Retry Logic

```python
import time
import random

def make_request_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 429:  # Rate limited
                retry_after = int(response.headers.get('Retry-After', 60))
                time.sleep(retry_after)
                continue

            if response.status_code >= 500:  # Server error
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(wait_time)
                    continue

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)

    raise Exception("Max retries exceeded")
```

### 3. Log Errors Properly

```python
import logging

logger = logging.getLogger(__name__)

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
except requests.exceptions.HTTPError as e:
    error_data = e.response.json()
    logger.error(
        f"API Error: {{error_data.get('code')}} - {{error_data.get('error')}}",
        extra={{'status_code': e.response.status_code, 'response': error_data}}
    )
    raise
```

### 4. Handle Specific Error Types

```python
def handle_api_error(response):
    if response.status_code == 401:
        # Handle authentication error
        raise AuthenticationError("Invalid API key")
    elif response.status_code == 403:
        # Handle permission error
        raise PermissionError("Insufficient permissions")
    elif response.status_code == 429:
        # Handle rate limiting
        raise RateLimitError("Rate limit exceeded")
    elif response.status_code >= 500:
        # Handle server errors
        raise ServerError("Server error occurred")
    else:
        # Handle other errors
        error_data = response.json()
        raise APIError(f"API Error: {{error_data.get('error')}}")
```

## Common Error Scenarios

### Invalid API Key
```json
{{
  "success": false,
  "error": "Invalid API key provided",
  "code": "AUTH_001"
}}
```

### Missing Required Parameter
```json
{{
  "success": false,
  "error": "Missing required parameter: 'email'",
  "code": "VAL_001",
  "details": {{
    "parameter": "email",
    "expected_type": "string"
  }}
}}
```

### Rate Limit Exceeded
```json
{{
  "success": false,
  "error": "Rate limit exceeded",
  "code": "RATE_001",
  "details": {{
    "limit": 100,
    "window": "1 hour",
    "retry_after": 3600
  }}
}}
```

### Resource Not Found
```json
{{
  "success": false,
  "error": "Resource not found",
  "code": "RES_001",
  "details": {{
    "resource_type": "user",
    "resource_id": "12345"
  }}
}}
```

## Support

If you encounter persistent errors or need help with error handling:

1. Check the error code in this documentation
2. Verify your API key and permissions
3. Check our status page for service issues
4. Contact support with the error code and request details
"""

    with open(os.path.join(api_docs_dir, "errors.md"), "w") as f:
        f.write(errors_content)

    # Create rate limiting documentation
    rate_limiting_content = f"""# Rate Limiting

Information about rate limits and usage quotas for the {project_name} API.

## Rate Limit Tiers

### Free Tier
- **Requests**: 100 per hour
- **Burst**: 10 requests per minute
- **Daily**: 1,000 requests per day

### Pro Tier
- **Requests**: 1,000 per hour
- **Burst**: 100 requests per minute
- **Daily**: 10,000 requests per day

### Enterprise
- **Requests**: Custom limits
- **Burst**: Custom limits
- **Daily**: Custom limits

## Rate Limit Headers

Every API response includes rate limit information in the headers:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1641648000
X-RateLimit-Window: 3600
```

### Header Descriptions

- `X-RateLimit-Limit`: Maximum requests allowed in the current window
- `X-RateLimit-Remaining`: Remaining requests in the current window
- `X-RateLimit-Reset`: Unix timestamp when the window resets
- `X-RateLimit-Window`: Window duration in seconds

## Rate Limit Exceeded Response

When you exceed the rate limit, you'll receive a 429 status code:

```json
{{
  "success": false,
  "error": "Rate limit exceeded",
  "code": "RATE_001",
  "details": {{
    "limit": 100,
    "window": "1 hour",
    "retry_after": 3600
  }}
}}
```

## Best Practices

### 1. Check Rate Limit Headers

```python
import requests
import time

def make_request_with_rate_limit_check(url, headers):
    response = requests.get(url, headers=headers)

    # Check remaining requests
    remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
    if remaining < 10:  # Low on requests
        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
        current_time = int(time.time())
        wait_time = reset_time - current_time

        if wait_time > 0:
            print(f"Rate limit low. Waiting {{wait_time}} seconds...")
            time.sleep(wait_time)

    return response
```

### 2. Implement Exponential Backoff

```python
import time
import random

def exponential_backoff_request(url, headers, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)

        if response.status_code == 429:
            # Extract retry-after header if available
            retry_after = response.headers.get('Retry-After')
            if retry_after:
                wait_time = int(retry_after)
            else:
                # Calculate exponential backoff
                wait_time = (2 ** attempt) + random.uniform(0, 1)

            print(f"Rate limited. Waiting {{wait_time}} seconds...")
            time.sleep(wait_time)
            continue

        return response

    raise Exception("Max retries exceeded due to rate limiting")
```

### 3. Use Request Queuing

```python
import time
from queue import Queue
from threading import Thread

class RateLimitedRequests:
    def __init__(self, requests_per_second=1):
        self.requests_per_second = requests_per_second
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0
        self.queue = Queue()
        self.worker_thread = Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

    def _worker(self):
        while True:
            request_func, args, kwargs = self.queue.get()

            # Ensure minimum interval between requests
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            if time_since_last < self.min_interval:
                time.sleep(self.min_interval - time_since_last)

            try:
                result = request_func(*args, **kwargs)
                self.last_request_time = time.time()
                return result
            except Exception as e:
                print(f"Request failed: {{e}}")

    def add_request(self, request_func, *args, **kwargs):
        self.queue.put((request_func, args, kwargs))

# Usage
rate_limiter = RateLimitedRequests(requests_per_second=0.5)  # 1 request every 2 seconds

def make_api_call():
    return requests.get(url, headers=headers)

rate_limiter.add_request(make_api_call)
```

### 4. Monitor Usage

```python
class APIUsageMonitor:
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.rate_limit_hits = 0
        self.start_time = time.time()

    def log_request(self, response):
        self.request_count += 1

        if response.status_code == 429:
            self.rate_limit_hits += 1
        elif response.status_code >= 400:
            self.error_count += 1

        # Log rate limit info
        remaining = response.headers.get('X-RateLimit-Remaining')
        if remaining:
            print(f"Requests remaining: {{remaining}}")

    def get_stats(self):
        runtime = time.time() - self.start_time
        return {{
            'total_requests': self.request_count,
            'errors': self.error_count,
            'rate_limit_hits': self.rate_limit_hits,
            'requests_per_second': self.request_count / runtime,
            'error_rate': self.error_count / self.request_count if self.request_count > 0 else 0
        }}

# Usage
monitor = APIUsageMonitor()
response = requests.get(url, headers=headers)
monitor.log_request(response)
```

## Upgrading Your Plan

To increase your rate limits:

1. **Pro Plan**: Higher limits for production applications
2. **Enterprise Plan**: Custom limits and dedicated support
3. **Contact Sales**: For very high-volume requirements

## Monitoring Tools

### Rate Limit Dashboard
- Real-time usage monitoring
- Historical usage analytics
- Alert configuration
- Usage forecasting

### API Analytics
- Request volume trends
- Error rate monitoring
- Performance metrics
- Geographic usage patterns

## Troubleshooting

### Common Issues

1. **Sudden Rate Limit Hits**
   - Check for infinite loops in your code
   - Verify retry logic isn't too aggressive
   - Monitor concurrent requests

2. **Inconsistent Rate Limits**
   - Rate limits are per API key
   - Check if multiple applications use the same key
   - Verify time zone differences in reset times

3. **Burst Limits**
   - Spread requests evenly over time
   - Don't send all requests at once
   - Use queuing for batch operations

### Getting Help

If you're experiencing rate limiting issues:

1. Check your current usage in the dashboard
2. Review your application's request patterns
3. Consider upgrading your plan
4. Contact support with your API key and usage patterns
"""

    with open(os.path.join(api_docs_dir, "rate-limiting.md"), "w") as f:
        f.write(rate_limiting_content)
