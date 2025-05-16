#!/usr/bin/env python3
"""
Create Python Project - Main Application

This is the main entry point for the Create Python Project application.
It handles the CLI interface and orchestrates the project creation process.
"""

import os
import sys
from typing import Dict, Tuple

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv(override=True)
except ImportError:
    print(
        "Warning: python-dotenv not installed. Install it using 'poetry add python-dotenv' to load environment variables from .env files."
    )

# Better input handling with arrow keys
from prompt_toolkit import prompt as pt_prompt
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.text import Text

# Local imports
from create_python_project.utils import (
    ai_integration,
    ai_prompts,
    config,
    core_project_builder,
)
from create_python_project.utils import logging as log_utils

# Initialize logger
logger = log_utils.setup_logging()

# Initialize Rich console
console = Console()


def get_project_info() -> Tuple[bool, Dict[str, str]]:
    """
    Get project information from the user.

    Returns:
        Tuple containing success status and project info dictionary
    """
    console.print("\n")
    title_panel = Panel(
        Text(
            "🐍 Python Project Initializer 🐍",
            justify="center",
            style="bold green",
        ),
        subtitle=Text(
            "Create professional Python projects in seconds",
            style="italic blue",
            justify="center",
        ),
        style="bold blue",
        border_style="blue",
        expand=True,
    )
    console.print(title_panel)

    # Show features
    console.print(
        "[yellow]⚡ AI-Powered ⚡ Best Practices ⚡ Fully Customizable ⚡[/yellow]",
        justify="center",
    )
    console.print("\n")

    welcome_text = "[bold cyan]Welcome to Create Python Project![/bold cyan] Let's set up your new project."
    console.print(welcome_text)

    project_info = {}

    # Get project name
    console.print("\n[bold magenta]Step 1: Project Name[/bold magenta]")
    console.print("Please enter a name for your project: ", end="")
    project_name = pt_prompt()
    if not project_name:
        console.print("[bold red]Error:[/bold red] Project name is required")
        return False, {"error": "Project name is required"}
    project_info["project_name"] = project_name

    # Get project directory with improved prompt
    default_dir = os.path.join(
        os.getcwd(), project_name.replace(" ", "_").replace("-", "_").lower()
    )
    console.print(f"Enter project directory (default: {default_dir}): ", end="")
    # Use the default value as initial text to avoid repetition
    project_dir = pt_prompt(default=default_dir) or default_dir
    project_info["project_dir"] = project_dir

    # Author information - make it clearly optional
    console.print("\n[bold]Author Information (optional)[/bold]")
    console.print(
        "[italic]Used for project metadata, Git configuration, and documentation.[/italic]"
    )
    console.print("Enter your name (optional, press Enter to skip): ", end="")
    author_name = pt_prompt()
    project_info["author_name"] = author_name

    # Make email field optional with clear skip instructions
    if author_name:  # Only ask for email if name was provided
        console.print("Enter your email (optional, press Enter to skip): ", end="")
        author_email = pt_prompt()
        project_info["author_email"] = author_email
    else:
        project_info["author_email"] = ""

    return True, project_info


