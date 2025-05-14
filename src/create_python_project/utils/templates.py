#!/usr/bin/env python3
"""
Templates Module

This module provides project templates and utilities for generating files
from templates based on the project type and user inputs.
"""

import os
import string
from pathlib import Path
from typing import Any, Dict, List, Tuple


def get_template_path(template_name: str) -> Path:
    """
    Get the path to a template file.

    Args:
        template_name: Name of the template

    Returns:
        Path to the template file
    """
    # Get the directory of this module
    module_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate to the templates directory
    templates_dir = os.path.join(module_dir, "..", "templates")

    # Construct the path to the specific template
    template_path = os.path.join(templates_dir, template_name)

    return Path(template_path)


def render_template(template_content: str, context: Dict[str, Any]) -> str:
    """
    Render a template string with the given context.

    Args:
        template_content: Template content as a string
        context: Dictionary containing template variables

    Returns:
        Rendered template as a string
    """
    # Create a template object
    template = string.Template(template_content)

    # Render the template with the context
    return template.safe_substitute(context)


def create_file_from_template(
    template_content: str,
    output_path: str,
    context: Dict[str, Any],
) -> Tuple[bool, str]:
    """
    Create a file from a template.

    Args:
        template_content: Template content
        output_path: Path where the file should be created
        context: Dictionary containing template variables

    Returns:
        Tuple containing success status and message
    """
    try:
        # Render the template
        rendered_content = render_template(template_content, context)

        # Create any necessary directories
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Write the rendered content to the output file
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(rendered_content)

        return True, f"Created file at {output_path}"
    except Exception as e:
        return False, f"Failed to create file: {str(e)}"


def get_template_variables(template_content: str) -> List[str]:
    """
    Get the variables required for a specific template.

    Args:
        template_content: Template content

    Returns:
        List of variable names required by the template
    """
    # Parse template for $variable or ${variable} patterns
    variables = []

    # Create a template object
    template = string.Template(template_content)

    # Extract identifiers (variables) from the template pattern
    # This is a simple implementation. A more robust one would use regex
    for match in template.pattern.findall(template_content):
        if match[1]:  # Named identifier in ${identifier} form
            variables.append(match[1])
        elif match[2]:  # Named identifier in $identifier form
            variables.append(match[2])

    return list(set(variables))


# Template content for different project types
PROJECT_TEMPLATES = {
    "basic": {
        "README.md": """# $project_name

$project_description

## Installation

```bash
pip install $package_name
```

## Usage

```python
import $package_name
```

## License

$license
""",
        "main.py": """#!/usr/bin/env python3
\"\"\"
$project_name - $project_description
\"\"\"

def main():
    \"\"\"Main entry point for the application.\"\"\"
    print("Hello from $project_name!")

if __name__ == "__main__":
    main()
""",
    },
    "cli": {
        "cli.py": """#!/usr/bin/env python3
\"\"\"
Command-line interface for $project_name
\"\"\"

import argparse
import sys


def parse_arguments():
    \"\"\"Parse command-line arguments.\"\"\"
    parser = argparse.ArgumentParser(description="$project_description")
    parser.add_argument('-v', '--version', action='store_true', help='Show version information and exit')
    # Add more arguments here
    return parser.parse_args()


def main():
    \"\"\"Main entry point for the application.\"\"\"
    args = parse_arguments()

    if args.version:
        from $package_name import __version__
        print(f"$project_name version {__version__}")
        return 0

    # Main application logic here
    print("Hello from $project_name!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
"""
    },
    "web": {
        "app.py": """#!/usr/bin/env python3
\"\"\"
Web application for $project_name
\"\"\"

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    \"\"\"Render the index page.\"\"\"
    return render_template('index.html', title="$project_name")


@app.route('/about')
def about():
    \"\"\"Render the about page.\"\"\"
    return render_template('about.html', title="About $project_name")


def create_app():
    \"\"\"Create and configure the Flask app.\"\"\"
    # Configuration can be added here
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
"""
    },
}
