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

1. **Main Module** (`create_python_project.py`): Entry point that orchestrates the CLI interface and comprehensive AI-driven project creation flow.

2. **Core Project Builder** (`utils/core_project_builder.py`): Handles dynamic file creation, directory structure, and technology installation based on AI recommendations.

3. **AI Integration** (`utils/ai_integration.py`): Manages connections with multiple AI providers (OpenAI, Anthropic, Perplexity, DeepSeek, Gemini) for generating comprehensive project analysis.

4. **AI Prompts** (`utils/ai_prompts.py`): Contains advanced prompt templates for comprehensive project analysis including architecture recommendations and technology justifications.

5. **Project Templates** (`utils/project_templates.py`): Dynamic template system that creates project structures based on AI technology analysis rather than hardcoded project types.

6. **Dynamic Installation System** (`utils/core_project_builder.py`): Automatically installs all AI-recommended technologies (Python packages via Poetry, Node.js packages via npm).

7. **CLI Utilities** (`utils/cli.py`): Rich terminal UI for enhanced user experience with professional output formatting.

8. **Configuration** (`utils/config.py`): Dynamic configuration management supporting any technology combination.

9. **Logging** (`utils/logging.py`): Clean logging system with debug information captured in files, not displayed to users.

## Revolutionary AI-Driven Workflow

**Major Innovation: Comprehensive Single-Step AI Analysis**

The new workflow eliminates artificial constraints and provides intelligent, coherent solutions:

1. **Project Context Collection**: User provides detailed problem description, target users, and inspiration sources
2. **AI Provider Selection**: Choose from DeepSeek, Anthropic, Perplexity, OpenAI, or Gemini based on project needs
3. **Comprehensive AI Analysis**: Single AI call provides complete solution including:
   - Recommended architecture with detailed reasoning
   - Complete technology stack with specific justifications
   - Project structure preview and user experience description
   - Future flexibility and expansion options
4. **Dynamic Project Creation**: System creates project structure based on actual AI recommendations, not predetermined templates
5. **Automatic Technology Installation**: All AI-recommended technologies are automatically installed (Python + Node.js)
6. **Complete Development Environment**: Git, workspace configuration, development tools, and automation scripts

## Key Architectural Improvements

### **Comprehensive AI Analysis System**
- Single AI call replaces separate "project type" and "technology stack" steps
- AI provides complete architectural reasoning, not just technology lists
- Eliminates conflicts between project type and technology selections
- Future-proof: handles any technology combination AI recommends

### **Dynamic Project Structure Creation**
- No hardcoded project types or technology assumptions
- Analyzes AI recommendations to determine appropriate structure:
  - GUI frameworks → Desktop applications
  - Frontend + Backend → Full-stack web applications  
  - CLI tools → Command-line applications
  - Data processing tools → Data analysis projects
  - Electron + React → Cross-platform desktop apps
- Supports hybrid approaches (e.g., web apps that can be packaged as desktop)

### **Universal Technology Installation**
- Dynamic mapping system supports 50+ technologies
- Automatically installs Python packages via Poetry
- Automatically installs Node.js packages via npm
- Handles frontend dependencies in separate directories
- Provides installation summaries and error handling

### **Enhanced User Experience**
- Clean, professional terminal output without debug noise
- Comprehensive technology explanations with reasoning
- Alternative architecture options clearly presented
- Future flexibility options highlighted
- Real-time progress indication

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

## PRD Stage Features

This is the PRD Stage development branch featuring expert AI personas:

### Expert AI Personas
- **Anya Sharma (Principal UI/UX Lead)**: User experience design and interaction patterns
- **Ben Carter (Senior Product Lead)**: Market strategy, business objectives, and feature prioritization  
- **Dr. Chloe Evans (Chief Software Architect)**: Technical architecture and system design

### Enhanced Workflow
1. Project vision collection with comprehensive problem description
2. Multi-expert AI consultation for holistic product analysis
3. Integrated requirements synthesis for unified PRD generation
4. Strategic project generation based on expert recommendations
5. Auto-generated TaskMaster/ directory with PRD documentation

## Core Architecture Patterns

### AI Provider Management
- Multiple provider support with automatic fallback mechanisms
- Provider-specific optimizations and token management
- Dynamic model selection based on task requirements

### Template System Architecture  
- Dynamic template generation based on AI recommendations
- No hardcoded project types - fully adaptive to AI suggestions
- Supports hybrid project structures (e.g., web apps that can be packaged as desktop)

### Installation System
- Universal technology installation supporting 50+ technologies
- Dynamic mapping between AI recommendations and package managers
- Separate handling for Python (Poetry) and Node.js (npm) dependencies

## Development Instructions from Cursor/Copilot Rules

### Code Style Requirements
- Maximum line length of 88 characters (Black default)
- Use Google-style docstrings format for all functions and classes
- Include type hints for all function parameters and return values
- Use explicit exception handling with specific exception types

### Testing Standards
- All code should have corresponding unit tests using pytest
- Use pytest fixtures for test setup (defined in `tests/conftest.py`)
- Target high test coverage (aim for 80%+)
- Mock external API calls and file system operations

### Import Organization
1. Standard library imports
2. Related third-party imports  
3. Local application/library specific imports
- Sort imports alphabetically within each group

## Recommended Memory Management

Consistently keep in memory:
- This CLAUDE.md file
- The main README.md in the root folder
- The aboutthisfolder.md files in most folders directly under the root folder