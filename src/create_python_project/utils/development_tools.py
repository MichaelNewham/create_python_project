#!/usr/bin/env python3
"""
Development Tools Module

Handles setup and configuration of development tools like pre-commit hooks,
linting configuration, and code quality tools.
"""

import os
import subprocess
from typing import Any


def setup_development_tools(
    project_dir: str, tech_stack: dict[str, Any]
) -> tuple[bool, str]:
    """
    Set up complete development toolchain for the project.

    Args:
        project_dir: Project directory path
        tech_stack: AI-recommended technology stack

    Returns:
        Tuple of success status and message
    """
    try:
        # Create pre-commit configuration
        _create_precommit_config(project_dir, tech_stack)

        # Create linting configurations
        _create_linting_configs(project_dir)

        # Create development scripts
        _create_dev_scripts(project_dir)

        # Install pre-commit hooks if git is available
        _install_precommit_hooks(project_dir)

        return True, "Development tools configured successfully"

    except Exception as e:
        return False, f"Failed to setup development tools: {str(e)}"


def _create_precommit_config(project_dir: str, tech_stack: dict[str, Any]):
    """Create .pre-commit-config.yaml with appropriate hooks."""

    config_content = """default_stages: [pre-commit]
repos:
  # Code formatting
  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks:
      - id: black
        stages: [pre-commit]
        args: [--line-length=88]

  # Linting and import sorting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix, --config=.config/ruff.toml]
        stages: [pre-commit]

  # Type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.2
    hooks:
      - id: mypy
        args: [--ignore-missing-imports, --config-file=.config/mypy.ini]
        stages: [pre-commit]
        additional_dependencies: [types-requests, types-urllib3]

  # Security scanning
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: package-lock.json

  # General pre-commit hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: check-case-conflict
      - id: check-docstring-first
      - id: debug-statements
      - id: name-tests-test
        args: [--pytest-test-first]

  # Commit message formatting
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.29.1
    hooks:
      - id: commitizen
        stages: [commit-msg]
"""

    # Add framework-specific hooks
    backend_framework = _extract_tech_choice(tech_stack, "Backend Framework")

    if backend_framework == "Django":
        config_content += """
  # Django specific hooks
  - repo: https://github.com/adamchainz/django-upgrade
    rev: 1.21.0
    hooks:
      - id: django-upgrade
        args: [--target-version, "5.0"]
"""

    elif backend_framework == "Flask":
        config_content += """
  # Flask specific hooks
  - repo: https://github.com/Lucas-C/pre-commit-hooks-bandit
    rev: v1.0.6
    hooks:
      - id: python-bandit-vulnerability-check
        args: [-ll]
"""

    # Add frontend hooks if React is used
    if "React" in str(tech_stack):
        config_content += """
  # Frontend hooks (React/TypeScript)
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v9.12.0
    hooks:
      - id: eslint
        files: \\.(js|jsx|ts|tsx)$
        types: [file]
        additional_dependencies:
          - eslint@8.57.0
          - "@typescript-eslint/parser@6.21.0"
          - "@typescript-eslint/eslint-plugin@6.21.0"
"""

    with open(os.path.join(project_dir, ".pre-commit-config.yaml"), "w") as f:
        f.write(config_content)


