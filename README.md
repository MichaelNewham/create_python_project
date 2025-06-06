# Create Python Project - PRD Stage (Development)

**🚧 DEVELOPMENT VERSION - Advanced PRD-Driven Project Creation**

A revolutionary CLI tool that uses expert AI personas to guide comprehensive Product Requirements Document (PRD) development and intelligent project creation. This advanced version goes beyond basic scaffolding to provide strategic product planning with input from simulated domain experts.

> **Note**: This is the PRD Stage development branch. For the stable Basic version, see the `main` branch.

## 🚀 Key Features

### 🎯 PRD Stage Innovation: Expert AI Personas
- **Virtual Domain Experts**: Three specialized AI personas guide comprehensive product analysis:
  - **Anya Sharma (Principal UI/UX Lead)**: User experience design and interaction patterns
  - **Ben Carter (Senior Product Lead)**: Market strategy, business objectives, and feature prioritization  
  - **Dr. Chloe Evans (Chief Software Architect)**: Technical architecture and system design
- **Comprehensive Requirements Gathering**: Multi-perspective analysis ensuring no critical aspects are overlooked
- **Strategic Product Planning**: Goes beyond code generation to create complete product strategies

### AI-Powered Project Generation
- **Multi-AI Provider Support**: Integrates with OpenAI, Anthropic Claude, Perplexity, DeepSeek, and Google Gemini
- **PRD-Driven Architecture**: Project structure based on comprehensive product requirements analysis
- **Expert-Guided Decision Making**: AI personas provide domain-specific recommendations and validation
- **Adaptive Configuration**: Dynamic project setup based on holistic product understanding

### Comprehensive Project Scaffolding
- **Standardized Project Structure**: Creates well-organized layouts following Python best practices
- **Poetry Integration**: Automated Poetry setup for dependency management and packaging
- **Multi-Framework Support**: Templates for CLI tools, web APIs, data science projects, and more
- **Testing Infrastructure**: Configures pytest with coverage reporting, fixtures, and example tests
- **Code Quality Pipeline**: Sets up Black, Ruff, mypy, and pre-commit hooks
- **Security & Documentation**: Integrates detect-secrets scanning and comprehensive documentation setup

### Development Tools & Automation
- **GitHub Integration**: Automated CI/CD workflows, issue templates, and repository setup
- **Script Templates**: Pre-configured development, testing, and deployment scripts
- **Environment Management**: Python environment detection and configuration
- **Logging & Monitoring**: Structured logging with configurable levels and output formats

### 📋 TaskMaster AI Integration
- **Automatic PRD Directory**: Every project includes a `TaskMaster/` directory ready for Product Requirements Documents
- **Expert Consultation Logs**: Complete records of AI expert analyses and provider assignments
- **TaskMaster Compatibility**: Generated PRDs are fully compatible with TaskMaster AI workflows
- **Professional Documentation**: Comprehensive guides and templates for product planning

## 🛠 Installation

### Prerequisites
- Python 3.10 or higher
- Poetry (recommended) or pip
- Git (for version control features)

### Quick Install
```bash
# Install from source (recommended for latest features)
git clone https://github.com/MichaelNewham/create_python_project.git
cd create_python_project
poetry install --with dev

# Or install dependencies directly
pip install -r requirements.txt
```

### AI Provider Setup (Optional)
Configure API keys for AI-powered features:
```bash
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export PERPLEXITY_API_KEY="your-perplexity-key"
export DEEPSEEK_API_KEY="your-deepseek-key"
export GEMINI_API_KEY="your-gemini-key"
```

## 📖 Usage

### PRD Stage Project Creation
```bash
# Create a new Python project with expert AI persona guidance
poetry run python -m create_python_project.create_python_project

# Or use the direct script
python src/create_python_project/create_python_project.py
```

### Enhanced PRD Stage Workflow
The PRD Stage introduces a revolutionary multi-expert consultation process:

1. **Project Vision Collection**: Comprehensive problem description and target user analysis
2. **Expert AI Persona Consultation**: 
   - **Anya (UX Lead)**: User experience requirements and design patterns
   - **Ben (Product Lead)**: Business objectives, market analysis, and feature prioritization
   - **Chloe (Architect)**: Technical requirements, scalability, and system architecture
