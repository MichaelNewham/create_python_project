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

- `src/` - Source code
- `tests/` - Test files
- `ai-docs/` - AI documentation
- `scripts/` - Utility scripts
- `.config/` - Configuration files (mypy.ini, etc.)
- `data/` - Sample data
- `notebooks/` - Documentation notebooks

## Project Types

The tool supports various project types and automatically suggests the best match based on your description:

- **Web Application**: FastAPI or Flask-based web applications
- **Data Analysis/Visualization**: Projects using Pandas, NumPy, Plotly, etc.
- **API Integration**: Integration with third-party APIs
- **User Authentication**: Projects with authentication systems
- **CLI Tools**: Command-line interface applications
- **Automation**: Background services and automation scripts
- **AI/ML**: Machine learning applications with model integration

## Project Structure

The tool generates an optimized project structure based on your selected project types and technologies. For example, a web application with data visualization might include:

```
my_project/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core functionality
│   │   ├── db/           # Database models and connections
│   │   ├── schemas/      # Data validation schemas
│   │   └── services/     # Business logic
│   ├── migrations/
│   ├── tests/
│   └── pyproject.toml
├── frontend/             # If a frontend is included
├── docker/               # Docker configuration
├── docker-compose.yml
├── .github/workflows/    # CI/CD configuration
├── README.md
└── .gitignore
```

The structure adapts to your specific project needs and selected technologies.

## AI Integration

The project supports multiple AI providers for intelligent project setup:

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

---

**Note:** This file has been automatically truncated to 150 lines maximum.
Full content was 154 lines. Last updated: 2025-05-17 01:05:28
