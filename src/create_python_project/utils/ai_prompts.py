#!/usr/bin/env python3
"""
AI Prompts Module

This module contains prompt templates for interacting with AI providers.
"""


def get_project_type_prompt(project_name: str, project_description: str) -> str:
    """
    Get a prompt for determining the project type.

    Args:
        project_name: Name of the project
        project_description: Description of the project

    Returns:
        Formatted prompt for AI
    """
    return f"""
You are an expert Python developer tasked with determining the most suitable project type for the following project:

Project Name: {project_name}
Project Description: {project_description}

Please analyze the project description and select the most appropriate project type from the following options:
1. basic (Standard Python package)
2. cli (Command-line interface application)
3. web (Web application, e.g., Flask, FastAPI)
4. api (API service)
5. data (Data analysis/science project)
6. ai (AI/ML project)
7. gui (Desktop GUI application)

Respond with just one of these project types, all lowercase, and a brief explanation of why you selected it.
Format: "project_type: brief explanation"
"""


def get_technology_stack_prompt(
    project_name: str, project_description: str, project_type: str
) -> str:
    """
    Get a prompt for suggesting a technology stack for the project.

    Args:
        project_name: Name of the project
        project_description: Description of the project
        project_type: Type of the project (web, cli, etc.)

    Returns:
        Formatted prompt for AI
    """
    return f"""
You are an expert Python developer tasked with recommending the most suitable technology stack for the following project:

Project Name: {project_name}
Project Description: {project_description}
Project Type: {project_type}

Please recommend a complete technology stack organized by categories.
For each category, recommend 1-3 options with the first being your top recommendation.

Your response should follow this JSON format exactly:

{{
  "categories": [
    {{
      "name": "Category Name",
      "description": "Description of this technology category",
      "options": [
        {{"name": "Technology Name 1",
          "description": "Clear description of this technology and why it suits this project",
          "recommended": true}},
        {{"name": "Technology Name 2",
          "description": "Description of alternative technology",
          "recommended": false}}
      ]
    }},
    {{
      "name": "Next category...",
      "description": "Description of this category",
      "options": []
    }}
  ],
  "analysis": [
    "Key feature needed: Feature 1",
    "Key feature needed: Feature 2",
    "Key feature needed: Feature 3",
    "Key feature needed: Feature 4"
  ]
}}

For a {project_type} project, include relevant technology categories such as:
- Backend Framework (if applicable)
- Database (if applicable)
- Authentication (if applicable)
- Frontend Technology (if applicable)
- Data Processing (if applicable)
- Testing Tools
- Deployment Options
- Any other categories relevant to the specific project needs

Analyze the project description carefully to identify the key requirements and recommend appropriate technologies.
Choose technologies that will best suit this specific project's needs. Always mark exactly one option as recommended=true in each category.
"""


def get_project_structure_prompt(
    project_name: str,
    project_description: str,
    project_type: str,
) -> str:
    """
    Get a prompt for suggesting the project structure.

    Args:
        project_name: Name of the project
        project_description: Description of the project
        project_type: Type of the project

    Returns:
        Formatted prompt for AI
    """
    return f"""
You are an expert Python developer tasked with designing the directory structure for a new Python project.

Project Details:
- Name: {project_name}
- Description: {project_description}
- Type: {project_type}

Please suggest an optimal directory structure for this project following these guidelines:
1. Follow Python best practices and packaging standards
2. Include appropriate directories for the project type
3. Include a brief description of each directory's purpose
4. For a {project_type} project, include any specific directories or files that would be beneficial

Format your response as a structured tree with explanations, for example:
```
project_root/
├── src/  # Source code directory
│   └── package_name/  # Main package
│       ├── __init__.py  # Package initialization
│       └── module.py  # Core functionality
├── tests/  # Test directory
│   └── test_module.py  # Tests for module.py
└── docs/  # Documentation
```

Only include directories and files that are essential for this specific project type.
"""


def get_dependencies_prompt(
    project_name: str,
    project_description: str,
    project_type: str,
) -> str:
    """
    Get a prompt for suggesting dependencies.

    Args:
        project_name: Name of the project
        project_description: Description of the project
        project_type: Type of the project

    Returns:
        Formatted prompt for AI
    """
    return f"""
You are an expert Python developer tasked with recommending the most appropriate dependencies for a new Python project.

Project Details:
- Name: {project_name}
- Description: {project_description}
- Type: {project_type}

Please recommend essential Python packages (dependencies) for this project based on:
1. The project description and type
2. Current best practices in Python development
3. Stability and community support of packages

Format your response as:
1. A list of essential production dependencies with brief explanations
2. A list of recommended development dependencies with brief explanations
3. For each dependency, specify the name as it would appear in a pyproject.toml file

Example format:
```
Production Dependencies:
- package1: Description of what this package does and why it's needed
- package2: Description of what this package does and why it's needed

Development Dependencies:
- test-package: Testing framework recommended for this project
- lint-package: Code quality tool recommended for this project
```

Be selective and focus on the most relevant packages for this specific project. Only recommend well-established packages with good community support.
"""
