# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Create Python Project is an all-in-one Python project creator with intelligent setup based on project description and built-in AI integration. It provides a rich CLI interface to scaffold Python projects with best practices.

## Development Commands

### Installation

```bash
# Install with Poetry (recommended)
poetry install --with dev

# Or with pip in a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### Running the Application

```bash
# With Poetry
poetry run python -m create_python_project.create_python_project

# Or after installing the package
create-python-project
```

### Code Quality Checks

```bash
# Type checking with mypy
poetry run mypy --config-file=.config/mypy.ini src/create_python_project

# Format code with Black (line length 88)
poetry run black src/create_python_project

# Linting and auto-fixing with Ruff (replaces isort, flake8, autopep8, pyupgrade, autoflake)
poetry run ruff check src/create_python_project --fix

# Security scanning
poetry run detect-secrets scan --all-files
```

### Testing

```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=src/create_python_project

# Run a specific test file
poetry run pytest tests/test_ai_integration.py

# Run a specific test function
poetry run pytest tests/test_ai_integration.py::test_function_name

# Run tests with verbose output
poetry run pytest -v
```

## Architecture Overview

The application is organized into several key components:

1. **Main Module** (`create_python_project.py`): Entry point that orchestrates the CLI interface and project creation flow.

2. **Core Project Builder** (`utils/core_project_builder.py`): Handles file creation, directory structure, and template rendering for different project types.

3. **AI Integration** (`utils/ai_integration.py`): Manages connections with multiple AI providers (OpenAI, Anthropic, Perplexity, DeepSeek, Gemini) for generating project recommendations.

4. **AI Prompts** (`utils/ai_prompts.py`): Contains prompt templates for different AI queries like project type detection and dependency recommendations.

5. **Templates** (`utils/templates.py`): Provides project templates and utilities for generating files based on project type.

6. **Project Templates** (`utils/project_templates.py`): Contains specific template definitions for different project types (CLI, Web, Data Analysis, etc.).

7. **Task Configuration** (`utils/task_config.py`): Manages VS Code task definitions for each project type.

8. **CLI Utilities** (`utils/cli.py`): Helper functions for handling command-line interface operations with rich terminal UI.

9. **Configuration** (`utils/config.py`): Manages configuration settings and project type definitions.

10. **Logging** (`utils/logging.py`): Sets up structured logging for the application.

The workflow is:
1. User initiates the application
2. System collects project info via CLI (name, location, author)
3. AI analyzes project description to recommend project type
4. System presents AI-recommended technologies for user selection
5. System scaffolds project structure based on type and selected technologies
6. Git repository and virtual environment are optionally set up
7. MCP servers are optionally configured

## Coding Standards

### Python Style
- Follow PEP 8 conventions with 4 spaces for indentation
- Maximum line length of 88 characters (Black default)
- Use snake_case for variables, functions, methods, and modules
- Use PascalCase for class names
- Include type hints for all function parameters and return values
- Follow Google-style docstrings format

### Import Organization
1. Standard library imports
2. Related third-party imports
3. Local application/library specific imports

### Testing Approach
- All code should have corresponding unit tests
- Use pytest fixtures for test setup (defined in `tests/conftest.py`)
- Tests mirror the source code structure
- Mock external API calls and file system operations

## Configuration Files

- **`.config/mypy.ini`**: Type checking configuration with specific error codes disabled for template files
- **`.config/ruff.toml`**: Linting configuration (line length 100, Python 3.11 target)
- **`pyproject.toml`**: Poetry configuration with tool settings for mypy and ruff
- **`.vscode/settings.json`**: Extensive VS Code configuration for Python development

## Environment Setup

The project requires environment variables for AI provider API keys:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `PERPLEXITY_API_KEY`
- `DEEPSEEK_API_KEY`
- `GEMINI_API_KEY`

Copy `.env.example` to `.env` and fill in your API keys before running.