def _create_linting_configs(project_dir: str):
    """Create comprehensive linting configuration files."""

    config_dir = os.path.join(project_dir, ".config")
    os.makedirs(config_dir, exist_ok=True)

    # Enhanced mypy configuration
    mypy_config = """[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
no_implicit_optional = True
strict_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True
strict_equality = True

# Allow untyped calls for third-party libraries
[[mypy.overrides]]
module = [
    "flask.*",
    "django.*",
    "fastapi.*",
    "cv2.*",
    "kivy.*",
    "celery.*",
    "redis.*",
    "numpy.*",
    "pandas.*",
    "matplotlib.*",
    "seaborn.*",
    "sklearn.*",
    "scipy.*",
    "pytest.*",
    "requests.*"
]
ignore_missing_imports = true

# Relax rules for test files
[[mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
disallow_incomplete_defs = false
"""

    with open(os.path.join(config_dir, "mypy.ini"), "w") as f:
        f.write(mypy_config)

    # Enhanced ruff configuration
    ruff_config = """target-version = "py311"
line-length = 88
indent-width = 4

[lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "SIM", # flake8-simplify
    "UP",  # pyupgrade
    "S",   # flake8-bandit
    "T20", # flake8-print
    "PT",  # flake8-pytest-style
    "Q",   # flake8-quotes
    "RET", # flake8-return
    "C90", # mccabe complexity
]

ignore = [
    "E501",  # Line too long (handled by black)
    "B008",  # Do not perform function calls in argument defaults
    "S101",  # Use of assert detected (fine in tests)
    "T201",  # Print found (fine for CLI apps)
    "S603",  # subprocess without shell check
    "S607",  # Starting a process with a partial executable path
]

[lint.per-file-ignores]
"tests/*" = ["E501", "S101", "PT009", "PT027"]
"migrations/*" = ["E501", "N806"]
"scripts/*" = ["T201", "S603", "S607"]

[lint.mccabe]
max-complexity = 10

[lint.isort]
known-first-party = ["src"]
force-single-line = true

[format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
"""

    with open(os.path.join(config_dir, "ruff.toml"), "w") as f:
        f.write(ruff_config)

    # Create .secrets.baseline for detect-secrets
    baseline_content = """{
  "version": "1.5.0",
  "plugins_used": [
    {
      "name": "ArtifactoryDetector"
    },
    {
      "name": "AWSKeyDetector"
    },
    {
      "name": "AzureStorageKeyDetector"
    },
    {
      "name": "Base64HighEntropyString",
      "limit": 4.5
    },
    {
      "name": "BasicAuthDetector"
    },
    {
      "name": "CloudantDetector"
    },
    {
      "name": "DiscordBotTokenDetector"
    },
    {
      "name": "GitHubTokenDetector"
    },
    {
      "name": "HexHighEntropyString",
      "limit": 3.0
    },
    {
      "name": "IbmCloudIamDetector"
    },
    {
      "name": "IbmCosHmacDetector"
    },
    {
      "name": "JwtTokenDetector"
    },
    {
      "name": "KeywordDetector",
      "keyword_exclude": ""
    },
    {
      "name": "MailchimpDetector"
    },
    {
      "name": "NpmDetector"
    },
    {
      "name": "PrivateKeyDetector"
    },
    {
      "name": "SendGridDetector"
    },
    {
      "name": "SlackDetector"
    },
    {
      "name": "SoftlayerDetector"
    },
    {
      "name": "SquareOAuthDetector"
    },
    {
      "name": "StripeDetector"
    },
    {
      "name": "TwilioKeyDetector"
    }
  ],
  "filters_used": [
    {
      "path": "detect_secrets.filters.allowlist.is_line_allowlisted"
    },
    {
      "path": "detect_secrets.filters.common.is_ignored_due_to_verification_policies",
      "min_level": 2
    },
    {
      "path": "detect_secrets.filters.heuristic.is_indirect_reference"
    },
    {
      "path": "detect_secrets.filters.heuristic.is_likely_id_string"
    },
    {
      "path": "detect_secrets.filters.heuristic.is_lock_file"
    },
    {
      "path": "detect_secrets.filters.heuristic.is_not_alphanumeric_string"
    },
    {
      "path": "detect_secrets.filters.heuristic.is_potential_uuid"
    },
    {
      "path": "detect_secrets.filters.heuristic.is_prefixed_with_dollar_sign"
    },
    {
      "path": "detect_secrets.filters.heuristic.is_sequential_string"
    },
    {
      "path": "detect_secrets.filters.heuristic.is_swagger_file"
    },
    {
      "path": "detect_secrets.filters.heuristic.is_templated_secret"
    }
  ],
  "results": {},
  "generated_at": "2024-01-01T00:00:00Z"
}"""

    with open(os.path.join(project_dir, ".secrets.baseline"), "w") as f:
        f.write(baseline_content)


