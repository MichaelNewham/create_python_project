#!/usr/bin/env python3
"""
Extension Configuration Generator

Manages VS Code/Cursor extension recommendations based on project type.
"""


def get_extensions_for_project(
    project_type: str, tech_stack: dict[str, str]
) -> list[str]:
    """Return VS Code/Cursor extensions based on project configuration."""

    # Base Python extensions for all projects
    extensions = [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "charliermarsh.ruff",
        "njpwerner.autodocstring",
        "tamasfe.even-better-toml",
        "GitHub.copilot",
        "GitHub.copilot-chat",
        "eamodio.gitlens",
        "streetsidesoftware.code-spell-checker",
    ]

    # Project-specific extensions
    if project_type == "web":
        extensions.extend(_get_web_extensions(tech_stack))
    elif project_type == "data":
        extensions.extend(_get_data_extensions())
    elif project_type == "api":
        extensions.extend(_get_api_extensions(tech_stack))

    return extensions


def _get_web_extensions(tech_stack: dict[str, str]) -> list[str]:
    """Get web development specific extensions."""
    extensions = []

    # Django extensions
    if tech_stack.get("Backend Framework") == "Django":
        extensions.extend(["batisteo.vscode-django", "wholroyd.jinja"])

    # React/Frontend extensions
    if tech_stack.get("Frontend") == "React":
        extensions.extend(
            [
                "dsznajder.es7-react-js-snippets",
                "dbaeumer.vscode-eslint",
                "esbenp.prettier-vscode",
                "bradlc.vscode-tailwindcss",
                "formulahendry.auto-rename-tag",
                "ms-vscode.vscode-typescript-next",
            ]
        )

    # Database extensions
    if tech_stack.get("Database") == "PostgreSQL":
        extensions.append("ckolkman.vscode-postgres")
    elif tech_stack.get("Database") == "MongoDB":
        extensions.append("mongodb.mongodb-vscode")

    return extensions


def _get_data_extensions() -> list[str]:
    """Get data science specific extensions."""
    return [
        "ms-toolsai.jupyter",
        "ms-python.vscode-jupyter-cell-tags",
        "ms-python.vscode-jupyter-slideshow",
        "mechatroner.rainbow-csv",
        "randomfractalsinc.vscode-data-preview",
    ]


def _get_api_extensions(tech_stack: dict[str, str]) -> list[str]:
    """Get API development specific extensions."""
    extensions = ["humao.rest-client", "42crunch.vscode-openapi"]

    if tech_stack.get("API Framework") == "FastAPI":
        extensions.append("ms-python.vscode-pylance")

    return extensions
