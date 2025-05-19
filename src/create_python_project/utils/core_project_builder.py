#!/usr/bin/env python3
"""
Core Project Builder Module

This module contains the core functionality for creating Python projects.
It handles file creation, directory structure, and template rendering.
"""

import os
import shutil
import subprocess
from typing import Any, Tuple


def create_project_structure(
    project_name: str,
    project_dir: str,
    project_type: str,
    with_ai: bool = True,
    tech_stack: dict = None,
    **kwargs: Any,
) -> Tuple[bool, str]:
    """
    Create the base project structure.

    Args:
        project_name: Name of the project
        project_dir: Directory where the project should be created
        project_type: Type of the project (web, cli, etc.)
        with_ai: Whether to include AI integration
        tech_stack: Dictionary containing AI-recommended technology stack
        **kwargs: Additional parameters for project creation

    Returns:
        Tuple containing success status and message
    """
    try:
        tech_stack = tech_stack or {}
        package_name = project_name.replace("-", "_").replace(" ", "_").lower()

        # Create project directory if it doesn't exist
        os.makedirs(project_dir, exist_ok=True)

        # Extract recommended technologies if available
        recommended_techs = {}
        if "categories" in tech_stack:
            for category in tech_stack["categories"]:
                for option in category["options"]:
                    if option.get("recommended", False):
                        # Store by category and individual technology
                        recommended_techs[category["name"]] = option["name"]
                        recommended_techs[option["name"].lower()] = True

        # Create README with tech stack information
        readme_content = (
            f"# {project_name}\n\n{kwargs.get('description', 'A Python project.')}\n\n"
        )

        if recommended_techs:
            readme_content += "## Technologies\n\n"
            for category in tech_stack.get("categories", []):
                category_name = category["name"]
                if category_name in recommended_techs:
                    readme_content += (
                        f"- **{category_name}**: {recommended_techs[category_name]}\n"
                    )
            readme_content += "\n"

        readme_content += """## Installation

```bash
# Install with Poetry (recommended)
poetry install

# Or with pip
pip install -e .
```

## Usage

Documentation for usage will be added here.

## License

MIT
"""

        # Create base files
        base_files = {
            "README.md": readme_content,
            ".gitignore": """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environments
venv/
.env
.venv
env/
ENV/

# IDE files
.idea/
.vscode/
*.swp
*.swo

# Logs
logs/
*.log
            """,
        }

        # Create pyproject.toml with recommended dependencies
        dependencies = []
        dev_dependencies = [
            'pytest = "^7.3.1"',
            'black = "^23.3.0"',
            'pylint = "^2.17.4"',
            'mypy = "^1.3.0"',
            'pytest-cov = "^4.1.0"',
        ]

        # Add dependencies based on project type and tech stack
        # Define common technology mappings
        tech_mapping = {
            # Web frameworks
            "fastapi": {
                "package": "fastapi",
                "version": "^0.101.0",
                "requires": ['uvicorn = "^0.23.2"'],
            },
            "django": {"package": "django", "version": "^4.2.4"},
            "flask": {"package": "flask", "version": "^2.3.2"},
            # Databases
            "postgresql": {
                "package": "psycopg2-binary",
                "version": "^2.9.7",
                "suggests": ["sqlalchemy"],
            },
            "mongodb": {"package": "pymongo", "version": "^4.5.0"},
            "sqlalchemy": {"package": "sqlalchemy", "version": "^2.0.19"},
            "sqlmodel": {"package": "sqlmodel", "version": "^0.0.8"},
            # Authentication
            "jwt": {"package": "pyjwt", "version": "^2.8.0"},
            "oauth2": {"package": "authlib", "version": "^1.2.1"},
            # Data processing
            "pandas": {"package": "pandas", "version": "^2.0.3"},
            "numpy": {"package": "numpy", "version": "^1.25.2"},
            "matplotlib": {"package": "matplotlib", "version": "^3.7.2"},
            # CLI tools
            "typer": {"package": "typer", "version": "^0.9.0"},
            "rich": {"package": "rich", "version": "^13.4.2"},
            "click": {"package": "click", "version": "^8.1.6"},
            # AI/ML
            "openai": {"package": "openai", "version": "^1.1.1"},
            "tensorflow": {"package": "tensorflow", "version": "^2.13.0"},
            "pytorch": {"package": "torch", "version": "^2.0.1"},
            "scikit-learn": {"package": "scikit-learn", "version": "^1.3.0"},
            # Frontend
            "vue.js": {"is_frontend": True},
            "react": {"is_frontend": True},
            "angular": {"is_frontend": True},
        }

        # Map the AI-recommended technologies to actual packages
        for tech_name in recommended_techs:
            # Create a normalized key for lookups
            tech_key = (
                tech_name.lower().replace(" ", "").replace("-", "").replace(".", "")
            )

            # Try to match with known technology mappings
            if tech_key in tech_mapping:
                tech_info = tech_mapping[tech_key]

                # Skip frontend technologies that don't need Python packages
                if tech_info.get("is_frontend", False):
                    continue

                # Add the package
                package_info = f"{tech_info['package']} = \"{tech_info['version']}\""
                if package_info not in dependencies:
                    dependencies.append(package_info)

                # Add any required dependencies
                for req in tech_info.get("requires", []):
                    if req not in dependencies:
                        dependencies.append(req)

                # Add suggested dependencies
                for suggestion in tech_info.get("suggests", []):
                    if suggestion in tech_mapping:
                        suggestion_info = tech_mapping[suggestion]
                        package_info = f"{suggestion_info['package']} = \"{suggestion_info['version']}\""
                        if package_info not in dependencies:
                            dependencies.append(package_info)
            else:
                # Handle custom/unknown technologies with best-effort matching
                # Try to infer package names based on common patterns
                # Mapping from common custom technologies to Python packages
                custom_tech_map = {
                    "nextjs": {"is_frontend": True},  # Next.js is a frontend framework
                    "nuxtjs": {"is_frontend": True},  # Nuxt.js is a frontend framework
                    "sveltekit": {
                        "is_frontend": True
                    },  # SvelteKit is a frontend framework
                    "magiclink": {
                        "package": "magic-link",
                        "version": "^0.3.4",
                    },  # Magic Link for passwordless auth
                    "magiclinkauthentication": {
                        "package": "magic-link",
                        "version": "^0.3.4",
                    },
                    "cloudflare": {
                        "is_deployment": True
                    },  # Cloudflare is a deployment solution
                    "cloudflaretunnels": {"is_deployment": True},
                    "vercel": {"is_deployment": True},
                    "netlify": {"is_deployment": True},
                    "supabase": {"package": "supabase", "version": "^1.0.3"},
                    "firebaseauth": {"package": "firebase-admin", "version": "^11.0.0"},
                    "pinecone": {"package": "pinecone-client", "version": "^2.2.1"},
                }

                # Try to find a match in the custom tech map
                custom_match = None
                for custom_key, custom_info in custom_tech_map.items():
                    if custom_key in tech_key or tech_key in custom_key:
                        custom_match = custom_info
                        break

                # If we found a match and it's a Python package, add it
                if (
                    custom_match
                    and "package" in custom_match
                    and not custom_match.get("is_frontend", False)
                    and not custom_match.get("is_deployment", False)
                ):
                    package_info = (
                        f"{custom_match['package']} = \"{custom_match['version']}\""
                    )
                    if package_info not in dependencies:
                        dependencies.append(package_info)

        # Add default dependencies based on project type if no matching technologies were found
        if not dependencies:
            if project_type == "web":
                dependencies.append('flask = "^2.3.2"')
            elif project_type == "cli":
                dependencies.append('typer = "^0.9.0"')
                dependencies.append('rich = "^13.4.2"')
            elif project_type == "ai":
                dependencies.append('openai = "^1.1.1"')
                dependencies.append('numpy = "^1.25.2"')
                dependencies.append('pandas = "^2.0.3"')
            elif project_type == "data":
                dependencies.append('pandas = "^2.0.3"')
                dependencies.append('numpy = "^1.25.2"')
                dependencies.append('matplotlib = "^3.7.2"')

        # Create pyproject.toml content
        pyproject_content = f"""
[tool.poetry]
name = "{package_name}"
version = "0.1.0"
description = "{kwargs.get('description', 'A Python project.')}"
authors = ["{kwargs.get('author_name', 'Your Name')} <{kwargs.get('author_email', 'your.email@example.com')}>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^{kwargs.get('python_version', '3.9')}"
"""

        # Add dependencies
        for dep in dependencies:
            pyproject_content += f"{dep}\n"

        # Add dev dependencies
        pyproject_content += "\n[tool.poetry.group.dev.dependencies]\n"
        for dep in dev_dependencies:
            pyproject_content += f"{dep}\n"

        # Add CLI entry point if needed
        if project_type == "cli":
            pyproject_content += f"""
[tool.poetry.scripts]
{package_name} = "{package_name}.cli:main"
"""

        # Add build system
        pyproject_content += """
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""

        # Add pyproject.toml to base files
        base_files["pyproject.toml"] = pyproject_content

        # Write base files
        for filename, content in base_files.items():
            with open(os.path.join(project_dir, filename), "w") as file:
                file.write(content)

        # Create src directory with project package
        src_dir = os.path.join(project_dir, "src")
        package_dir = os.path.join(src_dir, package_name)
        os.makedirs(package_dir, exist_ok=True)

        # Create __init__.py
        with open(os.path.join(package_dir, "__init__.py"), "w") as file:
            file.write(
                f'"""Top-level package for {project_name}."""\n\n__version__ = "0.1.0"\n'
            )

        # Create tests directory
        tests_dir = os.path.join(project_dir, "tests")
        os.makedirs(tests_dir, exist_ok=True)
        with open(os.path.join(tests_dir, "__init__.py"), "w") as file:
            file.write('"""Test package for the project."""\n')

        # Add AI integration if requested
        if with_ai:
            ai_docs_dir = os.path.join(project_dir, "ai-docs")
            os.makedirs(ai_docs_dir, exist_ok=True)

            # Create claude file
            with open(os.path.join(project_dir, "CLAUDE.md"), "w") as file:
                file.write(
                    f"""# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