def _create_dev_scripts(project_dir: str):
    """Create development utility scripts."""

    scripts_dir = os.path.join(project_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    # Quality check script
    quality_script = """#!/usr/bin/env python3
\"\"\"Run all code quality checks.\"\"\"

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, description: str) -> bool:
    \"\"\"Run a command and return success status.\"\"\"
    print(f"\\n🔍 {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ {description} passed")
        return True
    else:
        print(f"❌ {description} failed:")
        print(result.stdout)
        print(result.stderr)
        return False


def main():
    \"\"\"Run all quality checks.\"\"\"
    print("🚀 Running code quality checks...")

    checks = [
        ("poetry run black --check src/ tests/", "Code formatting check"),
        ("poetry run ruff check src/ tests/", "Linting check"),
        ("poetry run mypy --config-file=.config/mypy.ini src/", "Type checking"),
        ("poetry run pytest --cov=src --cov-report=term-missing", "Tests with coverage"),
        ("poetry run detect-secrets scan --baseline .secrets.baseline", "Security scan"),
    ]

    failed_checks = []

    for cmd, description in checks:
        if not run_command(cmd, description):
            failed_checks.append(description)

    if failed_checks:
        print(f"\\n❌ {len(failed_checks)} checks failed:")
        for check in failed_checks:
            print(f"  - {check}")
        sys.exit(1)
    else:
        print("\\n🎉 All quality checks passed!")


if __name__ == "__main__":
    main()
"""

    with open(os.path.join(scripts_dir, "quality_check.py"), "w") as f:
        f.write(quality_script)
    os.chmod(os.path.join(scripts_dir, "quality_check.py"), 0o755)

    # Development setup script
    setup_script = """#!/usr/bin/env python3
\"\"\"Set up development environment.\"\"\"

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, description: str) -> bool:
    \"\"\"Run a command and show progress.\"\"\"
    print(f"📦 {description}...")
    result = subprocess.run(cmd, shell=True)

    if result.returncode == 0:
        print(f"✅ {description} completed")
        return True
    else:
        print(f"❌ {description} failed")
        return False


def main():
    \"\"\"Set up development environment.\"\"\"
    print("🚀 Setting up development environment...")

    setup_steps = [
        ("poetry install --with dev", "Installing Python dependencies"),
        ("npm install", "Installing Node.js dependencies"),
        ("poetry run pre-commit install", "Installing pre-commit hooks"),
        ("poetry run detect-secrets scan --all-files > .secrets.baseline", "Creating secrets baseline"),
    ]

    for cmd, description in setup_steps:
        if not run_command(cmd, description):
            print(f"\\n❌ Setup failed at: {description}")
            sys.exit(1)

    print("\\n🎉 Development environment setup complete!")
    print("\\n📋 Next steps:")
    print("  - Run 'poetry run python scripts/quality_check.py' to verify setup")
    print("  - Use 'poetry run python scripts/commit_workflow.py' for commits")
    print("  - Open the .code-workspace file in VS Code")


if __name__ == "__main__":
    main()
"""

    with open(os.path.join(scripts_dir, "dev_setup.py"), "w") as f:
        f.write(setup_script)
    os.chmod(os.path.join(scripts_dir, "dev_setup.py"), 0o755)


def _install_precommit_hooks(project_dir: str):
    """Install pre-commit hooks if git and poetry are available."""
    try:
        # Check if this is a git repository
        if not os.path.exists(os.path.join(project_dir, ".git")):
            return

        # Try to install pre-commit hooks
        subprocess.run(
            ["poetry", "run", "pre-commit", "install"],
            cwd=project_dir,
            capture_output=True,
            check=False,  # Don't fail if this doesn't work
        )
    except Exception:
        # Installation failed, but continue
        pass


def _extract_tech_choice(tech_stack: dict[str, Any], category_name: str) -> str:
    """Extract the recommended technology for a given category."""
    if isinstance(tech_stack, dict) and "categories" in tech_stack:
        for category in tech_stack["categories"]:
            if category.get("name") == category_name:
                for option in category.get("options", []):
                    if option.get("recommended", False):
                        return str(option["name"])
    return ""


def create_pytest_config(project_dir: str) -> None:
    """Create pytest configuration file."""
    pytest_config = """[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-ra",
    "-q",
    "--strict-markers",
    "--strict-config",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=80"
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "unit: marks tests as unit tests",
    "integration: marks tests as integration tests",
    "e2e: marks tests as end-to-end tests"
]
filterwarnings = [
    "error",
    "ignore::UserWarning",
    "ignore::DeprecationWarning"
]
"""

    # Append to pyproject.toml if it exists
    pyproject_path = os.path.join(project_dir, "pyproject.toml")
    if os.path.exists(pyproject_path):
        with open(pyproject_path, "a") as f:
            f.write("\n" + pytest_config)


def create_coverage_config(project_dir: str) -> None:
    """Create coverage configuration."""
    coverage_config = """
[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/test_*", "*/conftest.py"]
branch = true

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:"
]

[tool.coverage.html]
directory = "htmlcov"
"""

    # Append to pyproject.toml if it exists
    pyproject_path = os.path.join(project_dir, "pyproject.toml")
    if os.path.exists(pyproject_path):
        with open(pyproject_path, "a") as f:
            f.write(coverage_config)
