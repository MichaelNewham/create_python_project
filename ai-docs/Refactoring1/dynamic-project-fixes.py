# Enhanced core_project_builder.py - Complete implementation

def create_project_structure(
    project_name: str,
    project_dir: str,
    project_type: str,
    with_ai: bool = True,
    tech_stack: dict[Any, Any] | None = None,
    **kwargs: Any,
) -> tuple[bool, str]:
    """Create the complete project structure with ALL development tools."""
    try:
        tech_stack = tech_stack or {}
        package_name = project_name.replace("-", "_").replace(" ", "_").lower()

        # ... existing directory creation ...

        # NEW: Create complete development environment
        _create_workspace_file(project_dir, project_name, project_type, tech_stack)
        _create_scripts_directory(project_dir, package_name)
        _create_config_directory(project_dir)
        _create_package_json(project_dir, tech_stack)

        # Enhanced Poetry configuration with ALL dev tools
        _create_enhanced_pyproject_toml(project_dir, project_name, project_type, tech_stack)

        # ... rest of existing code ...
        return True, f"Project {project_name} created successfully"
    except Exception as e:
        return False, f"Error creating project: {str(e)}"


def _create_enhanced_pyproject_toml(
    project_dir: str, project_name: str, project_type: str, tech_stack: dict[Any, Any]
):
    """Create Poetry configuration with AI-recommended AND dev dependencies."""
    package_name = project_name.replace("-", "_").replace(" ", "_").lower()

    # Get AI-recommended dependencies
    project_deps = _get_dynamic_project_dependencies(tech_stack)

    content = f"""[tool.poetry]
name = "{project_name}"
version = "0.1.0"
description = ""
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"
packages = [{{include = "{package_name}", from = "src"}}]

[tool.poetry.dependencies]
python = "^3.11"
{project_deps}

[tool.poetry.group.dev.dependencies]
# Essential development tools - ALWAYS included
pytest = "^8.0.0"
black = "^24.0.0"
ruff = "^0.5.0"
mypy = "^1.10.0"
pre-commit = "^4.2.0"
detect-secrets = "^1.5.0"
pytest-cov = "^6.1.1"
python-dotenv = "^1.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 88

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
"""

    with open(os.path.join(project_dir, "pyproject.toml"), "w", encoding="utf-8") as f:
        f.write(content)


def _get_dynamic_project_dependencies(tech_stack: dict[Any, Any]) -> str:
    """Extract dependencies from AI-recommended tech stack."""
    deps = []

    # Map of technology names to Poetry dependencies
    tech_to_deps = {
        # Backend Frameworks
        "Flask": ['flask = "^3.0.0"', 'python-dotenv = "^1.0.0"'],
        "Django": ['django = "^5.0.0"', 'djangorestframework = "^3.15.0"'],
        "FastAPI": ['fastapi = "^0.110.0"', 'uvicorn = "^0.29.0"'],

        # Authentication
        "Flask-Login": ['flask-login = "^0.6.0"'],
        "PyJWT": ['pyjwt = "^2.8.0"'],
        "Authlib": ['authlib = "^1.3.0"'],

        # Databases
        "PostgreSQL": ['psycopg2-binary = "^2.9.0"', 'sqlalchemy = "^2.0.0"'],
        "MongoDB": ['pymongo = "^4.0.0"', 'mongoengine = "^0.28.0"'],

        # Real-time Communication
        "WebSockets": ['websockets = "^12.0"'],
        "Flask-SocketIO": ['flask-socketio = "^5.3.0"', 'python-socketio = "^5.11.0"'],

        # Data Processing
        "Pandas": ['pandas = "^2.2.0"', 'numpy = "^1.26.0"'],
        "Matplotlib": ['matplotlib = "^3.8.0"', 'seaborn = "^0.13.0"'],

        # IoT/Hardware
        "MJPG-Streamer": ['opencv-python = "^4.9.0"', 'pillow = "^10.2.0"'],
        "Kivy": ['kivy = "^2.3.0"'],

        # Testing (additional)
        "Pytest": ['pytest-asyncio = "^0.23.0"', 'pytest-mock = "^3.12.0"'],
    }

    # Extract technologies from AI recommendations
    if isinstance(tech_stack, dict) and "categories" in tech_stack:
        for category in tech_stack["categories"]:
            for option in category.get("options", []):
                if option.get("recommended", False):
                    tech_name = option["name"]
                    if tech_name in tech_to_deps:
                        deps.extend(tech_to_deps[tech_name])

    # Remove duplicates while preserving order
    seen = set()
    unique_deps = []
    for dep in deps:
        if dep not in seen:
            seen.add(dep)
            unique_deps.append(dep)

    return "\n".join(unique_deps)