{project_name} - {kwargs.get('description', 'A Python project.')}.

## Development Commands

### Installation

```bash
# Install with Poetry (recommended)
poetry install

# Or with pip in a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -e .
```

### Running the Application

```bash
# With Poetry
poetry run python -m {package_name}

# Or directly
python -m {package_name}
```

### Code Quality Checks

```bash
# Type checking with mypy
poetry run mypy src/{package_name}

# Format code with Black
poetry run black src/{package_name}

# Linting with pylint
poetry run pylint src/{package_name}
```

### Testing

```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=src/{package_name}
```
"""
                )

            # Create convo.md in ai-docs
            with open(os.path.join(ai_docs_dir, "convo.md"), "w") as file:
                file.write(
                    f"# {project_name} Project\n\nThis file contains the conversation history with AI assistants for this project.\n"
                )

        # Create additional project-specific files based on project_type and tech stack
        if project_type == "web":
            # Create web-specific directories
            templates_dir = os.path.join(package_dir, "templates")
            static_dir = os.path.join(package_dir, "static")
            os.makedirs(templates_dir, exist_ok=True)
            os.makedirs(static_dir, exist_ok=True)

            # Determine which web framework to use based on recommended technologies
            framework_templates = {
                "fastapi": f'''"""FastAPI application for {project_name}."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="{project_name}", description="{kwargs.get('description', 'A FastAPI application.')}")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint."""
    return {{"message": "Welcome to {project_name} API"}}

def start():
    """Start the application with uvicorn."""
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start()
''',
                "django": f'''"""Django application for {project_name}."""

from django.apps import AppConfig


class {project_name.replace("-", "_").title()}Config(AppConfig):
    """Django app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "{package_name}"
''',
                "flask": f'''"""Web application for {project_name}."""

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html', title="{project_name}")


@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html', title="About {project_name}")


def create_app():
    """Create and configure the Flask app."""
    # Configuration can be added here
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
''',
            }

            # Find the recommended web framework
            framework = None
            frontend_framework = None

            # Check for backend framework
            for tech_name in recommended_techs:
                tech_key = (
                    tech_name.lower().replace(" ", "").replace("-", "").replace(".", "")
                )
                if tech_key in ["fastapi", "django", "flask"]:
                    framework = tech_key
                    break

            # Check for frontend framework
            for tech_name in recommended_techs:
                tech_key = (
                    tech_name.lower().replace(" ", "").replace("-", "").replace(".", "")
                )
                if tech_key in [
                    "nextjs",
                    "react",
                    "vuejs",
                    "vue",
                    "angular",
                    "nuxtjs",
                    "sveltekit",
                ]:
                    frontend_framework = tech_key
                    break

            # Default to Flask if no framework found
            if not framework:
                framework = "flask"

            # Log the selected frameworks
            print(f"Selected backend framework: {framework}")
            if frontend_framework:
                print(f"Selected frontend framework: {frontend_framework}")

            # Create the app.py file with the appropriate template
            app_file = os.path.join(package_dir, "app.py")
            with open(app_file, "w", encoding="utf-8") as file:
                file.write(framework_templates[framework])

            # Create a simple HTML template
            index_template = os.path.join(templates_dir, "index.html")
            with open(index_template, "w", encoding="utf-8") as file:
                file.write(
                    f"""<!DOCTYPE html>
<html>
<head>
    <title>{{title}}</title>
    <link rel="stylesheet" href="{{url_for('static', filename='css/style.css')}}">
</head>
<body>
    <h1>Welcome to {project_name}</h1>
    <p>{kwargs.get('description', 'A web application.')}</p>
    
    <script src="{{url_for('static', filename='js/main.js')}}"></script>
</body>
</html>
"""
                )

            # Create CSS and JS directories
            css_dir = os.path.join(static_dir, "css")
            js_dir = os.path.join(static_dir, "js")
            os.makedirs(css_dir, exist_ok=True)
            os.makedirs(js_dir, exist_ok=True)

            # Create basic CSS file
            with open(
                os.path.join(css_dir, "style.css"), "w", encoding="utf-8"
            ) as file:
                file.write(
                    """body {font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    line-height: 1.6;}

