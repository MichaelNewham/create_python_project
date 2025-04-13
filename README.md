# Create Python Project

An all-in-one Python project creator with intelligent setup based on project description.

***

## Features

- Interactive GUI-based setup using Zenity dialogs
- AI-powered project type detection and recommendation
- Support for multiple project types (Web, CLI, Automation, AI, Data)
- Integration with multiple AI providers (Anthropic, OpenAI, DeepSeek)
- Docker and systemd support
- Security modules for web applications
- VS Code integration with task definitions and launch configurations
- Comprehensive logging setup

## Installation

```bash
# Clone the repository
git clone https://github.com/MichaelNewham/create_python_project.git
cd create_python_project

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

## Usage

```bash
# Run the script directly
python -m create_python_project.create_python_project

# Or use the installed command
create-python-project
```

## Development

```bash
# Run tests
pytest

# Run linting
pylint create_python_project

# Format code
black create_python_project
```

## Project Types

- **Web**: Flask or FastAPI web applications
- **CLI**: Command-line interface applications
- **Automation**: Background services and automation scripts
- **AI**: AI/ML applications with model integration
- **Data**: Data processing and analysis

## License

MIT
