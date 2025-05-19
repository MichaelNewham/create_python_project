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

    # Select AI provider for project analysis
    providers = ai_integration.get_available_ai_providers()
    if not providers:
        console.print(
            "[bold yellow]No AI providers available. Please set up API keys in your environment variables.[/bold yellow]"
        )
        return manual_project_type_selection(project_types)

    provider_success, selected_provider = ai_integration.select_ai_provider(providers)
    if not provider_success or not selected_provider:
        console.print(
            "[bold yellow]Failed to select an AI provider. Falling back to manual selection.[/bold yellow]"
        )
        return manual_project_type_selection(project_types)

    # Use AI to determine project type
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]Analyzing your project description...[/bold cyan]"),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing", total=None)

        # Generate type detection prompt
        prompt = ai_prompts.get_project_type_prompt(
            project_info["project_name"],
            project_info["project_description"],
        )

        # Get AI response for project type
        ai_success, response = selected_provider.generate_response(prompt)

        # If selected provider fails, try DeepSeek as fallback
        if (
            not ai_success
            and selected_provider.__class__.__name__ != "DeepSeekProvider"
            and "DeepSeek" in providers
        ):
            console.print(
                f"[bold yellow]Selected AI provider failed: {response}. Trying DeepSeek as fallback...[/bold yellow]"
            )
            deepseek_provider = ai_integration.DeepSeekProvider()
            ai_success, response = deepseek_provider.generate_response(prompt)

        # Update progress
        progress.update(task, completed=True)
        progress.stop()

        if not ai_success:
            console.print(
                f"[bold red]Error getting AI suggestion:[/bold red] {response}"
            )
            return manual_project_type_selection(project_types)

        # Extract project type from response
        project_type = None
        explanation = ""
        response_lines = response.strip().split("\n")
        for line in response_lines:
            if ":" in line:
                suggested_type, explanation = line.split(":", 1)
                suggested_type = suggested_type.strip().lower()

                if suggested_type in project_types:
                    project_type = suggested_type
                    break

        if not project_type:
            console.print(
                "[bold yellow]AI couldn't determine a suitable project type from your description.[/bold yellow]"
            )
            return manual_project_type_selection(project_types)

    # Now that we have a project type, get technology stack recommendations
    project_info["project_type"] = project_type
    project_info["tech_stack"] = {}

    # Show AI analysis header
    console.print("\n")
    ai_header = Panel(
        Text("🤖 AI ANALYSIS COMPLETE", justify="center", style="bold white"),
        border_style="cyan",
        expand=True,
    )
    console.print(ai_header)

    # Display project type recommendation
    type_info = project_types.get(project_type, {"name": project_type.capitalize()})
    console.print("\nBased on your description, I recommend a ", end="")
    console.print(f"[bold green]'{project_type}'[/bold green]", end="")
    console.print(f" project ({type_info['name']}).")
    console.print(f"[italic]{explanation.strip()}[/italic]\n")

    # Generate technology stack prompt
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]Analyzing optimal technology stack...[/bold cyan]"),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing", total=None)

        tech_prompt = ai_prompts.get_technology_stack_prompt(
            project_info["project_name"],
            project_info["project_description"],
            project_type,
        )

        # Get AI response for technology stack
        tech_success, tech_response = selected_provider.generate_response(tech_prompt)

        # If selected provider fails, try DeepSeek as fallback
        if (
            not tech_success
            and selected_provider.__class__.__name__ != "DeepSeekProvider"
            and "DeepSeek" in providers
        ):
            console.print(
                f"[bold yellow]Selected AI provider failed for tech stack: {tech_response}. Trying DeepSeek as fallback...[/bold yellow]"
            )
            deepseek_provider = ai_integration.DeepSeekProvider()
            tech_success, tech_response = deepseek_provider.generate_response(
                tech_prompt
            )

        # Update progress
        progress.update(task, completed=True)
        progress.stop()

        if not tech_success:
            console.print(
                f"[bold yellow]Could not generate technology recommendations: {tech_response}[/bold yellow]"
            )
            return True, project_type

    # Parse the JSON response and display technology stack recommendations
    try:
        import json

        tech_data = json.loads(tech_response)

        # Display key project features identified by AI
        if "analysis" in tech_data and tech_data["analysis"]:
            console.print("I've analyzed your project needs:")
            for feature in tech_data["analysis"]:
                console.print(f"  {feature}", style="cyan")
            console.print("")

        # Display technology categories and options
        if "categories" in tech_data and tech_data["categories"]:
            console.print(
                "[bold yellow]Understanding Your Technology Stack Options:[/bold yellow]\n"
            )
            console.print(
                "Each technology category serves a specific purpose in your project. Here's what they do:\n"
            )

            # Print a brief explanation of each category first
            for category in tech_data["categories"]:
                console.print(
                    f"[bold magenta]{category['name']}[/bold magenta]: {category['description']}"
                )

            console.print(
                "\n[bold yellow]Recommended Technology Stack:[/bold yellow]\n"
            )

            for category in tech_data["categories"]:
                # Print category header with clearer explanation
                console.print(
                    f"🔹 [bold cyan]{category['name']}[/bold cyan] - {category['description']}"
                )
                console.print(
                    f"   [italic dim]Why it matters: This determines how your project will {get_category_impact(category['name'])}</italic dim>"
                )

                # Print technology options with checkboxes and clear explanations
                for option in category["options"]:
                    is_recommended = option.get("recommended", False)
                    prefix = "[x]" if is_recommended else "[ ]"
                    style = "bold green" if is_recommended else "white"

                    console.print(f"  {prefix} ", end="")
                    console.print(option["name"], style=style, end="")

                    if is_recommended:
                        console.print(" ⭐ ", end="")
                        console.print("(AI recommended)", style="italic")
                    else:
                        console.print("")

                    console.print(f"      {option['description']}")

                    # Add details on when this technology is most appropriate
                    console.print(
                        f"      [dim]Best for: {get_technology_use_case(option['name'])}</dim>"
                    )

                console.print("")

            # Allow user to customize technology selections
            console.print(
                "[bold cyan]Would you like to customize the technology selections? (yes/no)[/bold cyan]",
                end=" ",
            )
            customize = Prompt.ask("", choices=["yes", "no"], default="no")

            if customize.lower() == "yes":
                for category in tech_data["categories"]:
                    console.print(
                        f"\n[bold magenta]Select {category['name']}:[/bold magenta]"
                    )
                    console.print(
                        f"[italic]This determines how your project will {get_category_impact(category['name'])}.[/italic]"
                    )
                    options = [option["name"] for option in category["options"]]

                    # Find recommended option as default
                    default_option = next(
                        (
                            option["name"]
                            for option in category["options"]
                            if option.get("recommended", False)
                        ),
                        options[0],
                    )

                    # Display options with numbers and detailed explanations
                    for i, option_name in enumerate(options, 1):
                        is_recommended = option_name == default_option
                        style = "cyan" if is_recommended else "white"
                        recommendation = " (AI recommended)" if is_recommended else ""
                        console.print(
                            f"  {i}. [bold {style}]{option_name}[/bold {style}]{recommendation}"
                        )

                        # Find option details from category data
                        option_data = next(
                            (
                                opt
                                for opt in category["options"]
                                if opt["name"] == option_name
                            ),
                            None,
                        )
                        if option_data:
                            console.print(
                                f"     [dim]{option_data['description']}[/dim]"
                            )
                            console.print(
                                f"     [dim]Best for: {get_technology_use_case(option_name)}[/dim]"
                            )

                    # Add "Other" option
                    other_option_number = len(options) + 1
                    console.print(
                        f"  {other_option_number}. Other (describe your preference)"
                    )
                    console.print(
                        "     [dim]Tell us what technology you prefer if none of the above meet your needs[/dim]"
                    )

                    # Ask user to select an option
                    selection = Prompt.ask(
                        "Enter your choice",
                        choices=[
                            str(i) for i in range(1, len(options) + 2)
                        ],  # +2 to include the "Other" option
                        default=str(options.index(default_option) + 1),
                    )

                    selected_index = int(selection) - 1

                    # Handle "Other" option
                    if selected_index == len(options):  # User selected "Other"
                        console.print(
                            "\nPlease describe your preferred technology in plain English:"
                        )
                        user_description = pt_prompt()

                        console.print(
                            "\n[bold cyan]Processing your preference...[/bold cyan]"
                        )

                        # Generate a prompt to determine the appropriate technology based on user's description
                        tech_inference_prompt = f"""
                        The user is setting up a {project_type} project and wants to use a different {category['name']} than those offered.
                        
                        User's preference: "{user_description}"
                        
                        Based on this description, what specific technology name should be used? Respond with ONLY the name of the technology.
                        """

                        # Use the same AI provider to infer the technology
                        if "DeepSeek" in providers:
                            inference_provider = ai_integration.DeepSeekProvider()
                        else:
                            inference_provider = selected_provider

                        (
                            inference_success,
                            inferred_tech,
                        ) = inference_provider.generate_response(tech_inference_prompt)

                        if inference_success:
                            inferred_tech = inferred_tech.strip()
                            console.print(
                                f"[bold green]Based on your description, I'll use [/bold green][bold yellow]{inferred_tech}[/bold yellow]"
                            )

                            # Add this as a new option to the category
                            new_option = {
                                "name": inferred_tech,
                                "description": f"Custom selection: {user_description}",
                                "recommended": True,
                            }

                            # Add the new option
                            category["options"].append(new_option)

                            # Set selected_name to the inferred technology
                            selected_name = inferred_tech
                        else:
                            console.print(
                                "[bold red]Failed to process your custom selection. Using default option.[/bold red]"
                            )
                            selected_name = default_option
                    else:
                        selected_name = options[selected_index]

                    # Update recommended flag in the tech_data
                    for option in category["options"]:
                        option["recommended"] = option["name"] == selected_name

                console.print(
                    "\n[bold green]✅ Technology selections updated based on your preferences[/bold green]\n"
                )
            else:
                console.print(
                    "[bold cyan]Using AI-recommended technologies for your project.[/bold cyan]\n"
                )

            # Store technology selections in project_info
            project_info["tech_stack"] = tech_data

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        console.print(
            f"[bold yellow]Error parsing technology recommendations: {str(e)}[/bold yellow]"
        )

    return True, project_type


