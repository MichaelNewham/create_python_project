# Create Python Project ⭐

An all-in-one Python project creator with intelligent setup based on project description and built-in AI integration.

***

## Features

- Interactive CLI-based setup with intelligent defaults
- AI-powered project type detection based on project description
- Compulsory AI integration with multiple providers (Anthropic, OpenAI, DeepSeek)
- Support for multiple project types (Web, CLI, Automation, AI, Data)
- VS Code integration with workspace files and task definitions
- Claude Code integration with .claude configuration
- Comprehensive logging setup with detailed error tracking
- Automatic creation of project structure with best practices
- AI conversation logs stored in ai-docs directory
- Project specifications stored in specs directory

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

## Usage

```bash
# With Poetry
poetry run python -m create_python_project.create_python_project

# Or after installing the package
create-python-project

# Optional parameters
create-python-project --name "my-project" --dir "/path/to/save"
```

## Development

```bash
# Run tests
pytest

# Run linting
pylint create_python_project

# Run type checking
mypy --config-file=.config/mypy.ini src/create_python_project

# Format code
black create_python_project
```

## Project Organization

The project follows a clean organization structure:

- `src/` - Source code
- `tests/` - Test files
- `ai-docs/` - AI documentation
- `scripts/` - Utility scripts
- `.config/` - Configuration files (mypy.ini, etc.)
- `data/` - Sample data
- `notebooks/` - Documentation notebooks

## Project Types

- **Web**: Flask or FastAPI web applications
- **CLI**: Command-line interface applications
- **Automation**: Background services and automation scripts
- **AI**: AI/ML applications with model integration
- **Data**: Data processing and analysis

## Project Structure

The generated project structure follows best practices and includes:

```
project_name/
├── project_name.code-workspace    # VS Code workspace file
├── .claude                        # Claude Code configuration
├── README.md                      # Project documentation
├── pyproject.toml                 # Poetry package configuration
├── .vscode/                       # VS Code configuration
│   └── mcp.json                   # MCP configuration
├── ai-docs/                       # AI documentation
│   ├── aboutthisfolder.md         # Folder documentation
│   └── convo.md                   # AI conversation logs
├── specs/                         # Project specifications
│   └── aboutthisfolder.md         # Folder documentation
├── tests/                         # Test files
│   ├── __init__.py                # Package marker
│   └── aboutthisfolder.md         # Folder documentation
└── src/                           # Source code
    ├── aboutthisfolder.md         # Folder documentation
    └── project_name/              # Main module
        ├── __init__.py            # Package marker
        └── utils/                 # Utility modules
            ├── __init__.py        # Package marker
            ├── logging.py         # Logging configuration
            └── ai_provider.py     # AI provider integration
```

## AI Integration

The project includes built-in AI integration with:

1. **AI Provider Module**: A utility module for interacting with AI services
2. **Claude Code Integration**: Configuration for Claude Code in VS Code
3. **Conversation Logs**: Storage for AI conversation history
4. **Multiple Provider Support**:
   - Anthropic (Claude models)
   - OpenAI (GPT models)
   - DeepSeek (DeepSeek models)

## License

MIT
