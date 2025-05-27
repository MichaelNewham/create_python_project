#!/usr/bin/env python3
"""
Create Python Project - Main Application

This is the main entry point for the Create Python Project application.
It handles the CLI interface and orchestrates the project creation process.
"""

import os
import sys
from typing import Any

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv(override=True)
except ImportError:
    print(
        "Warning: python-dotenv not installed. Install it using 'poetry add python-dotenv' to load environment variables from .env files."
    )

# Rich formatting
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


# Step counter for CLI flow
STEP_COUNTER = 1

# Verbose mode flag (could be set via CLI arg or config in future)
VERBOSE_MODE = False

# Rich console
console = Console()


def get_project_info() -> tuple[bool, dict[str, Any]]:
    """
    Get project information from the user.

    Returns:
        Tuple containing success status and project info dictionary
    """
    # Clear any previous output that might be in the terminal
    console.clear()

    # Display welcome banner
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

    welcome_text = "[bold cyan]Welcome to Python Project Initializer![/bold cyan] Let's set up your new project."
    console.print(welcome_text)

    project_info = {}

    # Import the enhanced_input function from our CLI utilities
    from create_python_project.utils.cli import enhanced_input

    global STEP_COUNTER
    # Get project name
    console.print(f"\n[bold magenta]Step {STEP_COUNTER}: Project Name[/bold magenta]")
    STEP_COUNTER += 1
    while True:
        project_name = enhanced_input("Please enter a name for your project")
        if project_name:
            break
        console.print(
            "[bold red]Error:[/bold red] Project name is required. Please enter a valid project name."
        )
    project_info["project_name"] = project_name

    # Get project directory with improved prompt
    default_dir = os.path.join(
        os.getcwd(), project_name.replace(" ", "_").replace("-", "_").lower()
    )
    console.print(
        f"\n[bold magenta]Step {STEP_COUNTER}: Project Directory[/bold magenta]"
    )
    STEP_COUNTER += 1
    console.print(f"[dim]Default: {default_dir}[/dim]")
    console.print("Press Enter to accept the default or type a new path:")
    user_input = input("> ")
    project_dir = user_input if user_input else default_dir
    project_info["project_dir"] = project_dir

    # Author information - make it clearly optional
    console.print(
        f"\n[bold magenta]Step {STEP_COUNTER}: Author Information (optional)[/bold magenta]"
    )
    STEP_COUNTER += 1
    console.print(
        "[italic]Used for project metadata, Git configuration, and documentation.[/italic]"
    )
    author_name = enhanced_input("Enter your name (optional, press Enter to skip)")
    project_info["author_name"] = author_name
    if author_name:
        author_email = enhanced_input(
            "Enter your email (optional, press Enter to skip)"
        )
        project_info["author_email"] = author_email
    else:
        project_info["author_email"] = ""

    return True, project_info