def get_category_impact(category_name: str) -> str:
    """
    Get a description of how a technology category impacts the project.

    Args:
        category_name: Name of the technology category

    Returns:
        A string describing the impact of this category
    """
    category_impacts = {
        "Backend Framework": "handle web requests, organize your code, and determine the project architecture",
        "Database": "store and retrieve data efficiently and securely",
        "Authentication": "secure user accounts and manage user sessions",
        "Email Processing": "parse and extract information from incoming emails",
        "Frontend": "create the user interface and determine the user experience",
        "Deployment": "host your application and make it available to users",
        "Testing Tools": "ensure your code works correctly and catch bugs early",
        "API Integration": "connect with external services and data sources",
        "Caching": "improve performance by storing frequently accessed data",
        "Message Queue": "handle asynchronous tasks and background processing",
    }

    return category_impacts.get(
        category_name, "influence a critical part of your application"
    )


def get_technology_use_case(tech_name: str) -> str:
    """
    Get a description of when a specific technology is most appropriate.

    Args:
        tech_name: Name of the technology

    Returns:
        A string describing the ideal use case
    """
    tech_use_cases = {
        # Backend Frameworks
        "FastAPI": "high-performance APIs with automatic documentation and modern Python features",
        "Flask": "lightweight applications with flexible routing and minimal constraints",
        "Django": "full-featured applications needing built-in admin, auth, and ORM",
        # Databases
        "PostgreSQL": "complex queries, relational data, and production applications requiring reliability",
        "MongoDB": "document-based storage with flexible schemas and JSON-like data structures",
        "SQLite": "development environments, small applications, or embedded databases",
        # Authentication
        "PyJWT": "token-based authentication with minimal dependencies",
        "Authlib": "OAuth and OpenID Connect integration with multiple providers",
        "Passlib": "password hashing and verification with configurable security",
        "Magic Link Authentication": "passwordless authentication via email links for improved user experience",
        # Email Processing
        "Email-Parser": "extracting structured data from email content with specialized parsing",
        "Imaplib + BeautifulSoup": "direct IMAP access with powerful HTML parsing capabilities",
        "Mailparser": "automated email processing with predefined templates and rules",
        # Frontend
        "Vue.js": "reactive applications with a gentler learning curve and excellent component system",
        "React": "complex UIs with a robust ecosystem and strong community support",
        "Alpine.js": "adding interactivity to existing HTML with minimal JavaScript",
        # Deployment
        "Docker + Nginx": "containerized deployments with scalability and production-grade web serving",
        "Gunicorn + Heroku": "quick deployment with managed infrastructure and easy scaling",
        "Uvicorn + DigitalOcean": "modern ASGI applications on customizable cloud VMs",
    }

    return tech_use_cases.get(
        tech_name, "projects that match its specific strengths and features"
    )