def _create_workspace_file(
    project_dir: str, project_name: str, project_type: str, tech_stack: dict[Any, Any]
):
    """Create VS Code workspace file for easy project opening."""
    workspace_config = {
        "folders": [
            {"name": project_name.replace("_", " ").title(), "path": "."}
        ],
        "settings": {
            "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
            "python.terminal.activateEnvironment": True,
            "python.testing.pytestEnabled": True,
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.organizeImports": "explicit",
                "source.fixAll.ruff": "explicit"
            },
            "[python]": {
                "editor.defaultFormatter": "ms-python.black-formatter"
            },
            "files.exclude": {
                "**/__pycache__": True,
                "**/*.pyc": True,
                ".mypy_cache": True,
                ".pytest_cache": True,
                ".ruff_cache": True,
                "htmlcov": True,
                ".coverage": True
            }
        },
        "extensions": {
            "recommendations": [
                "ms-python.python",
                "ms-python.vscode-pylance",
                "ms-python.black-formatter",
                "charliermarsh.ruff",
                "njpwerner.autodocstring",
                "GitHub.copilot",
                "GitHub.copilot-chat",
                "eamodio.gitlens",
                "streetsidesoftware.code-spell-checker"
            ]
        }
    }

    # Add project-specific folders
    if project_type == "web" or "flask" in str(tech_stack).lower():
        workspace_config["folders"].extend([
            {"name": "Backend", "path": "./backend"},
            {"name": "Frontend", "path": "./frontend"}
        ])

    # IoT-specific configuration
    if any(keyword in project_name.lower() for keyword in ["esp32", "iot", "arduino", "sensor"]):
        workspace_config["folders"].append(
            {"name": "Firmware", "path": "./firmware"}
        )
        workspace_config["extensions"]["recommendations"].extend([
            "platformio.platformio-ide",
            "ms-vscode.cpptools"
        ])

    workspace_file = os.path.join(project_dir, f"{project_name}.code-workspace")
    with open(workspace_file, "w", encoding="utf-8") as f:
        import json
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
        return False
    print("✅ All checks passed!")
    return True

def generate_commit_message():
    \"\"\"Generate AI-powered commit message based on changes.\"\"\"
    # Simplified version - in real implementation, use AI
    changes = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True, text=True
    ).stdout.strip()

    if not changes:
        return "chore: update project files"

    files = changes.split("\\n")
    if len(files) == 1:
        return f"feat: update {{files[0]}}"
    else:
        return f"feat: update {{len(files)}} files"

def main():
    \"\"\"Main commit workflow.\"\"\"
    # Stage all changes
    subprocess.run(["git", "add", "."])

    # Run checks
    if not run_pre_commit_checks():
        sys.exit(1)

    # Generate commit message
    message = generate_commit_message()
    print(f"📝 Commit message: {{message}}")

    # Commit
    subprocess.run(["git", "commit", "-m", message])
    print("✅ Changes committed successfully!")

if __name__ == "__main__":
    main()
