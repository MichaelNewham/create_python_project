# Create Python Project - Custom Instructions for GitHub Copilot

## Project Overview
This project provides a CLI tool for creating standardized Python project scaffolding using Poetry. It automates the setup of best practices for project structure, testing, linting, and documentation.

## Tech Stack
- **Python**: Primary language (3.10+)
- **Poetry**: Package and dependency management
- **pytest**: Testing framework
- **Black**: Code formatting
- **mypy**: Type checking
- **detect-secrets**: Security scanning

## Coding Standards

### Python Style
- Follow PEP 8 conventions
- Use 4 spaces for indentation
- Maximum line length of 88 characters (Black default)
- Use snake_case for variables, functions, methods, and modules
- Use PascalCase for class names
- Use ALL_UPPERCASE for constants
- Include type hints for all function parameters and return values

### Documentation
- Every module, class, and function should have a docstring
- Follow Google-style docstrings format
- Include examples in docstrings for public APIs

### Testing
- All code should have corresponding unit tests
- Use pytest fixtures for test setup
- Target high test coverage (aim for 80%+)
- Tests should be isolated and not depend on external resources

### Error Handling
- Use explicit exception handling with specific exception types
- Log errors with appropriate context
- Provide meaningful error messages to users

### Imports
- Group imports in the following order:
  1. Standard library imports
  2. Related third-party imports
  3. Local application/library specific imports
- Sort imports alphabetically within each group
- Use absolute imports rather than relative imports

## Project Structure
- Use the standard Poetry project structure
- Keep modules focused and single-purpose
- Place reusable utilities in the utils module
- Configuration should be handled through environment variables or config files
- Organize tests to mirror the structure of the source code

## CLI Design
- Use clear, descriptive command and option names
- Provide helpful error messages and usage examples
- Follow consistent patterns for command structure
- Include command completion where appropriate

## Security
- Avoid hardcoded secrets
- Use secure practices for handling user data
- Scan for secrets in the codebase regularly

## Version Control
- Commit messages should be clear and descriptive
- Follow conventional commits format (feat, fix, docs, etc.)
- Update documentation when changing public APIs
