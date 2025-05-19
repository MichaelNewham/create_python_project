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

# Format code with Black
poetry run black src/create_python_project

# Linting with pylint
poetry run pylint src/create_python_project

# Using ruff (fast linter)
poetry run ruff src/create_python_project
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
```

## Architecture Overview

The application is organized into several key components:

1. **Main Module** (`create_python_project.py`): Entry point that orchestrates the CLI interface and project creation flow.

2. **Core Project Builder** (`utils/core_project_builder.py`): Handles file creation, directory structure, and template rendering for different project types.

3. **AI Integration** (`utils/ai_integration.py`): Manages connections with multiple AI providers (OpenAI, Anthropic, Perplexity, DeepSeek, Gemini) for generating project recommendations.

4. **AI Prompts** (`utils/ai_prompts.py`): Contains prompt templates for different AI queries like project type detection and dependency recommendations.

5. **Templates** (`utils/templates.py`): Provides project templates and utilities for generating files based on project type.

6. **CLI Utilities** (`utils/cli.py`): Helper functions for handling command-line interface operations.

7. **Configuration** (`utils/config.py`): Manages configuration settings and project type definitions.

8. **Logging** (`utils/logging.py`): Sets up logging for the application.

The workflow is:
1. User initiates the application
2. System collects project info via CLI
3. AI analyzes project description to recommend project type
4. System scaffolds project structure based on type
5. Git repository and virtual environment are optionally set up

The project uses Poetry for dependency management and follows modern Python practices with proper typing and comprehensive error handling.