3. **Integrated Requirements Analysis**: AI personas collaborate to create comprehensive PRD
4. **Strategic Technology Selection**: Architecture-driven technology recommendations
5. **Advanced Project Generation**: PRD-informed project structure and implementation
6. **Expert Validation**: Multi-perspective review ensuring product viability

### Key Improvements Over Basic Version
- **Strategic Product Thinking**: Beyond code scaffolding to complete product strategy
- **Multi-Expert Validation**: Every decision validated from UX, Product, and Technical perspectives
- **Comprehensive Analysis**: Market considerations, user needs, and technical constraints
- **Future-Proof Architecture**: Scalable designs informed by expert architectural principles

### Command-Line Options
- **Interactive Mode**: Default guided setup process
- **AI Provider Selection**: Choose from OpenAI, Anthropic, Perplexity, DeepSeek, or Gemini
- **Project Templates**: Web APIs, Data Analysis, CLI Tools, Libraries, and more
- **Integration Options**: GitHub/GitLab setup, Docker configuration, CI/CD pipelines
- **VS Code Integration**: Workspace files, task definitions, and extension recommendations

## 📁 Generated Project Structure

```
my-awesome-project/
├── src/
│   └── my_awesome_project/
│       ├── __init__.py
│       ├── main.py
│       ├── cli.py                    # CLI interface
│       ├── config.py                 # Configuration management
│       └── utils/
│           ├── __init__.py
│           ├── logging.py            # Structured logging
│           └── helpers.py            # Utility functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py                   # pytest configuration
│   ├── test_main.py
│   ├── test_cli.py
│   └── test_utils.py
├── docs/
│   ├── README.md
│   ├── CONTRIBUTING.md
│   ├── CHANGELOG.md
│   └── api/                          # API documentation
├── TaskMaster/
│   ├── README.md                     # PRD directory guide
│   ├── PRD_{project}_{date}.md       # Generated PRDs (PRD Stage)
│   └── Expert_Consultation_Log_{date}.md  # Expert analysis logs
├── scripts/
│   ├── setup.sh                      # Environment setup
│   ├── lint.sh                       # Code quality checks
│   └── deploy.sh                     # Deployment scripts
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                    # Continuous integration
│   │   ├── release.yml               # Release automation
│   │   └── security.yml              # Security scanning
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
├── .config/
│   ├── mypy.ini                      # Type checking config
│   └── ruff.toml                     # Linting configuration
├── pyproject.toml                    # Project metadata & dependencies
├── README.md                         # Project documentation
├── .gitignore                        # Git ignore rules
├── .pre-commit-config.yaml           # Pre-commit hooks
├── .secrets.baseline                 # Security baseline
└── my-awesome-project.code-workspace # VS Code workspace
```

## 🤖 AI Integration Features

### Supported AI Providers
- **OpenAI GPT Models**: GPT-4o-mini and other OpenAI models for advanced code generation
- **Anthropic Claude**: Claude 3.7 Sonnet for detailed analysis and documentation
- **Perplexity AI**: Sonar model for research-driven project recommendations
- **DeepSeek**: DeepSeek Reasoner for advanced reasoning and complex problem analysis
- **Google Gemini**: Gemini 2.5 Pro for multi-modal project understanding

### PRD Stage AI-Powered Capabilities
- **Multi-Expert Product Analysis**: Comprehensive evaluation from UX, Product, and Technical perspectives
- **Strategic Architecture Planning**: System design informed by scalability and maintainability principles
- **User-Centered Design Integration**: UX patterns and interaction models baked into project structure
- **Market-Informed Technology Selection**: Technology choices validated against business objectives
- **Comprehensive Requirements Documentation**: Auto-generated PRD with expert insights
- **Future-Proof Configuration**: Project setup designed for long-term evolution and scaling

## 🔧 Development

### Development Environment Setup
```bash
# Clone and setup
git clone https://github.com/MichaelNewham/create_python_project.git
cd create_python_project

# Install with development dependencies
poetry install --with dev

# Setup pre-commit hooks
poetry run pre-commit install
```