def manual_project_type_selection(
    project_types: Dict[str, Dict[str, str]]
) -> Tuple[bool, str]:
    """
    Allow manual selection of project type when AI is unavailable or not chosen.

    Args:
        project_types: Dictionary of available project types

    Returns:
        Tuple containing success status and selected project type
    """
    # Manual selection
    console.print("\n[bold]Please select a project type:[/bold]")

    project_type_list = []
    for type_key, type_info in project_types.items():
        project_type_list.append(f"{type_info['name']} - {type_info['description']}")

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
        console.print(f"[bold red]Error selecting project type:[/bold red] {str(e)}")
        return False, "Failed to select project type"


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
            "[bold magenta]Step 4: Creating Project Structure[/bold magenta]",
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
    console.print(f"\n[bold yellow]Creating {type_info['name']} project[/bold yellow]")

    # Display a small animated python in the terminal
    with console.status(
        "[bold green]Building your Python project 🐍[/bold green]", spinner="dots"
    ):
        console.print("\n[dim]Scaffolding directory structure...[/dim]")

        # Create project structure with technology stack information
        structure_success, message = core_project_builder.create_project_structure(
            project_name=project_info["project_name"],
            project_dir=project_info["project_dir"],
            project_type=project_type,
            with_ai=True,
            tech_stack=project_info.get("tech_stack", {}),
            **project_info,
        )

        if not structure_success:
            console.print(f"[bold red]Error:[/bold red] {message}")
            return False, message

        console.print("[dim]Finalizing project setup...[/dim]")

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

        # Ask for GitHub Copilot configuration
        setup_github_config = Confirm.ask(
            "\n[bold cyan]Would you like to set up GitHub Copilot configuration files?[/bold cyan]",
            default=True,
        )

        # If setting up GitHub config, explain the benefits
        if setup_github_config:
            console.print(
                "\n[italic]This will create a .github directory with configuration files for GitHub Copilot:[/italic]"
            )
            console.print("[dim]- Project-specific coding standards and guidelines")
            console.print("[dim]- Custom prompt templates for common development tasks")
            console.print("[dim]- VS Code settings for integration with GitHub Copilot")

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]Setting up Git repository...[/bold cyan]"),
            console=console,
        ) as progress:
            task = progress.add_task("Setting up", total=None)

            git_success, git_message = core_project_builder.initialize_git_repo(
                project_dir=project_info["project_dir"],
                project_name=project_info["project_name"],
                github_username=github_username,
                gitlab_username=gitlab_username,
                with_github_config=setup_github_config,
                project_description=project_info.get("project_description", ""),
                project_type=project_type,
                tech_stack=project_info.get("tech_stack", {}),
            )

            progress.update(task, completed=True)

        if git_success:
            console.print(f"\n[bold green]✅ {git_message}[/bold green]")

            if setup_github_config:
                console.print(
                    "\n[green]✓[/green] GitHub Copilot configuration files created in the .github directory"
                )
                console.print(
                    "[dim]To use these with VS Code, install the GitHub Copilot extension[/dim]"
                )

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
        Text("🐍 SETTING UP POETRY ENVIRONMENT", justify="center"),
        style="bold yellow",
        border_style="yellow",
        expand=True,
    )
    console.print(venv_panel)

    setup_venv = Confirm.ask(
        "[bold cyan]Do you want to set up Poetry and install dependencies?[/bold cyan]",
        default=True,
    )

    if setup_venv:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold yellow]Setting up Poetry environment...[/bold yellow]"),
            console=console,
        ) as progress:
            task = progress.add_task("Setting up", total=None)

            venv_success, venv_message = core_project_builder.setup_virtual_environment(
                project_info["project_dir"]
            )

            progress.update(task, completed=True)

        if venv_success:
            console.print(f"\n[bold green]✅ {venv_message}[/bold green]")
            console.print(
                "[dim]To activate the environment, run [bold]poetry shell[/bold] in your project directory[/dim]"
            )
        else:
            console.print(f"\n[bold red]❌ {venv_message}[/bold red]")
            console.print(
                "[yellow]Continuing without Poetry environment setup...[/yellow]"
            )
            console.print(
                "[dim]You can set it up later by running [bold]poetry install[/bold] in your project directory[/dim]"
            )

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

2. Activate the Poetry environment:
   ```bash
   poetry shell
   ```

3. Start coding in the `src/` directory

4. Add your tests in the `tests/` directory

5. Use Poetry to manage dependencies:
   ```bash
   # Add a production dependency
   poetry add <package-name>

   # Add a development dependency
   poetry add --group dev <package-name>
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