def determine_project_type(project_info: Dict[str, str]) -> Tuple[bool, str]:
    """
    Determine the project type based on project description.

    Args:
        project_info: Dictionary containing project information

    Returns:
        Tuple containing success status and project type
    """
    # Get available project types
    project_types = config.get_project_types()

    console.print("\n")
    section_panel = Panel(
        Text("🔍 PROJECT TYPE DETECTION", justify="center"),
        style="bold green",
        border_style="green",
        expand=True,
    )
    console.print(section_panel)

    console.print("\n[bold magenta]Step 3: Project Description[/bold magenta]")

    if not project_info.get("project_description"):
        project_info["project_description"] = Prompt.ask(
            "Please describe your project (this helps with AI recommendations)"
        )

    console.print(
        "\nYou can select a project type or let AI suggest one based on your description."
    )
    ai_suggestion = Confirm.ask(
        "[bold cyan]Would you like AI to suggest a project type?[/bold cyan]",
        default=True,
    )

    # Select AI provider first if wanting AI suggestions
    selected_provider = None
    if ai_suggestion:
        providers = ai_integration.get_available_ai_providers()
        if not providers:
            console.print(
                "[bold yellow]No AI providers available. Please set up API keys in your environment variables.[/bold yellow]"
            )
            ai_suggestion = False
        else:
            provider_success, selected_provider = ai_integration.select_ai_provider(
                providers
            )
            if not provider_success or not selected_provider:
                console.print(
                    "[bold yellow]Failed to select an AI provider. Falling back to manual selection.[/bold yellow]"
                )
                ai_suggestion = False

    # Now proceed with project type analysis if we have a provider
    if ai_suggestion and selected_provider:
        # Try to use AI to determine project type
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]Analyzing your project description...[/bold cyan]"),
            console=console,
        ) as progress:
            task = progress.add_task("Analyzing", total=None)

            # Generate prompt
            prompt = ai_prompts.get_project_type_prompt(
                project_info["project_name"],
                project_info["project_description"],
            )

            # Get AI response
            ai_success, response = selected_provider.generate_response(prompt)

            # Stop the progress indicator before showing results
            progress.update(task, completed=True)
            progress.stop()

            if ai_success:
                # Extract project type from response
                response_lines = response.strip().split("\n")
                for line in response_lines:
                    if ":" in line:
                        suggested_type, explanation = line.split(":", 1)
                        suggested_type = suggested_type.strip().lower()

                        if suggested_type in project_types:
                            console.print(
                                f"\n[bold green]Based on your description, I recommend a '[cyan]{suggested_type}[/cyan]' project.[/bold green]"
                            )
                            console.print(
                                f"[italic]Explanation: {explanation.strip()}[/italic]"
                            )

                            confirm = Confirm.ask(
                                "[bold cyan]Do you want to use this suggestion?[/bold cyan]",
                                default=True,
                            )
                            if confirm:
                                return True, suggested_type
                            break

                console.print(
                    "[bold yellow]AI couldn't determine a suitable project type from your description.[/bold yellow]"
                )
                ai_suggestion = False
            else:
                console.print(
                    f"[bold red]Error getting AI suggestion:[/bold red] {response}"
                )
                ai_suggestion = False

    if not ai_suggestion:
        # Manual selection
        console.print("\n[bold]Please select a project type:[/bold]")

        project_type_list = []
        for type_key, type_info in project_types.items():
            project_type_list.append(
                f"{type_info['name']} - {type_info['description']}"
            )

        for i, item in enumerate(project_type_list, 1):
            console.print(f"[cyan]{i}.[/cyan] {item}")

        try:
            selection = Prompt.ask(
                "[bold cyan]Select project type[/bold cyan]",
                choices=[str(i) for i in range(1, len(project_type_list) + 1)],
                default="1",
            )
            index = int(selection) - 1

            # Extract type key from selection
            type_key = list(project_types.keys())[index]
            return True, type_key

        except Exception as e:
            console.print(
                f"[bold red]Error selecting project type:[/bold red] {str(e)}"
            )
            return False, "Failed to select project type"

    return False, "Failed to determine project type"