### Available Tasks (VS Code)
The project includes pre-configured VS Code tasks:
- **Lint All**: Run comprehensive linting across the codebase
- **Test Coverage**: Execute tests with coverage reporting
- **Format and Lint Code**: Automated code formatting and linting
- **Run Mypy**: Type checking with daemon mode
- **Find Secrets**: Security scanning for exposed secrets
- **Update Docs**: Automated documentation updates
- **Build Package**: Create distribution packages

### Testing
```bash
# Run all tests with coverage
poetry run pytest --cov=create_python_project tests/

# Run specific test categories
poetry run pytest tests/test_ai_integration.py      # AI provider tests
poetry run pytest tests/test_cli.py                 # CLI functionality
poetry run pytest tests/test_templates.py           # Template generation
poetry run pytest tests/test_core_project_builder.py # Project creation
```

### Code Quality
```bash
# Format code
poetry run black src/create_python_project

# Lint and fix issues
poetry run ruff check --fix src/create_python_project

# Type checking
poetry run mypy --config-file=.config/mypy.ini src/create_python_project

# Security scanning
poetry run detect-secrets scan --all-files

# Run all checks
poetry run pre-commit run --all-files
```

## 📚 Configuration

### Environment Setup
For full functionality, configure:

1. **Environment Variables**: Copy `.env.example` to `.env` and add API keys
2. **VS Code Settings**: 
   ```bash
   cp .vscode/settings.json.template .vscode/settings.json
   cp .vscode/mcp.json.template .vscode/mcp.json
   ```

### AI Provider Configuration
The tool automatically detects available API keys and presents options for:
- Model selection per provider
- Temperature and token limits
- Provider-specific optimizations
- Fallback mechanisms for reliability

### Security Best Practices
- API keys stored in environment variables
- Secrets detection with detect-secrets
- Pre-commit hooks for security scanning
- Comprehensive `.gitignore` for sensitive files

## 🚀 Project Architecture

### Core Components
- **`create_python_project.py`**: Main CLI interface and workflow orchestration
- **`utils/ai_integration.py`**: Multi-provider AI integration and management
- **`utils/config.py`**: Configuration management and validation
- **`utils/project_templates.py`**: Project scaffolding and template generation
- **`utils/cli.py`**: CLI utilities and user interaction helpers

### PRD Stage Workflow Architecture
1. **Initial Vision Capture**: Comprehensive problem and user context collection
2. **Multi-Expert AI Consultation**: Sequential consultation with specialized personas
   - **UX Expert (Anya)**: User research, interaction patterns, accessibility
   - **Product Expert (Ben)**: Market analysis, business objectives, feature prioritization
   - **Technical Expert (Chloe)**: Architecture design, scalability, implementation strategy
3. **Integrated Requirements Synthesis**: AI personas collaborate to create unified PRD
4. **Strategic Project Generation**: Architecture and requirements-driven scaffolding
5. **Expert-Validated Configuration**: Multi-perspective validation of all technical decisions
6. **Comprehensive Documentation**: Auto-generated PRD, technical docs, and implementation guides

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Steps
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes following our coding standards
4. **Test** your changes (`poetry run pytest`)
5. **Lint** your code (`poetry run pre-commit run --all-files`)
6. **Commit** with conventional commit format (`git commit -m 'feat: add amazing feature'`)
7. **Push** to your branch (`git push origin feature/amazing-feature`)
8. **Open** a Pull Request

### Development Standards
- Follow PEP 8 and use Black formatting (88 char line length)
- Include type hints for all functions and methods
- Write comprehensive docstrings (Google style)
- Maintain test coverage above 80%
- Update documentation for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Poetry** for excellent dependency management
- **AI Provider APIs** for intelligent code generation capabilities
- **Python Packaging Community** for best practices and standards
- **Open Source Contributors** who help improve this tool
- **VS Code** for excellent development environment integration

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/MichaelNewham/create_python_project/issues)
- **Discussions**: [GitHub Discussions](https://github.com/MichaelNewham/create_python_project/discussions)
- **Documentation**: [Project Documentation](ai-docs/)

---

**PRD Stage Development Branch | Revolutionary Expert AI-Guided Project Creation**

> 🚧 **Development Status**: This branch contains experimental PRD Stage features. 
> For stable project creation, use the `main` branch (Basic Version).

**Built with ❤️ and expert AI personas | Transforming how Python projects are conceived and created**

*Last Updated: 2025-06-06 | PRD Stage Development*
