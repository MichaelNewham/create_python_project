# Create Python Project ⭐

An all-in-one Python project creator with intelligent setup based on project description and built-in AI integration.

***

## Features

- Interactive CLI-based setup with rich colorful interface and intelligent defaults
- AI-powered project type detection based on your project description
- Multiple AI provider integrations including OpenAI, Anthropic, Perplexity, DeepSeek, and Gemini
- Support for multiple project types (Web, Data Analysis, API Integration, etc.)
- AI-recommended technology selection with customizable options
- Project structure visualization with organized, best-practice directory layouts
- VS Code integration with workspace files and task definitions
- Comprehensive logging system with detailed error tracking
- Docker, CI/CD, and pre-commit hook configuration options
- Git repository setup with dual remote support (GitHub and GitLab)

## Installation

```bash
# Clone the repository
git clone https://github.com/MichaelNewham/create_python_project.git
cd create_python_project

# Install with Poetry (recommended)
poetry install

# Or with pip in a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

## Configuration

This project requires some configuration for MCP and VS Code integration:

1. **Environment Variables**: Copy the example .env file and fill in your API keys
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **VS Code Settings**:
   ```bash
   cp .vscode/settings.json.template .vscode/settings.json
   cp .vscode/mcp.json.template .vscode/mcp.json
   ```

For more information on security best practices:
- [MCP Setup Guide](docs/MCP_SETUP.md)
- [VS Code Security Guide](docs/VSCODE_SECURITY.md)

## Usage

```bash
# With Poetry
poetry run python -m create_python_project.create_python_project

# Or after installing the package
create-python-project
```

The interactive process will guide you through:
1. Setting up your project name and location
2. Selecting an AI provider for recommendations
3. Describing your project for AI analysis
4. Selecting from AI-recommended technologies
5. Configuring additional options (Docker, CI/CD, etc.)
6. Creating the project with the optimal structure

## Development

```bash
# Install all dependencies including development dependencies
poetry install --with dev

# Run type checking to verify all issues are fixed
poetry run mypy --config-file=.config/mypy.ini src/create_python_project

# Test the application
poetry run python -m create_python_project.create_python_project

# Run AI integration tests
poetry run pytest tests/test_ai_integration.py -v

# Format code with Black
poetry run black src/create_python_project
```

## Project Organization

The project follows a clean organization structure:

... (truncated for brevity) ...


1. **OpenAI**: GPT-4o-mini and other OpenAI models
2. **Anthropic**: Claude 3.7 Sonnet and other Claude models
3. **Perplexity**: Sonar model for project analysis
4. **DeepSeek**: DeepSeek Chat model
5. **Gemini**: Gemini 2.5 Pro and other Gemini models

Each provider helps with:
- Project type detection based on your description
- Recommending appropriate technologies and libraries
- Suggesting optimal project structure
- Providing implementation guidance

## License

MIT

## Last Updated

This project was last updated on: 2025-05-22 01:07:57

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-22 01:05:10

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-21 00:55:41

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-20 01:22:28

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-20 00:52:06

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-20 00:19:41

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-19 23:38:59

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-19 23:06:30

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-18 00:26:21

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-18 00:25:48

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-18 00:25:41

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-18 00:25:24

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-18 00:25:07

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-18 00:17:52

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-17 02:05:26

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-17 02:03:17

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-17 01:59:20

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-17 01:56:52

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-17 01:54:30

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-17 01:53:55

Run `./scripts/update_documentation.sh` to update documentation.

This project was last updated on: 2025-05-17 01:51:53

Run `./scripts/update_documentation.sh` to update documentation.

---

**Note:** This file has been automatically truncated to 150 lines maximum.
Full content was 154 lines. Last updated: 2025-05-17 01:23:47

## Project Structure

The project is organized as follows:

- **ai-docs/**: AI-related documentation and conversation logs
- **imagesandvids/**: Project files
- **logs/**: Log output files
- **scripts/**: Automation scripts for development workflow
- **src/**: Main implementation code
- **tests/**: Test files for the project

### Configuration Directories

- **.claude/**: Configuration files
- **.config/**: Configuration files for linters and tools
- **.git/**: Configuration files
- **.github/**: GitHub workflows and configuration