def determine_project_type(project_info: dict[str, Any]) -> tuple[bool, str]:
    """
    Determine the project type based on project description.

    Args:
        project_info: Dictionary containing project information

    Returns:
        Tuple containing success status and project type
    """
    global STEP_COUNTER
    # Get available project types
    project_types = config.get_project_types()

    # Step 4: Project Description
    console.print(
        f"\n[bold magenta]Step {STEP_COUNTER}: Project Description[/bold magenta]"
    )
    STEP_COUNTER += 1

    if not project_info.get("project_description"):
        project_info["project_description"] = Prompt.ask(
            "Please describe your project (this helps with AI recommendations)"
        )

    # Step: AI Provider Selection
    providers = ai_integration.get_available_ai_providers()
    if not providers:
        console.print(
            "[bold yellow]No AI providers available. Please set up API keys in your environment variables.[/bold yellow]"
        )
        return manual_project_type_selection(project_types)

    # Step number and header
    console.print(
        f"\n[bold magenta]Step {STEP_COUNTER}: AI Provider Selection[/bold magenta]"
    )
    STEP_COUNTER += 1

    # Provider descriptions for user guidance
    # Reorder providers so DeepSeek is first, OpenAI is fourth
    provider_order = ["DeepSeek", "Anthropic", "Perplexity", "OpenAI", "Gemini"]
    provider_descriptions = {
        "DeepSeek": "DeepSeek Chat, strong for code and technical tasks.",
        "Anthropic": "Claude models, strong on reasoning and summarization.",
        "Perplexity": "Sonar model, good for research and Q&A.",
        "OpenAI": "Fast, general-purpose, good for most projects.",
        "Gemini": "Google's Gemini, good for data and integration with Google services.",
    }
    from rich.table import Table

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="cyan", no_wrap=True)
    table.add_column("Provider", style="green")
    table.add_column("Description", style="white")
    ordered_providers = [
        (name, providers[name]) for name in provider_order if name in providers
    ]
    for idx, (name, _) in enumerate(ordered_providers, 1):
        desc = provider_descriptions.get(name, "")
        table.add_row(str(idx), name, desc)
    console.print(table)
    console.print(
        "[dim]Choose the provider that best matches your needs. If unsure, select the default (1: DeepSeek).[/dim]"
    )

    # Remove any duplicate or legacy Step 2: AI Integration/Select an AI provider text output
    provider_success, selected_provider = ai_integration.select_ai_provider(
        dict(ordered_providers)
    )
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
    # Create a new dictionary specifically for tech_stack
    project_info["tech_stack"] = {}

    # Show AI analysis step (no bounding box)
    console.print(
        "\n[bold magenta]Step {STEP_COUNTER}: AI Analysis with {provider_name.upper()} ({model_name})[/bold magenta]"
    )
    STEP_COUNTER += 1

    # Display project type recommendation with more detailed description
    type_info = project_types.get(project_type, {"name": project_type.capitalize()})
    detailed_descriptions = {
        "basic": "Standard Python package with modular structure and clean organization.",
        "cli": "Command-line interface application with argument parsing and terminal interaction.",
        "web": "Browser-based application with HTML rendering and user interface components.",
        "api": "RESTful or GraphQL service with data endpoints and request validation.",
        "data": "Data analysis project with processing pipelines and visualization capabilities.",
        "ai": "Machine learning project with model training and inference components.",
        "gui": "Desktop application with interactive graphical user interface elements.",
    }
    detailed_description = detailed_descriptions.get(
        project_type,
        f"Project with {type_info.get('description', 'specialized functionality')}.",
    )
    console.print(
        f"\n[bold green]Recommended Project Type:[/bold green] {type_info['name']}"
    )
    console.print(f"[italic]{detailed_description} {explanation.strip()}[/italic]\n")

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

        # Try up to 2 more times with the same provider if successful but response
        # might not be valid JSON
        max_retries = 2
        retry_count = 0

        # Check if we have a successful response but it doesn't look like valid JSON
        if tech_success and not (
            tech_response.strip().startswith("{")
            and tech_response.strip().endswith("}")
        ):
            logger.debug("Response doesn't look like valid JSON, will retry")
            while retry_count < max_retries:
                retry_count += 1
                console.print(
                    f"[bold yellow]Response format may not be valid JSON. Retrying ({retry_count}/{max_retries})...[/bold yellow]",
                    end="\r",
                )
                # Add stronger emphasis on JSON format in the retry
                retry_prompt = (
                    tech_prompt
                    + "\n\nCRITICAL: Your response MUST be ONLY a valid JSON object with no additional text."
                )
                tech_success, retry_response = selected_provider.generate_response(
                    retry_prompt
                )
                if (
                    tech_success
                    and retry_response.strip().startswith("{")
                    and retry_response.strip().endswith("}")
                ):
                    tech_response = retry_response
                    logger.debug(
                        f"Retry {retry_count} successful, response looks like valid JSON"
                    )
                    break
                logger.debug(
                    f"Retry {retry_count} failed or response still doesn't look like valid JSON"
                )

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
        import re

        # Handle empty or invalid responses
        if not tech_response or tech_response.strip() == "":
            console.print(
                "[bold yellow]No technology stack recommendations received.[/bold yellow]"
            )
            # Create a default tech stack structure
            tech_data = create_default_tech_stack(project_type)
            project_info["tech_stack"] = tech_data
            return True, project_type

        # Log the raw response for debugging
        logger.debug(f"Raw technology stack response: {tech_response}")

        # First try direct JSON parsing
        try:
            tech_data = json.loads(tech_response)
            logger.debug("Successfully parsed JSON directly")
        except json.JSONDecodeError:
            # If direct parsing fails, try to extract JSON using regex
            logger.debug("Direct JSON parsing failed, trying regex extraction")

            # Try to extract JSON from the response (in case the AI included extra text)
            # This improved regex looks for the most complete JSON object in the response
            json_match = re.search(
                r"(\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\})", tech_response
            )

            if json_match:
                json_str = json_match.group(1)
                logger.debug(f"Extracted JSON using regex: {json_str[:100]}...")

                try:
                    tech_data = json.loads(json_str)
                    logger.debug("Successfully parsed extracted JSON")
                except json.JSONDecodeError as e:
                    logger.debug(f"JSON parsing error after extraction: {str(e)}")
                    console.print(
                        "[bold yellow]Invalid technology stack response format. Using default configuration.[/bold yellow]"
                    )
                    # Create a default tech stack structure
                    tech_data = create_default_tech_stack(project_type)
                    project_info["tech_stack"] = tech_data
                    return True, project_type
            else:
                # No JSON found in the response
                logger.debug("No JSON pattern found in the response")
                console.print(
                    "[bold yellow]Invalid technology stack response format. Using default configuration.[/bold yellow]"
                )
                # Create a default tech stack structure
                tech_data = create_default_tech_stack(project_type)
                project_info["tech_stack"] = tech_data
                return True, project_type

        # Display key project features identified by AI
        if "analysis" in tech_data and tech_data["analysis"]:
            console.print("[bold cyan]Key Project Features:[/bold cyan]")
            for feature in tech_data["analysis"]:
                console.print(f"- {feature}", style="cyan")
            console.print("")

        # Display technology categories and options
        if "categories" in tech_data and tech_data["categories"]:
            from rich.table import Table

            console.print("[bold yellow]Recommended Technology Stack:[/bold yellow]\n")
            if VERBOSE_MODE:
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Category", style="cyan", no_wrap=True)
                table.add_column("Option", style="green")
                table.add_column("Description", style="white")
                table.add_column("Best For", style="dim")
                for category in tech_data["categories"]:
                    for option in category["options"]:
                        is_recommended = option.get("recommended", False)
                        option_name = (
                            f"{option['name']} ⭐" if is_recommended else option["name"]
                        )
                        table.add_row(
                            category["name"],
                            option_name,
                            option["description"],
                            get_technology_use_case(option["name"]),
                        )
                console.print(table)
            else:
                for category in tech_data["categories"]:
                    # Only show the recommended option and a one-sentence explanation
                    recommended = next(
                        (o for o in category["options"] if o.get("recommended", False)),
                        None,
                    )
                    if recommended:
                        console.print(
                            f"- [bold cyan]{category['name']}:[/bold cyan] "
                            f"[green]{recommended['name']}[/green] — "
                            f"{recommended['description']} "
                            f"[dim](Best for: {get_technology_use_case(recommended['name'])})[/dim]"
                        )
            console.print("")

            # Allow user to customize technology selections
            console.print(
                "[bold cyan]Would you like to customize the technology selections? [yes/no] (no): [/bold cyan]",
                end="",
            )
            customize = Prompt.ask("", choices=["yes", "no"], default="no")

            if customize.lower() == "yes":
                for category in tech_data["categories"]:
                    console.print(
                        f"\n[bold magenta]Select {category['name']}:[/bold magenta]"
                    )
                    console.print(
                        f"[italic]This determines how your project will "
                        f"{get_category_impact(category['name'])}.[/italic]"
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
                        console.print("\n")
                        # Import the enhanced_input function if not already imported
                        from create_python_project.utils.cli import enhanced_input

                        user_description = enhanced_input(
                            "Please describe your preferred technology in plain English"
                        )

                        console.print(
                            "\n[bold cyan]Processing your preference...[/bold cyan]"
                        )

                        # Generate a prompt to determine the appropriate technology based on
                        # user's description
                        tech_inference_prompt = f"""
                        The user is setting up a {project_type} project and wants to use a different {category["name"]} than those offered.

                        User's preference: "{user_description}"

                        Based on this description, what specific technology name should be used? Respond with ONLY the name of the technology.
                        """

                        # Create a provider for inferring technology
                        from create_python_project.utils.ai_integration import (
                            AIProvider,
                            DeepSeekProvider,
                            OpenAIProvider,
                        )

                        # Initialize with a concrete implementation
                        inference_provider: AIProvider

                        if "DeepSeek" in providers:
                            # Create a DeepSeek provider
                            inference_provider = DeepSeekProvider()
                        elif selected_provider is not None:
                            # Clone the selected provider's properties
                            if isinstance(selected_provider, DeepSeekProvider):
                                inference_provider = DeepSeekProvider(
                                    api_key=selected_provider.api_key,
                                    model=selected_provider.model,
                                )
                            elif isinstance(selected_provider, OpenAIProvider):
                                inference_provider = OpenAIProvider(
                                    api_key=selected_provider.api_key,
                                    model=selected_provider.model,
                                )
                            else:
                                # Default to a concrete implementation
                                inference_provider = OpenAIProvider()

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

        # --- Write session to markdown in ai-docs/ ---
        try:
            import datetime

            ai_docs_dir = os.path.join(project_info["project_dir"], "ai-docs")
            os.makedirs(ai_docs_dir, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
            session_md = os.path.join(
                ai_docs_dir, f"project_initialization_{timestamp}.md"
            )
            with open(session_md, "w", encoding="utf-8") as f:
                f.write("# Project Initialization Session\n\n")
                f.write(f"**Project Name:** {project_info['project_name']}\n\n")
                f.write(f"**Project Directory:** {project_info['project_dir']}\n\n")
                f.write(
                    f"**Author:** {project_info.get('author_name', '')} {project_info.get('author_email', '')}\n\n"
                )
                f.write(f"**Project Type:** {type_info['name']}\n\n")
                f.write("## Key Features\n")
                for feature in tech_data.get("analysis", []):
                    f.write(f"- {feature}\n")
                f.write("\n## Recommended Technology Stack\n")
                for category in tech_data.get("categories", []):
                    recommended = next(
                        (o for o in category["options"] if o.get("recommended", False)),
                        None,
                    )
                    if recommended:
                        f.write(
                            f"- **{category['name']}**: {recommended['name']} — "
                            f"{recommended['description']} "
                            f"(Best for: {get_technology_use_case(recommended['name'])})\n"
                        )
            # --- Write summary to README.md ---
            readme_path = os.path.join(project_info["project_dir"], "README.md")
            with open(readme_path, "a", encoding="utf-8") as f:
                f.write("\n## Project Initialization Summary\n")
                f.write(f"- **Project Name:** {project_info['project_name']}\n")
                f.write(f"- **Project Type:** {type_info['name']}\n")
                f.write("- **Key Features:**\n")
                for feature in tech_data.get("analysis", []):
                    f.write(f"  - {feature}\n")
                f.write("- **Recommended Stack:**\n")
                for category in tech_data.get("categories", []):
                    recommended = next(
                        (o for o in category["options"] if o.get("recommended", False)),
                        None,
                    )
                    if recommended:
                        f.write(f"  - {category['name']}: {recommended['name']}\n")
            # Print the path to the session log for user reference
            console.print(f"[green]Session log saved to:[/green] {session_md}")
        except Exception as e:
            logger.warning(f"Failed to write session markdown or README summary: {e}")
            console.print(
                f"[yellow]Warning: Could not write session log to ai-docs. {e}[/yellow]"
            )

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
    project_types: dict[str, dict[str, str]],
) -> tuple[bool, str]:
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
    for _, type_info in project_types.items():
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


def create_project(project_info: dict[str, Any], project_type: str) -> tuple[bool, str]:
    """
    Create the project structure.

    Args:
        project_info: Dictionary containing project information
        project_type: Type of the project

    Returns:
        Tuple containing success status and message
    """
    # Step 7: Creating Project Structure (no bounding box, consistent formatting)
    console.print("\n[bold magenta]Step 7: Creating Project Structure[/bold magenta]")

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
        tech_stack_from_info = project_info.get("tech_stack")
        tech_stack_dict: dict[str, Any] = {}

        # Make sure we have a valid dictionary
        if isinstance(tech_stack_from_info, dict):
            tech_stack_dict = tech_stack_from_info

        # Extract specific parameters to avoid duplicate keyword arguments
        project_name = project_info["project_name"]
        project_dir = project_info["project_dir"]

        # Create a copy of project_info without project_name, project_dir,
        # project_type, and tech_stack
        extra_info = {
            k: v
            for k, v in project_info.items()
            if k not in ["project_name", "project_dir", "project_type", "tech_stack"]
        }

        structure_success, message = core_project_builder.create_project_structure(
            project_name=project_name,
            project_dir=project_dir,
            project_type=project_type,
            with_ai=True,
            tech_stack=tech_stack_dict,
            **extra_info,
        )

        if not structure_success:
            console.print(f"[bold red]Error:[/bold red] {message}")
            return False, message

        console.print("[dim]Finalizing project setup...[/dim]")

    console.print(f"\n[bold green]✅ {message}[/bold green]")

    # Step 8: Git Repository Setup (no bounding box, consistent formatting)
    console.print("\n[bold cyan]Step 8: Git Repository Setup[/bold cyan]")

    setup_git = Confirm.ask(
        "[bold cyan]Do you want to initialize a Git repository?[/bold cyan]",
        default=True,
    )

    if setup_git:
        # Ask for GitHub username
        console.print("\n[bold]Remote Repository Setup (optional)[/bold]")
        console.print("[italic]Configure remotes for GitHub and GitLab[/italic]")

        # Import the enhanced_input function if not already imported
        from create_python_project.utils.cli import enhanced_input

        github_username = enhanced_input(
            "Enter your GitHub username (optional, press Enter to skip)"
        )

        # Ask for GitLab username
        gitlab_username = enhanced_input(
            "Enter your GitLab username (optional, press Enter to skip)"
        )

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

            # Ensure we have a valid tech_stack dictionary
            git_tech_stack_from_info = project_info.get("tech_stack")
            git_tech_stack: dict[str, Any] = {}

            # Make sure we have a valid dictionary
            if isinstance(git_tech_stack_from_info, dict):
                git_tech_stack = git_tech_stack_from_info

            git_success, git_message = core_project_builder.initialize_git_repo(
                project_dir=project_info["project_dir"],
                project_name=project_info["project_name"],
                github_username=github_username,
                gitlab_username=gitlab_username,
                with_github_config=setup_github_config,
                project_description=project_info.get("project_description", ""),
                project_type=project_type,
                tech_stack=git_tech_stack,
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

    # Step 9: Poetry Environment Setup (no bounding box, consistent formatting)
    console.print("\n[bold yellow]Step 9: Poetry Environment Setup[/bold yellow]")

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

    global STEP_COUNTER
    STEP_COUNTER = 1
    try:
        # Clear the terminal completely at startup
        os.system("clear")

        # Add debug print statements
        print("Starting Python Project Initializer...")

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

        # Step 10: Project Created Successfully (no bounding box, consistent formatting)
        console.print(
            "\n[bold green]Step 10: Project Created Successfully! 🎉[/bold green]"
        )

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


def create_default_tech_stack(project_type: str) -> dict[str, Any]:
    """
    Create a default technology stack structure based on project type.

    Args:
        project_type: Type of the project (web, cli, etc.)

    Returns:
        Dictionary containing default technology stack
    """
    # Create a basic structure for the tech stack
    tech_stack: dict[str, Any] = {
        "categories": [],  # This will be a list of category dictionaries
        "analysis": [
            "Using default configuration",
            "Customized for your project type",
            "Based on industry best practices",
            "Optimized for developer productivity",
        ],
    }

    # Add categories based on project type
    if project_type == "web":
        tech_stack["categories"] = [
            {
                "name": "Backend Framework",
                "description": "The foundation of your web application",
                "options": [
                    {
                        "name": "Flask",
                        "description": "Lightweight and flexible web framework",
                        "recommended": True,
                    },
                    {
                        "name": "FastAPI",
                        "description": "Modern, high-performance web framework with automatic API documentation",
                        "recommended": False,
                    },
                ],
            },
            {
                "name": "Database",
                "description": "Storage solution for your application data",
                "options": [
                    {
                        "name": "SQLite",
                        "description": "Lightweight file-based database for development and small applications",
                        "recommended": True,
                    },
                    {
                        "name": "PostgreSQL",
                        "description": "Powerful open-source relational database",
                        "recommended": False,
                    },
                ],
            },
        ]
    elif project_type == "cli":
        tech_stack["categories"] = [
            {
                "name": "CLI Framework",
                "description": "Framework for building command-line interfaces",
                "options": [
                    {
                        "name": "Click",
                        "description": "Composable command-line interface toolkit",
                        "recommended": True,
                    },
                    {
                        "name": "Typer",
                        "description": "Modern CLI framework based on type hints",
                        "recommended": False,
                    },
                ],
            }
        ]
    elif project_type == "api":
        tech_stack["categories"] = [
            {
                "name": "API Framework",
                "description": "Framework for building APIs",
                "options": [
                    {
                        "name": "FastAPI",
                        "description": "Modern, high-performance API framework with automatic documentation",
                        "recommended": True,
                    },
                    {
                        "name": "Flask-RESTful",
                        "description": "Extension for Flask that adds support for quickly building REST APIs",
                        "recommended": False,
                    },
                ],
            },
            {
                "name": "Database",
                "description": "Storage solution for your application data",
                "options": [
                    {
                        "name": "PostgreSQL",
                        "description": "Powerful open-source relational database",
                        "recommended": True,
                    },
                    {
                        "name": "MongoDB",
                        "description": "NoSQL document database for flexible data models",
                        "recommended": False,
                    },
                ],
            },
        ]
    elif project_type == "data":
        tech_stack["categories"] = [
            {
                "name": "Data Processing",
                "description": "Libraries for data manipulation and analysis",
                "options": [
                    {
                        "name": "Pandas",
                        "description": "Data analysis and manipulation library",
                        "recommended": True,
                    },
                    {
                        "name": "NumPy",
                        "description": "Fundamental package for scientific computing",
                        "recommended": False,
                    },
                ],
            },
            {
                "name": "Visualization",
                "description": "Libraries for data visualization",
                "options": [
                    {
                        "name": "Matplotlib",
                        "description": "Comprehensive library for creating static, animated, and interactive visualizations",
                        "recommended": True,
                    },
                    {
                        "name": "Seaborn",
                        "description": "Statistical data visualization based on matplotlib",
                        "recommended": False,
                    },
                ],
            },
        ]
    elif project_type == "ai":
        tech_stack["categories"] = [
            {
                "name": "Machine Learning",
                "description": "Libraries for machine learning",
                "options": [
                    {
                        "name": "Scikit-learn",
                        "description": "Simple and efficient tools for data analysis and modeling",
                        "recommended": True,
                    },
                    {
                        "name": "TensorFlow",
                        "description": "End-to-end open source platform for machine learning",
                        "recommended": False,
                    },
                ],
            }
        ]
    else:  # basic or other types
        tech_stack["categories"] = [
            {
                "name": "Testing",
                "description": "Libraries for testing your code",
                "options": [
                    {
                        "name": "Pytest",
                        "description": "Simple and powerful testing framework",
                        "recommended": True,
                    },
                    {
                        "name": "Unittest",
                        "description": "Built-in Python testing framework",
                        "recommended": False,
                    },
                ],
            }
        ]

    # Add common categories for all project types
    tech_stack["categories"].append(
        {
            "name": "Testing",
            "description": "Libraries for testing your code",
            "options": [
                {
                    "name": "Pytest",
                    "description": "Simple and powerful testing framework",
                    "recommended": True,
                },
                {
                    "name": "Unittest",
                    "description": "Built-in Python testing framework",
                    "recommended": False,
                },
            ],
        }
    )

    return tech_stack


if __name__ == "__main__":
    sys.exit(main())