h1 {color: #333;}
"""
                )

            # Create basic JS file
            with open(os.path.join(js_dir, "main.js"), "w", encoding="utf-8") as file:
                file.write(
                    """document.addEventListener('DOMContentLoaded', function() {console.log('Application loaded');});
"""
                )

        elif project_type == "cli":
            # Create CLI module
            cli_file = os.path.join(package_dir, "cli.py")
            with open(cli_file, "w", encoding="utf-8") as file:
                file.write(
                    f'''"""Command-line interface for {project_name}."""

import sys
import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(help="{kwargs.get('description', 'A Python CLI application.')}")
console = Console()

@app.command()
def hello(name: str = typer.Option("World", help="Name to greet")):
    """Say hello to someone."""
    panel = Panel(f"Hello, {{name}}!", title="{project_name}")
    console.print(panel)
    return 0

def main():
    """Main entry point for the CLI."""
    return app()

if __name__ == "__main__":
    sys.exit(main())
'''
                )

        elif project_type == "ai":
            # Create AI-specific directories
            models_dir = os.path.join(package_dir, "models")
            prompts_dir = os.path.join(package_dir, "prompts")
            data_dir = os.path.join(package_dir, "data")
            os.makedirs(models_dir, exist_ok=True)
            os.makedirs(prompts_dir, exist_ok=True)
            os.makedirs(data_dir, exist_ok=True)

            # Create AI module
            ai_file = os.path.join(package_dir, "ai.py")
            with open(ai_file, "w", encoding="utf-8") as file:
                file.write(
                    f'''"""AI integration for {project_name}."""

import os
from typing import Dict, List, Any, Tuple

# Check if OpenAI is available
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class AIModel:
    """Base class for AI models."""
    
    def __init__(self, api_key: str = None):
        """Initialize the AI model."""
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        
    def generate(self, prompt: str) -> str:
        """Generate a response from the AI model."""
        raise NotImplementedError("Subclasses must implement this method")
        
class OpenAIModel(AIModel):
    """OpenAI API integration."""
    
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        """Initialize the OpenAI model."""
        super().__init__(api_key)
        self.model = model
        
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package is not installed. Run 'pip install openai'")
            
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
            
        # Initialize OpenAI client
        openai.api_key = self.api_key
        
    def generate(self, prompt: str) -> str:
        """Generate a response from the OpenAI model."""
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1000,
            )
            return response.choices[0].message.content
        except Exception as error:
            return f"Error: {str(error)}"
'''
                )

        elif project_type == "data":
            # Create data-specific directories
            data_dir = os.path.join(package_dir, "data")
            notebooks_dir = os.path.join(project_dir, "notebooks")
            os.makedirs(data_dir, exist_ok=True)
            os.makedirs(notebooks_dir, exist_ok=True)

            # Create data analysis module
            data_file = os.path.join(package_dir, "analysis.py")
            with open(data_file, "w", encoding="utf-8") as file:
                file.write(
                    f'''"""Data analysis module for {project_name}."""

import os
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Any, Tuple

def load_data(file_path: str) -> pd.DataFrame:
    """Load data from a file into a pandas DataFrame."""
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension.lower() == '.csv':
        return pd.read_csv(file_path)
    elif file_extension.lower() in ['.xls', '.xlsx']:
        return pd.read_excel(file_path)
    elif file_extension.lower() == '.json':
        return pd.read_json(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")

def analyze_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Perform basic data analysis."""
    results = {"shape": df.shape,
        "columns": df.columns.tolist(),
        "summary": df.describe().to_dict(),
        "missing_values": df.isnull().sum().to_dict(),}
    return results

def visualize_data(df: pd.DataFrame, column_name: str, output_path: str = None) -> None:
    """Create a simple visualization for a column."""
    plt.figure(figsize=(10, 6))
    
    if pd.api.types.is_numeric_dtype(df[column_name]):
        df[column_name].hist()
        plt.title(f"Histogram of {column_name}")
    else:
        df[column_name].value_counts().plot(kind=\'bar\')
        plt.title(f"Value counts of {column_name}")
        
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path)
    else:
        plt.show()
'''
                )

            # Create a simple Jupyter notebook
            notebook_file = os.path.join(notebooks_dir, "data_exploration.ipynb")
            with open(notebook_file, "w", encoding="utf-8") as file:
                file.write(
                    """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Data Exploration Notebook"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# Set up plot styling\n",
    "plt.style.use('ggplot')\n",
    "sns.set_theme()\n",
    "%matplotlib inline"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Loading Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# TODO: Load your data\n",
    "# df = pd.read_csv('data/your_data.csv')\n",
    "# df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Data Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# TODO: Analyze your data\n",
    "# df.describe()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Data Visualization"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# TODO: Visualize your data\n",
    "# plt.figure(figsize=(10, 6))\n",
    "# sns.histplot(df['column_name'])\n",
    "# plt.title('Histogram of Column')\n",
    "# plt.show()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {"display_name": "Python 3",
   "language": "python",
   "name": "python3"},
  "language_info": {
   "codemirror_mode": {"name": "ipython",
    "version": 3},
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
"""
                )

        # Create utils directory in the project package
        utils_dir = os.path.join(package_dir, "utils")
        os.makedirs(utils_dir, exist_ok=True)
        with open(os.path.join(utils_dir, "__init__.py"), "w") as file:
            file.write('"""Utility functions for the project."""\n')

        return True, f"Project structure created at {project_dir}"

    except Exception as e:
        return False, f"Failed to create project structure: {str(e)}"


def setup_virtual_environment(project_dir: str) -> Tuple[bool, str]:
    """
    Set up a virtual environment using Poetry.

    Args:
        project_dir: The project directory where the dependencies should be installed

    Returns:
        Tuple containing success status and message
    """
    try:
        # Check if Poetry is installed
        if not shutil.which("poetry"):
            return False, "Poetry is not installed. Please install Poetry first."

        # Configure Poetry to create virtual environment in the project directory
        subprocess.run(
            ["poetry", "config", "virtualenvs.in-project", "true", "--local"],
            cwd=project_dir,
            check=True,
        )

        # Install dependencies using Poetry
        subprocess.run(["poetry", "install"], cwd=project_dir, check=True)

        return True, "Poetry virtual environment created and dependencies installed"
    except Exception as e:
        return False, f"Failed to set up Poetry virtual environment: {str(e)}"


def initialize_git_repo(
    project_dir: str,
    project_name: str,
    github_username: str = "",
    gitlab_username: str = "",
    with_github_config: bool = False,
    project_description: str = "",
    project_type: str = "",
    tech_stack: dict = None,
) -> Tuple[bool, str]:
    """
    Initialize a Git repository and set up GitHub and GitLab remotes.

    This function now handles custom deployment configurations based on tech_stack.
    For example, if Cloudflare Tunnels is selected, it will add related configuration files.

    Args:
        project_dir: The project directory
        project_name: Name of the project
        github_username: GitHub username for remote setup
        gitlab_username: GitLab username for remote setup
        with_github_config: Whether to create GitHub config files (.github dir)
        project_description: Description of the project
        project_type: Type of the project (web, cli, etc.)
        tech_stack: Dictionary containing AI-recommended technology stack

    Returns:
        Tuple containing success status and message
    """
    try:
        # Check if git is installed
        if not shutil.which("git"):
            return False, "Git is not installed or not in PATH"

        # Initialize git repository
        subprocess.run(["git", "init"], cwd=project_dir, check=True)

        # Create GitHub configuration files if requested
        if with_github_config:
            create_github_config_files(
                project_dir, project_name, project_description, project_type, tech_stack
            )

        # Create comprehensive .gitignore
        create_comprehensive_gitignore(project_dir, project_type)

        # Handle custom deployment configurations based on tech stack
        if tech_stack and "categories" in tech_stack:
            deployment_tech = None

            # Find the selected deployment technology
            for category in tech_stack["categories"]:
                if category["name"] == "Deployment":
                    for option in category["options"]:
                        if option.get("recommended", False):
                            deployment_tech = option["name"]
                            break

            # If a custom deployment is found, create its configuration
            if deployment_tech:
                normalized_tech = (
                    deployment_tech.lower()
                    .replace(" ", "")
                    .replace("-", "")
                    .replace(".", "")
                )

                # Handle Cloudflare Tunnels
                if "cloudflare" in normalized_tech and "tunnel" in normalized_tech:
                    create_cloudflare_tunnels_config(project_dir, project_name)
                # Handle Vercel deployment
                elif "vercel" in normalized_tech:
                    create_vercel_config(project_dir, project_name)
                # Handle Netlify deployment
                elif "netlify" in normalized_tech:
                    create_netlify_config(project_dir, project_name)

        # Add all files to git
        subprocess.run(["git", "add", "."], cwd=project_dir, check=True)

        # Create initial commit
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"], cwd=project_dir, check=True
        )

        # Set up remotes if usernames are provided
        if github_username:
            repo_name = project_name.replace(" ", "-").lower()
            github_url = f"https://github.com/{github_username}/{repo_name}.git"
            subprocess.run(
                ["git", "remote", "add", "github", github_url],
                cwd=project_dir,
                check=True,
            )

        if gitlab_username:
            repo_name = project_name.replace(" ", "-").lower()
            gitlab_url = f"https://gitlab.com/{gitlab_username}/{repo_name}.git"
            subprocess.run(
                ["git", "remote", "add", "gitlab", gitlab_url],
                cwd=project_dir,
                check=True,
            )

        return True, "Git repository initialized with remotes"
    except subprocess.CalledProcessError as e:
        return False, f"Git command failed: {str(e)}"
    except Exception as e:
        return False, f"Failed to set up Git repository: {str(e)}"


def create_comprehensive_gitignore(project_dir: str, project_type: str) -> None:
    """
    Create a comprehensive .gitignore file for the project.

    Args:
        project_dir: The project directory
        project_type: Type of the project (web, cli, etc.)
    """
    gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# VS Code
.vscode/*
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
.vscode/mcp-secrets.json

# VS Code Settings with Secrets
.vscode/settings.json

# Logs
*.log

# Documentation build
docs/_build/
docs/build/

# Temporary and backup files
*.bak
*.tmp
*_report.txt

# Coverage reports
.coverage
htmlcov/

# IDE/Editor specific
*.code-workspace
.idea/
"""

    # Add project-type specific entries
    if project_type == "web":
        gitignore_content += """
# Web specific
node_modules/
package-lock.json
yarn.lock
static/dist/
.env.local
.env.development.local
.env.test.local
.env.production.local
"""
    elif project_type == "data":
        gitignore_content += """
# Data science specific
.ipynb_checkpoints/
*.csv
*.xlsx
*.parquet
data/raw/
data/processed/
data/external/
"""

    # Write the comprehensive .gitignore file
    with open(os.path.join(project_dir, ".gitignore"), "w", encoding="utf-8") as file:
        file.write(gitignore_content)


def create_cloudflare_tunnels_config(project_dir: str, project_name: str) -> None:
    """
    Create configuration files for Cloudflare Tunnels deployment.

    Args:
        project_dir: The project directory
        project_name: Name of the project
    """
    # Create .cloudflare directory
    cloudflare_dir = os.path.join(project_dir, ".cloudflare")
    os.makedirs(cloudflare_dir, exist_ok=True)

    # Create sample tunnel configuration
    config_content = f"""
# This is a sample configuration for Cloudflare Tunnels
# You'll need to update it with your specific tunnel details

tunnel: {project_name.replace(" ", "-").lower()}-tunnel
credentials-file: /path/to/your/credentials/file.json

ingress:
  - hostname: mycv.michaelnewham.me
    service: http://localhost:8000
  - hostname: jobs.michaelnewham.me
    service: http://localhost:8000/jobs
  - service: http_status:404
"""

    with open(
        os.path.join(cloudflare_dir, "config.yml"), "w", encoding="utf-8"
    ) as file:
        file.write(config_content)

    # Create README file with instructions
    readme_content = f"""# Cloudflare Tunnels Configuration

This directory contains configuration for deploying {project_name} using Cloudflare Tunnels.

## Setup Instructions

1. Install the Cloudflare Tunnel client (cloudflared):
   ```
   # On Linux
   curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
   sudo dpkg -i cloudflared.deb
   
   # On MacOS
   brew install cloudflare/cloudflare/cloudflared
   ```

2. Authenticate with Cloudflare:
   ```
   cloudflared tunnel login
   ```

3. Create a new tunnel:
   ```
   cloudflared tunnel create {project_name.replace(" ", "-").lower()}-tunnel
   ```

4. Update the `config.yml` file with your specific tunnel ID and hostnames

5. Start the tunnel:
   ```
   cloudflared tunnel run {project_name.replace(" ", "-").lower()}-tunnel
   ```

For more information, see the [Cloudflare Tunnels documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/).
"""

    with open(os.path.join(cloudflare_dir, "README.md"), "w", encoding="utf-8") as file:
        file.write(readme_content)


def create_vercel_config(project_dir: str, project_name: str) -> None:
    """
    Create configuration files for Vercel deployment.

    Args:
        project_dir: The project directory
        project_name: Name of the project
    """
    # Create vercel.json file
    vercel_config = {
        "version": 2,
        "name": project_name.replace(" ", "-").lower(),
        "builds": [
            {"src": "api/*.py", "use": "@vercel/python"},
            {"src": "public/**", "use": "@vercel/static"},
        ],
        "routes": [
            {"src": "/api/(.*)", "dest": "/api/$1"},
            {"src": "/(.*)", "dest": "/public/$1"},
        ],
    }

    import json

    with open(os.path.join(project_dir, "vercel.json"), "w", encoding="utf-8") as file:
        json.dump(vercel_config, file, indent=2)

    # Create an api directory with a sample file
    api_dir = os.path.join(project_dir, "api")
    os.makedirs(api_dir, exist_ok=True)

    with open(os.path.join(api_dir, "index.py"), "w", encoding="utf-8") as file:
        file.write(
            f"""from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(f'Hello from {project_name}!'.encode())
        return
"""
        )

    # Create a public directory for static files
    public_dir = os.path.join(project_dir, "public")
    os.makedirs(public_dir, exist_ok=True)

    with open(os.path.join(public_dir, "index.html"), "w", encoding="utf-8") as file:
        file.write(
            f"""<!DOCTYPE html>
<html>
<head>
    <title>{project_name}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <h1>Welcome to {project_name}</h1>
    <p>This is a static page served by Vercel.</p>
</body>
</html>
"""
        )


def create_netlify_config(project_dir: str, project_name: str) -> None:
    """
    Create configuration files for Netlify deployment.

    Args:
        project_dir: The project directory
        project_name: Name of the project
    """
    # Create netlify.toml file
    netlify_config = """[build]
  command = "pip install -r requirements.txt"
  publish = "public"
  functions = "netlify/functions"

[dev]
  command = "npm run dev"
  port = 8888
  publish = "public"
  framework = "#custom"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200
"""

    with open(os.path.join(project_dir, "netlify.toml"), "w", encoding="utf-8") as file:
        file.write(netlify_config)

    # Create Netlify functions directory
    functions_dir = os.path.join(project_dir, "netlify", "functions")
    os.makedirs(functions_dir, exist_ok=True)

    with open(os.path.join(functions_dir, "hello.py"), "w", encoding="utf-8") as file:
        file.write(
            f"""def handler(event, context):
    return {{
        "statusCode": 200,
        "body": f"Hello from {project_name}!"
    }}
"""
        )

    # Create a public directory for static files
    public_dir = os.path.join(project_dir, "public")
    os.makedirs(public_dir, exist_ok=True)

    with open(os.path.join(public_dir, "index.html"), "w", encoding="utf-8") as file:
        file.write(
            f"""<!DOCTYPE html>
<html>
<head>
    <title>{project_name}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <h1>Welcome to {project_name}</h1>
    <p>This is a static page served by Netlify.</p>
</body>
</html>
"""
        )


def create_github_config_files(
    project_dir: str,
    project_name: str,
    project_description: str,
    project_type: str,
    tech_stack: dict = None,
) -> None:
    """
    Create GitHub configuration files for Copilot and other tools.

    Args:
        project_dir: The project directory
        project_name: Name of the project
        project_description: Description of the project
        project_type: Type of the project (web, cli, etc.)
        tech_stack: Dictionary containing AI-recommended technology stack
    """
    tech_stack = tech_stack or {}

    # Extract technology information
    tech_list = []
    if tech_stack and "categories" in tech_stack:
        for category in tech_stack["categories"]:
            for option in category["options"]:
                if option.get("recommended", False):
                    tech_list.append(
                        {
                            "category": category["name"],
                            "name": option["name"],
                            "description": option["description"],
                        }
                    )

    # Create .github directory
    github_dir = os.path.join(project_dir, ".github")
    instructions_dir = os.path.join(github_dir, "instructions")
    prompts_dir = os.path.join(github_dir, "prompts")

    os.makedirs(github_dir, exist_ok=True)
    os.makedirs(instructions_dir, exist_ok=True)
    os.makedirs(prompts_dir, exist_ok=True)

    # Create main README.md file
    with open(os.path.join(github_dir, "README.md"), "w", encoding="utf-8") as file:
        file.write(
            f"""# GitHub Copilot Configuration

This directory contains configuration files for GitHub Copilot to understand our project's coding standards and best practices.

## Structure

- `copilot-instructions.md` - Main instructions file for the entire workspace
- `/instructions/` - Directory containing specific instruction files for different file types or tasks
- `/prompts/` - Directory containing reusable prompt files for common development tasks

## Instruction Files

These files tell GitHub Copilot about our coding standards, project structure, and best practices:

- `copilot-instructions.md` - Main project-wide instructions
- `instructions/python_style.instructions.md` - Python code style guidelines
- `instructions/testing.instructions.md` - Testing standards and practices
{'- `instructions/cli.instructions.md` - CLI development guidelines' if project_type == 'cli' else ''}
{'- `instructions/web.instructions.md` - Web development guidelines' if project_type == 'web' else ''}
{'- `instructions/data.instructions.md` - Data analysis guidelines' if project_type == 'data' else ''}
{'- `instructions/ai.instructions.md` - AI/ML development guidelines' if project_type == 'ai' else ''}

## Prompt Files

These files provide reusable templates for common development tasks:

- `prompts/generate_tests.prompt.md` - Generate comprehensive test files
- `prompts/add_feature.prompt.md` - Add new features to the project
- `prompts/code_review.prompt.md` - Review and refactor code

## Usage

### Using Instruction Files

Instruction files are automatically applied to relevant files based on the `applyTo` pattern in their front matter. The main `copilot-instructions.md` file is applied to all requests when enabled in settings.

### Using Prompt Files

To use a prompt file:

1. In the Chat view, type `/` followed by the prompt file name
2. Or use the Command Palette (Ctrl+Shift+P) and select "Chat: Run Prompt"
3. Or open the prompt file and click the play button in the editor title

### Configuration

The VS Code settings that enable these features are in `.vscode/settings.json`:

```json
{{"github.copilot.chat.codeGeneration.useInstructionFiles": true,
  "chat.promptFiles": true,
  "chat.instructionsFilesLocations": [".github/instructions"],
  "chat.promptFilesLocations": [".github/prompts"]}}
```
"""
        )

    # Create main copilot-instructions.md file
    with open(
        os.path.join(github_dir, "copilot-instructions.md"), "w", encoding="utf-8"
    ) as file:
        # Extract all selected technologies
        tech_stack_str = "\n".join(
            [f"- **{tech['category']}**: {tech['name']}" for tech in tech_list]
        )

        # Determine the primary languages based on tech stack and project type
        primary_languages = ["Python"]

        # Check if project includes web frontend technologies
        has_frontend = False
        frontend_techs = []
        for tech in tech_list:
            if tech["name"].lower() in ["vue.js", "react", "angular"]:
                has_frontend = True
                frontend_techs.append(tech["name"])
                if "vue.js" in tech["name"].lower():
                    primary_languages.append("JavaScript/Vue.js")
                elif "react" in tech["name"].lower():
                    primary_languages.append("JavaScript/React")
                elif "angular" in tech["name"].lower():
                    primary_languages.append("TypeScript/Angular")

        # Format primary languages string
        primary_languages_str = ", ".join(primary_languages)

        # Generate custom coding standards based on technologies
        coding_standards = []

        # Always include Python standards
        coding_standards.append(
            """### Python Style
- Follow PEP 8 conventions
- Use 4 spaces for indentation
- Maximum line length of 88 characters (Black default)
- Use snake_case for variables, functions, methods, and modules
- Use PascalCase for class names
- Use ALL_UPPERCASE for constants
- Include type hints for all function parameters and return values"""
        )

        # Add frontend standards if applicable
        if has_frontend:
            if "vue.js" in str(frontend_techs).lower():
                coding_standards.append(
                    """### Vue.js Style
- Follow Vue.js Style Guide (Priority A rules)
- Use kebab-case for component names in templates
- Use PascalCase for component names in JS/TS
- Use composition API for new components
- Organize components with clear separation of concerns"""
                )
            elif "react" in str(frontend_techs).lower():
                coding_standards.append(
                    """### React Style
- Follow React best practices
- Use functional components with hooks
- Use PascalCase for component names
- Keep components focused on a single responsibility
- Use prop-types or TypeScript for props validation"""
                )
            elif "angular" in str(frontend_techs).lower():
                coding_standards.append(
                    """### Angular Style
- Follow Angular style guide
- Use kebab-case for component selectors
- Use PascalCase for component names
- Follow OnPush change detection when possible
- Implement proper module organization"""
                )

        # Add documentation standards
        coding_standards.append(
            """### Documentation
- Every module, class, and function should have a docstring
- Follow Google-style docstrings format for Python
- Include examples in docstrings for public APIs"""
        )

        # Add database specific standards if applicable
        for tech in tech_list:
            if tech["category"] == "Database":
                if "postgresql" in tech["name"].lower():
                    coding_standards.append(
                        """### Database Practices
- Use SQLAlchemy for database operations
- Write migrations for schema changes
- Follow normalization principles for database design
- Use connection pooling for efficiency"""
                    )
                elif "mongodb" in tech["name"].lower():
                    coding_standards.append(
                        """### Database Practices
- Design document schemas with appropriate validation
- Use indexes for frequently queried fields
- Implement proper error handling for database operations
- Consider data aggregation pipelines for complex queries"""
                    )

        # Add API specific standards for web projects
        if project_type == "web":
            coding_standards.append(
                """### API Design
- Follow RESTful principles for endpoints
- Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- Return consistent error responses
- Implement proper input validation
- Document all endpoints comprehensively"""
            )

        # Always include testing, error handling and imports standards
        coding_standards.append(
            """### Testing
- All code should have corresponding unit tests
- Use pytest fixtures for test setup
- Target high test coverage (aim for 80%+)
- Tests should be isolated and not depend on external resources"""
        )

        coding_standards.append(
            """### Error Handling
- Use explicit exception handling with specific exception types
- Log errors with appropriate context
- Provide meaningful error messages to users"""
        )

        coding_standards.append(
            """### Imports
- Group imports in the following order:
  1. Standard library imports
  2. Related third-party imports
  3. Local application/library specific imports
- Sort imports alphabetically within each group
- Use absolute imports rather than relative imports"""
        )

        # Join all coding standards
        coding_standards_str = "\n\n".join(coding_standards)

        # Define project structure based on project type
        if project_type == "web":
            project_structure = """## Project Structure
- Use the standard Poetry project structure for Python components
- Keep backend modules focused and single-purpose
- Organize API endpoints logically
- Separate business logic from route handlers
- Place reusable utilities in the utils module
- For frontend code, follow component-based architecture
- Organize tests to mirror the structure of the source code"""
        elif project_type == "cli":
            project_structure = """## Project Structure
- Use the standard Poetry project structure
- Separate CLI interface from business logic
- Organize commands in a logical hierarchy
- Place reusable utilities in the utils module
- Implement proper command-line argument parsing
- Organize tests to mirror the structure of the source code"""
        elif project_type == "data":
            project_structure = """## Project Structure
- Use the standard Poetry project structure
- Organize data processing pipelines clearly
- Separate data acquisition, preprocessing, and analysis
- Store data models in dedicated modules
- Keep visualization code separate from data processing
- Organize tests to mirror the structure of the source code"""
        elif project_type == "ai":
            project_structure = """## Project Structure
- Use the standard Poetry project structure
- Separate model definition, training, and inference
- Store pre-trained models in a dedicated directory
- Organize datasets and data processing pipelines clearly
- Keep evaluation metrics and visualization separate
- Organize tests to mirror the structure of the source code"""
        else:
            project_structure = """## Project Structure
- Use the standard Poetry project structure
- Keep modules focused and single-purpose
- Place reusable utilities in the utils module
- Configuration should be handled through environment variables or config files
- Organize tests to mirror the structure of the source code"""

        # Write the file with dynamically generated content
        file.write(
            f"""# {project_name} - Custom Instructions for GitHub Copilot

## Project Overview
{project_description}

## Tech Stack
- **Primary Languages**: {primary_languages_str}
{tech_stack_str if tech_list else ""}
- **Package Management**: Poetry
- **Testing Framework**: pytest
- **Code Quality**: Black, pylint, mypy

## Coding Standards

{coding_standards_str}

{project_structure}
"""
        )

    # Create Python style instructions
    with open(
        os.path.join(instructions_dir, "python_style.instructions.md"),
        "w",
        encoding="utf-8",
    ) as file:
        file.write(
            """---
applyTo: "**/*.py"
---
# Python Code Style Guidelines

## Formatting
- Follow PEP 8 conventions strictly
- Format code with Black using 88-character line length
- Use 4 spaces for indentation (not tabs)
- Use single quotes for strings unless the string contains single quotes
- Add a blank line at the end of each file
- Use trailing commas in multi-line data structures

## Variables and Functions
- Use descriptive names that convey intent
- Use snake_case for all variable and function names
- Use ALL_CAPS for constants and module-level variables that shouldn't change
- Avoid abbreviations unless they are standard in the domain

## Type Annotations
- Always include type hints for:
  - Function parameters
  - Return values
  - Class attributes when their type isn't obvious
- Use typing module for complex types (List, Dict, Optional, Union, etc.)
- Use collections.abc for container types in Python 3.9+

## Comments and Docstrings
- Every public function, class, and module should have a docstring
- Follow Google-style docstring format consistently
- Include Args, Returns, Raises, and Examples sections as appropriate
- Comment complex logic or non-obvious decisions, not obvious code

## Imports
- Organize imports in three groups:
  1. Standard library imports
  2. Third-party imports
  3. Local application/library imports
- Sort each group alphabetically
- One import per line
- Use absolute imports, not relative imports

## Best Practices
- Prefer dict.get() with a default value over checking if a key exists
- Use context managers (with statements) for resource management
- Use list/dict comprehensions for simple transformations instead of loops
- For complex list processing operations, prefer generator expressions to save memory
"""
        )

    # Create testing instructions
    with open(
        os.path.join(instructions_dir, "testing.instructions.md"), "w", encoding="utf-8"
    ) as file:
        file.write(
            """---
applyTo: "**/test_*.py"
---
# Testing Guidelines

## Test Structure
- Follow the Arrange-Act-Assert pattern for test organization
- Keep tests small and focused on a single functionality
- Use descriptive test names that convey what's being tested
- Group related tests in test classes when appropriate
- Use pytest fixtures for common setup and teardown

## Test Coverage
- Aim for 80%+ test coverage overall
- Test success paths thoroughly
- Test edge cases and error conditions
- Test boundary conditions and input validation
- Test any configuration or environment dependencies

## Best Practices
- Use parameterized tests for testing similar functionality with different inputs
- Mock external dependencies to ensure tests run in isolation
- Use appropriate assertions for the type of comparison being made
- Keep tests deterministic (no randomness or time-dependent behavior)
- Avoid testing implementation details, focus on behavior

## Fixtures and Setup
- Use fixtures for reusable test setup
- Keep fixture scope as narrow as possible (function > class > module > session)
- Clean up resources in teardown even if tests fail
- Use setup/teardown methods consistently

## Naming Conventions
- Test files should be named `test_[module].py`
- Test classes should be named `Test[Class]`
- Test methods should be named `test_[functionality]_[condition]`
- Fixtures should have descriptive names indicating what they provide

## Test Documentation
- Include docstrings for test classes explaining what they test
- For complex test cases, include comments explaining the intent and setup
- Document any non-obvious test data or test configuration
"""
        )

    # Create CLI instructions if applicable
    if project_type == "cli":
        with open(
            os.path.join(instructions_dir, "cli.instructions.md"), "w", encoding="utf-8"
        ) as file:
            file.write(
                f"""---
applyTo: "**/{project_name.replace('-', '_').replace(' ', '_').lower()}/cli.py"
---
# CLI Development Guidelines

## Command Structure
- Use a consistent command structure: `{project_name.replace('-', '_').replace(' ', '_').lower()} [options] <command>`
- Group related options logically
- Provide sensible defaults for all options
- Support both short (-h) and long (--help) option forms

## User Experience
- Provide clear, concise help text for all commands and options
- Include examples in help text for common use cases
- Use color in terminal output to highlight important information
- Show progress for long-running operations

## Error Handling
- Provide clear error messages that explain both what went wrong and how to fix it
- Handle common errors gracefully (e.g., missing dependencies, invalid inputs)
- Use appropriate exit codes for different error types
- Log detailed error information for debugging

## Input Validation
- Validate all user inputs before processing
- Confirm destructive operations before proceeding
- Provide clear feedback on invalid inputs
- Support interactive prompts for required information

## Output
- Make output concise by default
- Provide a verbose mode for detailed output
- Format output for both human readability and potential machine parsing
- Include timestamps for long-running operations

## Configuration
- Support configuration via environment variables
- Support configuration via config files
- Document all configuration options
- Validate configuration values at startup

## Testing
- Test all CLI command paths
- Test with various combinations of options
- Test error handling and edge cases
- Include integration tests that run the CLI as a subprocess
"""
            )

    # Create web instructions if applicable
    if project_type == "web":
        # Determine which web framework is being used
        web_framework = None
        for tech in tech_list:
            if tech["name"].lower() == "fastapi":
                web_framework = "fastapi"
            elif tech["name"].lower() == "flask":
                web_framework = "flask"
            elif tech["name"].lower() == "django":
                web_framework = "django"

        # Create frontend instructions if needed
        has_frontend = False
        frontend_tech = None
        for tech in tech_list:
            if tech["name"].lower() in ["vue.js", "react", "angular"]:
                has_frontend = True
                frontend_tech = tech["name"].lower()

        # Create database instructions if needed
        database_tech = None
        for tech in tech_list:
            if tech["category"] == "Database":
                database_tech = tech["name"].lower()

        # Write web backend instructions file
        with open(
            os.path.join(instructions_dir, "web.instructions.md"), "w", encoding="utf-8"
        ) as file:
            # Determine appropriate apply pattern based on framework
            if web_framework == "fastapi":
                apply_pattern = "**/app.py"
            elif web_framework == "django":
                apply_pattern = "**/*.py"
            else:  # Default to Flask
                apply_pattern = "**/app.py"

            file.write(
                f"""---
applyTo: "{apply_pattern}"
---
# Web Development Guidelines

## {'FastAPI' if web_framework == 'fastapi' else 'Flask' if web_framework == 'flask' else 'Django' if web_framework == 'django' else 'Web Framework'} Best Practices
"""
            )

            # Add framework-specific advice
            if web_framework == "fastapi":
                file.write(
                    """- Use Pydantic models for request/response validation
- Leverage dependency injection for shared resources
- Use async functions for IO-bound operations
- Organize routers by resource or feature
- Use proper status codes and response models
- Implement comprehensive API documentation with OpenAPI
"""
                )
            elif web_framework == "django":
                file.write(
                    """- Follow Django's MTV (Model-Template-View) architecture
- Use class-based views for complex endpoints
- Leverage Django's ORM features appropriately
- Group related functionality into apps
- Use Django REST Framework for API endpoints
- Apply Django's security best practices
"""
                )
            else:  # Default to Flask
                file.write(
                    """- Use Blueprints to organize routes
- Implement proper application factories
- Use Flask extensions for common functionality
- Create reusable view functions or classes
- Structure templates with inheritance
- Leverage context processors for shared template data
"""
                )

            file.write(
                """
## API Design
- Follow RESTful principles for API endpoints
- Use consistent URL patterns and naming conventions
- Use appropriate HTTP methods for different operations (GET, POST, PUT, DELETE)
- Return appropriate HTTP status codes for different situations
- Implement proper error handling and validation

## Security
- Implement proper authentication and authorization
- Validate and sanitize all user inputs
- Protect against common web vulnerabilities (XSS, CSRF, SQL injection)
- Use HTTPS for all communications
- Follow the principle of least privilege for API access

## Performance
- Minimize database queries and optimize where necessary
- Use caching appropriately for frequently accessed data
- Implement pagination for large result sets
- Optimize static assets (minification, compression)
- Use asynchronous operations where appropriate

## Frontend Integration
- Ensure API responses are consistent and well-structured
- Document API endpoints for frontend developers
- Consider cross-origin concerns and implement CORS as needed
- Provide mechanisms for error handling in API responses
"""
            )

            # Add database-specific advice if available
            if database_tech:
                file.write("\n## Database Integration\n")
                if "postgresql" in database_tech:
                    file.write(
                        """- Use SQLAlchemy or ORM appropriately
- Implement proper migration strategies
- Use connection pooling for efficiency
- Design normalized database schema
- Use appropriate indexes for query optimization
- Implement transactions for data consistency
"""
                    )
                elif "mongodb" in database_tech:
                    file.write(
                        """- Design document schemas with appropriate validation
- Use indexes for frequently queried fields
- Implement proper error handling for database operations
- Consider data aggregation pipelines for complex queries
- Handle MongoDB-specific connection concerns
- Use appropriate data modeling patterns for document databases
"""
                    )
                elif "sqlite" in database_tech:
                    file.write(
                        """- Understand SQLite concurrency limitations
- Use appropriate journal modes for your use case
- Implement efficient query patterns
- Consider using SQLAlchemy for ORM capabilities
- Maintain proper backup strategies
"""
                    )

            file.write(
                """
## Testing
- Test all API endpoints thoroughly
- Include tests for authentication and authorization
- Test for error conditions and edge cases
- Include performance tests for critical endpoints
- Test for security vulnerabilities
"""
            )

        # Create frontend-specific instructions if applicable
        if has_frontend:
            frontend_file_name = f"{frontend_tech.replace('.', '')}.instructions.md"
            with open(
                os.path.join(instructions_dir, frontend_file_name),
                "w",
                encoding="utf-8",
            ) as file:
                if "vue" in frontend_tech:
                    file.write(
                        """---
applyTo: "**/*.vue"
---
# Vue.js Development Guidelines

## Component Structure
- Use Single File Components (SFC) with clear separation of template, script, and style
- Follow Vue.js Style Guide priority A and B rules
- Use composition API for new components
- Keep components focused on a single responsibility
- Use props validation with appropriate types

## State Management
- Use reactive refs and computed properties appropriately
- For complex state, consider Pinia or Vuex
- Avoid excessive prop drilling
- Maintain unidirectional data flow
- Use provide/inject for deeply nested component communication

## Styling
- Use scoped styles or CSS modules to prevent leakage
- Consider using utility-first CSS frameworks like Tailwind
- Maintain consistent naming conventions for CSS classes
- Use CSS variables for theming
- Optimize for mobile responsiveness

## Performance
- Use computed properties for derived state
- Implement proper component lazy-loading
- Use v-memo for optimizing updates of large lists
- Avoid unnecessary re-renders
- Use v-once for static content

## Testing
- Write unit tests for components using Vue Test Utils
- Test component props, events, and slots
- Mock external dependencies and API calls
- Test user interactions and state changes
- Write end-to-end tests for critical user flows
"""
                    )
                elif "react" in frontend_tech:
                    file.write(
                        """---
applyTo: "**/*.jsx"
---
# React Development Guidelines

## Component Structure
- Use functional components with hooks
- Keep components focused on a single responsibility
- Use proper prop types or TypeScript interfaces
- Follow component composition patterns
- Implement consistent error boundaries

## State Management
- Use useState, useReducer, and useContext appropriately
- For complex state, consider Redux or Zustand
- Maintain unidirectional data flow
- Avoid prop drilling with composition or context
- Keep state as close as possible to where it's used

## Styling
- Choose and stick with one styling approach (CSS Modules, styled-components, etc.)
- Consider using utility-first CSS frameworks like Tailwind
- Maintain consistent naming conventions for CSS classes
- Use theming for consistent visual identity
- Optimize for mobile responsiveness

## Performance
- Use React.memo for expensive renders
- Implement useMemo and useCallback appropriately
- Use virtualization for long lists
- Optimize images and assets
- Implement code splitting with lazy loading

## Testing
- Write unit tests with React Testing Library
- Focus on testing behavior, not implementation
- Mock external dependencies and API calls
- Test user interactions and state changes
- Write end-to-end tests for critical user flows
"""
                    )
                elif "angular" in frontend_tech:
                    file.write(
                        """---
applyTo: "**/*.ts"
---
# Angular Development Guidelines

## Component Structure
- Follow Angular style guide
- Use OnPush change detection when possible
- Keep components focused on a single responsibility
- Use proper input/output decorators
- Implement proper lifecycle hooks

## State Management
- Use services for shared state between components
- For complex state, consider NgRx or other state management libraries
- Keep presentation and data access logic separate
- Use RxJS observables for reactive programming
- Implement proper subscription management

## Styling
- Use component-scoped styles
- Consider Angular Material or other UI libraries
- Maintain consistent naming conventions for CSS classes
- Use theming for consistent visual identity
- Optimize for mobile responsiveness

## Performance
- Implement lazy loading for feature modules
- Use trackBy for ngFor directives
- Avoid expensive computations in templates
- Optimize change detection strategy
- Use pure pipes for data transformations

## Testing
- Write unit tests with Jasmine/Karma
- Use TestBed for component testing
- Mock dependencies with providers
- Test component templates with fixture debugging
- Write end-to-end tests with Cypress or Protractor
"""
                    )
                else:
                    file.write(
                        """---
applyTo: "**/static/**/*.js"
---
# Frontend Development Guidelines

## Structure
- Organize code into logical modules or components
- Keep files focused on a single responsibility
- Use consistent naming conventions
- Implement proper error handling
- Follow separation of concerns

## Styling
- Maintain consistent CSS naming conventions
- Optimize for mobile responsiveness
- Use CSS variables for theming
- Minimize specificity conflicts
- Keep selectors simple and maintainable

## Performance
- Minimize DOM manipulations
- Optimize resource loading
- Implement proper event delegation
- Use asynchronous loading where appropriate
- Optimize images and assets

## Testing
- Write unit tests for business logic
- Test user interactions
- Mock external dependencies
- Write end-to-end tests for critical flows
- Test across different browsers and devices
"""
                    )

        # Create database-specific instructions if applicable
        if (
            database_tech and project_type != "web"
        ):  # Only create if not already covered in web instructions
            db_file_name = "database.instructions.md"
            with open(
                os.path.join(instructions_dir, db_file_name), "w", encoding="utf-8"
            ) as file:
                file.write(
                    """---
applyTo: "**/*.py"
---
# Database Usage Guidelines

"""
                )
                if "postgresql" in database_tech:
                    file.write(
                        """## PostgreSQL Best Practices
- Use SQLAlchemy for database operations
- Implement proper connection pooling
- Write migrations for schema changes
- Use appropriate indexes for query optimization
- Implement proper transactions for data consistency
- Follow normalization principles for database design
- Use parametrized queries to prevent SQL injection
- Implement proper error handling for database operations
- Consider using pgAdmin or similar tools for database management
- Regularly backup your database
"""
                    )
                elif "mongodb" in database_tech:
                    file.write(
                        """## MongoDB Best Practices
- Use PyMongo or ODM libraries like MongoEngine
- Design document schemas with appropriate validation
- Use indexes for frequently queried fields
- Implement proper error handling for database operations
- Consider data aggregation pipelines for complex queries
- Use appropriate data modeling patterns for document databases
- Implement proper connection pool management
- Consider MongoDB Atlas for cloud hosting
- Use projections to limit returned fields
- Implement proper error handling
"""
                    )
                elif "sqlite" in database_tech:
                    file.write(
                        """## SQLite Best Practices
- Understand SQLite concurrency limitations
- Use appropriate journal modes for your use case
- Implement efficient query patterns
- Consider using SQLAlchemy for ORM capabilities
- Maintain proper backup strategies
- Use parametrized queries to prevent SQL injection
- Implement proper error handling
- Use appropriate index strategies
- Understand SQLite type affinity system
- Use appropriate constraints for data integrity
"""
                    )
                else:
                    file.write(
                        """## Database Best Practices
- Use appropriate ORM or database adapter
- Implement connection pooling if applicable
- Write migrations for schema changes
- Use parametrized queries to prevent SQL injection
- Implement proper error handling for database operations
- Design efficient database schema
- Use appropriate indexes for query optimization
- Implement proper transactions for data consistency
- Regularly backup your database
- Consider using connection pooling for efficiency
"""
                    )

    # Create AI/ML-specific instructions if applicable
    if project_type == "ai":
        with open(
            os.path.join(instructions_dir, "ai.instructions.md"), "w", encoding="utf-8"
        ) as file:
            file.write(
                """---
applyTo: "**/*.py"
---
# AI/ML Development Guidelines

## Model Development
- Separate model definition, training, and inference
- Document model architecture and hyperparameters
- Implement proper abstraction for different model types
- Use appropriate model serialization (e.g., pickle, joblib, TensorFlow SavedModel)
- Version control your models and training data

## Data Processing
- Create reproducible data preprocessing pipelines
- Implement proper train/validation/test splits
- Document data transformations and feature engineering
- Implement proper handling for missing values and outliers
- Use appropriate data normalization or standardization

## Training Workflow
- Log metrics and hyperparameters during training
- Implement early stopping and checkpointing
- Use appropriate evaluation metrics for your problem
- Implement cross-validation where appropriate
- Consider using experiment tracking tools (MLflow, Weights & Biases)

## Model Evaluation
- Use appropriate metrics for your problem type (classification, regression, etc.)
- Implement proper validation strategies
- Create visualizations for model performance
- Analyze failure cases and edge conditions
- Document model limitations and assumptions

## Production Considerations
- Optimize models for inference performance
- Implement proper error handling for predictions
- Consider model monitoring and drift detection
- Document inference requirements and dependencies
- Implement appropriate security measures for sensitive models

## Ethical Considerations
- Document potential biases in training data
- Consider fairness metrics across different groups
- Implement transparency measures for model decisions
- Document intended use cases and limitations
- Consider privacy implications of model outputs
"""
            )

    # Create data-specific instructions if applicable
    if project_type == "data":
        with open(
            os.path.join(instructions_dir, "data.instructions.md"),
            "w",
            encoding="utf-8",
        ) as file:
            file.write(
                """---
applyTo: "**/*.py"
---
# Data Analysis Guidelines

## Data Organization
- Store raw data in a dedicated directory
- Keep processed data separate from raw data
- Use consistent naming conventions for datasets
- Document data sources and transformations
- Implement version control for data when feasible

## Code Structure
- Separate data acquisition, cleaning, and analysis
- Create reusable utility functions for common operations
- Use Pandas, NumPy, and similar libraries effectively
- Optimize memory usage for large datasets
- Document data transformation steps

## Notebook Best Practices
- Structure notebooks with clear sections and headings
- Include markdown cells explaining the analysis
- Keep code cells focused and concise
- Restart and run all cells to verify reproducibility
- Consider converting critical code to modules

## Visualization
- Use appropriate chart types for different data
- Implement consistent styling for visualizations
- Include proper titles, labels, and legends
- Consider colorblind-friendly color palettes
- Create both exploratory and explanatory visualizations

## Performance
- Profile code to identify bottlenecks
- Use vectorized operations when possible
- Consider chunking for large datasets
- Implement caching for expensive computations
- Use appropriate data types to reduce memory usage

## Analysis Documentation
- Document hypotheses and assumptions
- Explain methodology and approach
- Include statistical justification
- Highlight limitations and potential biases
- Document conclusions and next steps
"""
            )

    # Create add_feature prompt template
    with open(
        os.path.join(prompts_dir, "add_feature.prompt.md"), "w", encoding="utf-8"
    ) as file:
        file.write(
            f"""---
mode: 'agent'
tools: ['codebase', 'file_search']
description: 'Add new feature to the project'
---
# Add New Feature to {project_name}

Your goal is to implement a new feature in the {project_name} project.

If not provided, ask for the feature name and description. Search #codebase to understand the current project structure and implementation patterns.

Follow these steps:
1. Analyze the current codebase to understand the architecture
2. Design the new feature to integrate seamlessly with existing code
3. Implement the feature following all project standards
4. Add appropriate tests for the new functionality
5. Update documentation to reflect the new feature

Requirements:
- Follow the [Python style guidelines](../instructions/python_style.instructions.md)
- For CLI components, follow the [CLI guidelines](../instructions/cli.instructions.md)
- Include detailed docstrings for all new functions and classes
- Ensure all new code has corresponding tests
- Maintain backward compatibility with existing functionality
- Add appropriate error handling for the new feature

After implementing, run tests to ensure the feature works as expected and doesn't break existing functionality.
"""
        )

    # Create generate_tests prompt template
    with open(
        os.path.join(prompts_dir, "generate_tests.prompt.md"), "w", encoding="utf-8"
    ) as file:
        file.write(
            """---
mode: 'agent'
tools: ['codebase', 'file_search']
description: 'Generate comprehensive tests'
---
# Generate Comprehensive Tests

Your goal is to create a comprehensive test suite for a module or function in the project.

If not provided,
ask for the specific module or function to test. Search #codebase to understand the current implementation and existing test patterns.

Follow these steps:
1. Analyze the module or function to understand its functionality and edge cases
2. Identify existing test patterns in the project
3. Create test fixtures and helper functions as needed
4. Write unit tests for all public functions, including:
   - Happy path tests for expected functionality
   - Edge case tests for boundary conditions
   - Error case tests for exception handling
5. Ensure appropriate test coverage

Requirements:
- Follow the [Testing guidelines](../instructions/testing.instructions.md)
- Use pytest fixtures for reusable test setup
- Include docstrings for test functions describing what they test
- Make tests deterministic and isolated
- Aim for high test coverage (80%+)
- Mock external dependencies appropriately

After implementing, run the tests to ensure they all pass and provide useful feedback when they fail.
"""
        )

    # Create code_review prompt template
    with open(
        os.path.join(prompts_dir, "code_review.prompt.md"), "w", encoding="utf-8"
    ) as file:
        file.write(
            """---
mode: 'agent'
tools: ['codebase', 'file_search']
description: 'Code review and refactoring suggestions'
---
# Code Review and Refactoring

Your goal is to review code for quality, style, and performance issues and suggest improvements.

If not provided, ask for the specific file or module to review. Search #codebase to understand the current implementation and project patterns.

Follow these steps:
1. Analyze the code for:
   - Adherence to Python style guidelines
   - Potential bugs or edge cases
   - Performance issues
   - Maintainability concerns
   - Testing coverage
2. Identify areas for improvement
3. Suggest specific refactoring changes with code examples
4. Explain the benefits of each suggested change

Focus on:
- Code organization and readability
- Function and variable naming
- Error handling and edge cases
- Performance optimization opportunities
- Test coverage and quality

Provide a summary of findings with severity levels (critical, major, minor) and concrete suggestions for improvement. When possible,
provide before/after code examples to illustrate proposed changes.
"""
        )

    # Create .vscode directory and settings.json
    vscode_dir = os.path.join(project_dir, ".vscode")
    os.makedirs(vscode_dir, exist_ok=True)

    with open(os.path.join(vscode_dir, "settings.json"), "w", encoding="utf-8") as file:
        file.write(
            """{"python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.linting.mypyEnabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "88"],
  "editor.formatOnSave": true,
  "editor.rulers": [88],
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.nosetestsEnabled": false,
  "python.testing.pytestArgs": [
    "tests"
  ],
  "github.copilot.chat.codeGeneration.useInstructionFiles": true,
  "chat.promptFiles": true,
  "chat.instructionsFilesLocations": [".github/instructions"],
  "chat.promptFilesLocations": [".github/prompts"]}
"""
        )
