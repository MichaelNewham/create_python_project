#!/usr/bin/env python3
"""
AI Prompts Module

This module contains prompt templates for interacting with AI providers.
"""


def get_project_type_prompt(
    project_name: str, project_description: str, context: dict | None = None
) -> str:
    """
    Get a prompt for determining the project type with rich context.

    Args:
        project_name: Name of the project
        project_description: Description of the project
        context: Dictionary with problem, users, inspiration

    Returns:
        Formatted prompt for AI
    """
    context = context or {}

    context_section = ""
    if context:
        context_section = f"""
**Additional Context:**
- Problem being solved: {context.get('problem', 'Not specified')}
- Target users: {context.get('users', 'Not specified')}
- Inspiration/Examples: {context.get('inspiration', 'Not specified')}
"""

    return f"""
You are an expert Python developer tasked with determining the most suitable project type for the following project:

**Project Name:** {project_name}
**Project Description:** {project_description}
{context_section}

Please analyze all the information and select the most appropriate project type from these categories:

**Application Types:**
- cli (Terminal tools and scripts for automation)
- web (Browser-based interfaces and full-stack applications)
- mobile-backend (Server-side services specifically for mobile applications)
- gui (Native desktop applications with graphical interfaces)

**Service Types:**
- api (RESTful/GraphQL endpoints for general consumption)
- microservice (Single-responsibility service in distributed architecture)

**Analysis Types:**
- data (Data processing, analytics, and scientific computing)
- ai (Machine learning models and AI applications)

**Development Types:**
- library (Reusable packages and tools for other developers)
- automation (Workflow automation, bots, and system integration)

Respond with just one of these project types, all lowercase, and a brief explanation of why you selected it.
Format your response EXACTLY as: "project_type: brief explanation" where project_type is one of the exact types listed above.

IMPORTANT: Your first line MUST follow this exact format with the project type appearing first, followed by a colon, then your explanation.
For example: "cli: This project would be best as a command-line tool because it focuses on automation tasks."
"""


def get_comprehensive_analysis_prompt(
    project_name: str, project_description: str, context: dict | None = None
) -> str:
    """
    Get a prompt for comprehensive project analysis including architecture and tech stack.

    Args:
        project_name: Name of the project
        project_description: Description of the project
        context: Dictionary with problem, users, inspiration

    Returns:
        Formatted prompt for AI
    """
    context = context or {}

    context_section = ""
    if context:
        context_section = f"""
**Additional Context:**
- Problem being solved: {context.get('problem', 'Not specified')}
- Target users: {context.get('users', 'Not specified')}
- Inspiration/Examples: {context.get('inspiration', 'Not specified')}
"""

    return f"""
You are an expert software architect tasked with designing the complete solution for the following project:

**Project Name:** {project_name}
**Project Description:** {project_description}
{context_section}

Please provide a comprehensive analysis and design recommendation in the following JSON format:

{{
  "recommended_architecture": {{
    "type": "web|cli|gui|api|data|ai|mobile-backend",
    "approach": "Brief description of the recommended approach",
    "reasoning": "2-3 sentences explaining why this architecture is optimal for this specific project"
  }},
  "technology_stack": {{
    "categories": [
      {{
        "name": "Category Name",
        "description": "What this technology category handles",
        "options": [
          {{
            "name": "Exact Package Name",
            "description": "Why this technology fits this specific project",
            "recommended": true,
            "reasoning": "Specific reason why this is best for the user's needs",
            "install_type": "python|npm|system|manual"
          }}
        ]
      }}
    ]
  }},
  "project_structure": {{
    "type": "Brief description of structure (e.g., 'Modern web app with API backend')",
    "key_features": [
      "Feature 1 that directly addresses user needs",
      "Feature 2 that solves stated problems",
      "Feature 3 that matches user inspiration"
    ],
    "user_experience": "How the end user will interact with this solution"
  }},
  "future_flexibility": {{
    "expansion_options": ["Potential future enhancements"],
    "alternative_deployments": ["Other ways this could be deployed/packaged"]
  }}
}}

**CRITICAL PACKAGE NAMING REQUIREMENTS:**

For "name" field in technology options, you MUST use EXACT installable package names:
- Python packages: Use actual PyPI names (e.g., "fastapi", "flask", "psycopg2-binary", "elasticsearch")
- npm packages: Use actual npm names (e.g., "react", "vue", "@types/node", "express")
- System services: Use "install_type": "system" and provide setup instructions in description
- Custom components: Use "install_type": "manual" and provide build instructions

**INVALID EXAMPLES TO AVOID:**
❌ "Custom Python Agent" (not a real package)
❌ "Elasticsearch + Kibana" (multiple services, use separate entries)
❌ "Python (Flask/FastAPI)" (multiple options, pick one)
❌ "Vue.js or React" (multiple options, pick one)

**VALID EXAMPLES:**
✅ "fastapi" with install_type: "python"
✅ "react" with install_type: "npm"
✅ "postgresql" with install_type: "system"
✅ "monitoring-agent" with install_type: "manual"

Focus on:
1. Choose architecture that best solves the user's actual problems
2. Select technologies that work coherently together
3. Use ONLY real, installable package names or mark as system/manual
4. Consider the target users' technical expertise level
5. Ensure technologies support the key features needed

IMPORTANT: Respond with ONLY the valid JSON object. Do not include any markdown formatting, code blocks, or additional text. Start your response with {{ and end with }}.
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

IMPORTANT: Your response MUST be a valid JSON object and NOTHING ELSE.
Do not include any explanatory text, markdown formatting, or code blocks before or after the JSON.
The response should be parseable by Python's json.loads() function.

Your response must follow this JSON format exactly:

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
    {{"name": "Next category...",
      "description": "Description of this category",
      "options": []}}
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

REMEMBER: Your entire response must be a single, valid JSON object with no additional text or formatting.
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