"""

    with open(os.path.join(scripts_dir, "commit_workflow.py"), "w") as f:
        f.write(commit_workflow)
    os.chmod(os.path.join(scripts_dir, "commit_workflow.py"), 0o755)


def _create_config_directory(project_dir: str):
    """Create .config directory with linting and type checking configs."""
    config_dir = os.path.join(project_dir, ".config")
    os.makedirs(config_dir, exist_ok=True)

    # mypy.ini
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

[[mypy.overrides]]
module = "flask.*"
ignore_missing_imports = true

[[mypy.overrides]]
module = "cv2.*"
ignore_missing_imports = true
"""
    with open(os.path.join(config_dir, "mypy.ini"), "w") as f:
        f.write(mypy_content)

    # ruff.toml
    ruff_content = """target-version = "py311"
line-length = 88

[lint]
select = ["E", "F", "I", "N", "W", "B", "C4", "SIM", "UP"]
ignore = ["E501", "B008"]

[lint.per-file-ignores]
"tests/*" = ["E501"]
"""
    with open(os.path.join(config_dir, "ruff.toml"), "w") as f:
        f.write(ruff_content)

    # .pre-commit-config.yaml (in project root)
    precommit_content = """default_stages: [pre-commit]
repos:
  - repo: https://github.com/psf/black
    rev: 24.0.0
    hooks:
      - id: black
        stages: [pre-commit]

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix, --config=.config/ruff.toml]
        stages: [pre-commit]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        args: [--ignore-missing-imports, --config-file=.config/mypy.ini]
        stages: [pre-commit]
"""
    with open(os.path.join(project_dir, ".pre-commit-config.yaml"), "w") as f:
        f.write(precommit_content)


def _create_package_json(project_dir: str, tech_stack: dict[Any, Any]):
    """Create package.json for MCP server management."""
    package_json = {
        "name": os.path.basename(project_dir),
        "version": "1.0.0",
        "description": "MCP servers for enhanced development",
        "dependencies": {
            "@upstash/context7-mcp": "latest",
            "server-perplexity-ask": "latest"
        }
    }

    # Add project-specific MCP servers based on tech stack
    if "github" in str(tech_stack).lower() or True:  # Always useful
        package_json["dependencies"]["@github/github-mcp-server"] = "latest"

    with open(os.path.join(project_dir, "package.json"), "w") as f:
        import json
        json.dump(package_json, f, indent=2)


# Enhanced task_config.py additions

def generate_tasks_json(project_type: str, tech_stack: dict[str, str]) -> dict[str, Any]:
    """Create complete tasks.json with all development workflows."""

    # Essential base tasks for ALL projects
    base_tasks = [
        # ... existing tasks ...

        # NEW: Essential workflow tasks
        {
            "label": "Commit Workflow",
            "type": "shell",
            "command": "poetry run python ${workspaceFolder}/scripts/commit_workflow.py",
            "problemMatcher": [],
            "group": {
                "kind": "build",
                "isDefault": True
            }
        },
        {
            "label": "Run Main App",
            "type": "shell",
            "command": "poetry run python -m ${workspaceFolderBasename}",
            "problemMatcher": [],
            "group": "build",
            "presentation": {
                "reveal": "always",
                "panel": "new",
                "clear": True
            }
        },
        {
            "label": "Lint and Fix All",
            "type": "shell",
            "command": "poetry run black src/ && poetry run ruff check --fix src/ && poetry run mypy --config-file=.config/mypy.ini src/",
            "problemMatcher": [],
            "group": "build"
        },
        {
            "label": "Pre-commit Install",
            "type": "shell",
            "command": "poetry run pre-commit install",
            "problemMatcher": [],
            "group": "build"
        },
        {
            "label": "Pre-commit Run All",
            "type": "shell",
            "command": "poetry run pre-commit run --all-files",
            "problemMatcher": [],
            "group": "test"
        },
        {
            "label": "Update Dependencies",
            "type": "shell",
            "command": "poetry update",
            "problemMatcher": [],
            "group": "build"
        },
        {
            "label": "Generate Requirements",
            "type": "shell",
            "command": "poetry export -f requirements.txt --output requirements.txt",
            "problemMatcher": [],
            "group": "build"
        }
    ]

    # ... rest of existing code ...