def create_project(project_info: Dict[str, str], project_type: str) -> Tuple[bool, str]:
    """
    Create the project structure.

    Args:
        project_info: Dictionary containing project information
        project_type: Type of the project

    Returns:
        Tuple containing success status and message
    """
    console.print("\n")
    section_panel = Panel(
        Text(
            "[bold magenta]Step 4: Project Type and Technology Selection[/bold magenta]",
            justify="center",
        ),
        style="bold magenta",
        border_style="magenta",
        expand=True,
    )
    console.print(section_panel)

    # Show selected project type
    project_types = config.get_project_types()
    type_info = project_types.get(project_type, {"name": project_type.capitalize()})
    console.print(f"\n[bold yellow]{type_info['name']}[/bold yellow]")

    # Create project structure
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold magenta]Creating project structure...[/bold magenta]"),
        console=console,
    ) as progress:
        task = progress.add_task("Creating", total=None)

        structure_success, message = core_project_builder.create_project_structure(
            project_name=project_info["project_name"],
            project_dir=project_info["project_dir"],
            project_type=project_type,
            with_ai=True,
            **project_info,
        )

        progress.update(task, completed=True)

    if not structure_success:
        console.print(f"[bold red]Error:[/bold red] {message}")
        return False, message

    console.print(f"\n[bold green]✅ {message}[/bold green]")

    # Set up Git repository
    console.print("\n")
    git_panel = Panel(
        Text("🔄 GIT REPOSITORY SETUP", justify="center"),
        style="bold cyan",
        border_style="cyan",
        expand=True,
    )
    console.print(git_panel)

    setup_git = Confirm.ask(
        "[bold cyan]Do you want to initialize a Git repository?[/bold cyan]",
        default=True,
    )

    if setup_git:
        # Ask for GitHub username
        console.print("\n[bold]Remote Repository Setup (optional)[/bold]")
        console.print("[italic]Configure remotes for GitHub and GitLab[/italic]")
        console.print(
            "Enter your GitHub username (optional, press Enter to skip): ", end=""
        )
        github_username = pt_prompt()

        # Ask for GitLab username
        console.print(
            "Enter your GitLab username (optional, press Enter to skip): ", end=""
        )
        gitlab_username = pt_prompt()

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]Setting up Git repository...[/bold cyan]"),
            console=console,
        ) as progress:
            task = progress.add_task("Setting up", total=None)

            git_success, git_message = core_project_builder.initialize_git_repo(
                project_info["project_dir"],
                project_info["project_name"],
                github_username=github_username,
                gitlab_username=gitlab_username,
            )

            progress.update(task, completed=True)

        if git_success:
            console.print(f"\n[bold green]✅ {git_message}[/bold green]")

            if github_username or gitlab_username:
                console.print(
                    "\n[italic]Remote repositories have been configured but not pushed.[/italic]"
                )
                console.print(
                    "[italic]Use 'git push -u origin main' to push your code when ready.[/italic]"
                )
        else:
            console.print(f"\n[bold red]❌ {git_message}[/bold red]")
            console.print("[yellow]Continuing without Git repository...[/yellow]")

    # Set up virtual environment
    console.print("\n")
    venv_panel = Panel(
        Text("🐍 SETTING UP VIRTUAL ENVIRONMENT", justify="center"),
        style="bold yellow",
        border_style="yellow",
        expand=True,
    )
    console.print(venv_panel)

    setup_venv = Confirm.ask(
        "[bold cyan]Do you want to set up a virtual environment?[/bold cyan]",
        default=True,
    )

    if setup_venv:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold yellow]Setting up virtual environment...[/bold yellow]"),
            console=console,
        ) as progress:
            task = progress.add_task("Setting up", total=None)

            venv_success, venv_message = core_project_builder.setup_virtual_environment(
                project_info["project_dir"]
            )

            progress.update(task, completed=True)

        if venv_success:
            console.print(f"\n[bold green]✅ {venv_message}[/bold green]")
        else:
            console.print(f"\n[bold red]❌ {venv_message}[/bold red]")
            console.print("[yellow]Continuing without virtual environment...[/yellow]")

    return True, "Project created successfully"


def main() -> int:
    """Main entry point for the application."""
    try:
        # Log available AI providers for debugging
        available_providers = ai_integration.get_available_ai_providers()
        logger.debug(f"Available AI providers: {available_providers}")

        # Flow control
        success, project_info = get_project_info()
        if not success:
            console.print("\n[bold red]Failed to get project information.[/bold red]")
            return 1

        # Determine project type
        success, project_type = determine_project_type(project_info)
        if not success:
            console.print("\n[bold red]Failed to determine project type.[/bold red]")
            return 1

        # Create the project
        success, message = create_project(project_info, project_type)
        if not success:
            console.print(f"\n[bold red]Failed to create project: {message}[/bold red]")
            return 1

        # Display success message
        console.print("\n")
        success_panel = Panel(
            Text("🎉 PROJECT CREATED SUCCESSFULLY! 🎉", justify="center"),
            style="bold green",
            border_style="green",
            expand=True,
        )
        console.print(success_panel)

        console.print("\n[bold]Your new Python project has been created at:[/bold]")
        console.print(f"  [cyan]{project_info['project_dir']}[/cyan]")

        next_steps = """
## Next steps:

1. Navigate to your project directory:
   ```bash
   cd {project_dir}
   ```

2. Start coding in the `src/` directory

3. Add your tests in the `tests/` directory

4. Use Poetry to manage dependencies:
   ```bash
   poetry add <package-name>
   ```
        """.format(
            project_dir=project_info["project_dir"]
        )

        console.print(Markdown(next_steps))

        return 0

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Operation cancelled by user.[/yellow]")
        return 130
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        console.print(f"\n[bold red]❌ An error occurred:[/bold red] {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
