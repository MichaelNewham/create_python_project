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
    development_tools,
    script_templates,
    workspace_config,
)
from create_python_project.utils import logging as log_utils

# Initialize logger with file logging
logs_dir = os.path.join(os.path.dirname(__file__), "..", "..", "logs")
logger = log_utils.setup_logging(logs_dir)


# Global CLI state management
class CLIState:
    """Manages CLI state and formatting consistency."""

    def __init__(self):
        self.step_counter = 1
        self.verbose_mode = False
        self.section_icon = "🔧"
        self.success_icon = "✅"
        self.warning_icon = "⚠️"
        self.error_icon = "❌"
        self.ai_icon = "🤖"
        self.git_icon = "📚"
        self.poetry_icon = "📦"
        self.complete_icon = "🎉"

    def get_step_header(self, title: str, icon: str | None = None) -> str:
        """Get formatted step header."""
        icon = icon or self.section_icon
        header = (
            f"[bold magenta]Step {self.step_counter}: {title} {icon}[/bold magenta]"
        )
        self.step_counter += 1
        return header

    def print_separator(self, console: Console) -> None:
        """Print a visual separator between sections."""
        console.print("─" * 80, style="dim")

    def print_subsection(
        self, console: Console, title: str, description: str = ""
    ) -> None:
        """Print a subsection header."""
        console.print(f"\n[bold cyan]{title}[/bold cyan]")
        if description:
            console.print(f"[italic]{description}[/italic]")


# Initialize CLI state
cli_state = CLIState()

# Rich console
console = Console()


def get_project_info() -> tuple[bool, dict[str, Any]]:
    """
    Get project information from the user with enhanced CLI experience.

    Returns:
        Tuple containing success status and project info dictionary
    """
    # Clear terminal for fresh start
    console.clear()

    # Enhanced welcome banner with animations
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

    # Feature highlights with consistent styling
    console.print(
        "[yellow]⚡ AI-Powered ⚡ Best Practices ⚡ Fully Customizable ⚡[/yellow]",
        justify="center",
    )
    console.print("\n")
    cli_state.print_separator(console)

    welcome_text = (
        "[bold cyan]Welcome to Python Project Initializer![/bold cyan] "
        "Let's set up your new project with intelligent automation."
    )
    console.print(welcome_text)

    project_info = {}

    # Import the enhanced_input function from our CLI utilities
    from create_python_project.utils.cli import enhanced_input

    # Step 1: Project Name 🔧
    console.print(f"\n{cli_state.get_step_header('Project Name')}")
    cli_state.print_separator(console)

    with console.status("[bold cyan]Preparing project name input...[/bold cyan]"):
        # Brief delay for visual effect
        import time

        time.sleep(0.5)

    while True:
        project_name = enhanced_input("Please enter a name for your project")
        if project_name:
            break
        console.print(
            f"[bold red]{cli_state.error_icon} Error:[/bold red] Project name is required. Please enter a valid project name."
        )
    project_info["project_name"] = project_name

    # Step 2: Project Directory 🔧
    console.print(f"\n{cli_state.get_step_header('Project Directory')}")
    cli_state.print_separator(console)

    # Default to ~/Projects directory for better organization
    projects_dir = os.path.expanduser("~/Projects")
    os.makedirs(projects_dir, exist_ok=True)
    default_dir = os.path.join(
        projects_dir, project_name.replace(" ", "_").replace("-", "_").lower()
    )
    console.print(f"[dim]Default location: {default_dir}[/dim]")

    # Check if directory already exists
    if os.path.exists(default_dir):
        console.print(
            f"[yellow]{cli_state.warning_icon} Warning: Directory already exists![/yellow]"
        )
        if not Confirm.ask(
            "Do you want to overwrite the existing directory?", default=False
        ):
            console.print("[dim]Enter a different path:[/dim]")
            while True:
                user_input = input("> ")
                if user_input and not os.path.exists(user_input):
                    project_dir = user_input
                    break
                elif user_input and os.path.exists(user_input):
                    console.print(
                        f"[red]{cli_state.error_icon} That directory also exists. Try another:[/red]"
                    )
                else:
                    console.print(
                        f"[red]{cli_state.error_icon} Please enter a valid path:[/red]"
                    )
        else:
            project_dir = default_dir
    else:
        console.print("Press Enter to accept the default or type a new path:")
        user_input = input("> ")
        project_dir = user_input if user_input else default_dir
    project_info["project_dir"] = project_dir

    # Step 3: Author Information 🔧
    console.print(f"\n{cli_state.get_step_header('Author Information (Optional)')}")
    cli_state.print_separator(console)

    console.print(
        "[italic]Used for project metadata, Git configuration, and documentation.[/italic]"
    )

    # Add option to skip all author info
    skip_author = console.input(
        "[dim]Press 's' to skip author info entirely, or Enter to continue: [/dim]"
    )

    if skip_author.lower() == "s":
        project_info["author_name"] = ""
        project_info["author_email"] = ""
        console.print(
            f"[yellow]{cli_state.warning_icon} Skipped author information[/yellow]"
        )
    else:
        author_name = enhanced_input("Enter your name (optional, press Enter to skip)")
        project_info["author_name"] = author_name
        if author_name:
            author_email = enhanced_input(
                "Enter your email (optional, press Enter to skip)"
            )
            project_info["author_email"] = author_email
        else:
            project_info["author_email"] = ""

    console.print(
        f"\n[bold green]{cli_state.success_icon} Project information collected successfully![/bold green]"
    )
    return True, project_info


def determine_project_type(project_info: dict[str, Any]) -> tuple[bool, str]:
    """
    Determine the project type based on project description with enhanced UI.

    Args:
        project_info: Dictionary containing project information

    Returns:
        Tuple containing success status and project type
    """
    # Get available project types
    project_types = config.get_project_types()

    # Step 4: Project Context & Inspiration 🔧
    console.print(f"\n{cli_state.get_step_header('Project Context & Inspiration')}")
    cli_state.print_separator(console)

    console.print(
        "[italic]Help AI understand your vision by sharing context and inspiration.[/italic]"
    )

    # Three key contextual questions
    context_info = {}

    # Import the enhanced_input function from our CLI utilities
    from create_python_project.utils.cli import enhanced_input

    console.print("\n[bold cyan]1. What problem are you solving?[/bold cyan]")
    problem = enhanced_input("Describe the main problem or need your project addresses")
    context_info["problem"] = problem

    console.print("\n[bold cyan]2. Who will use this?[/bold cyan]")
    users = enhanced_input(
        "Who are the end users? (developers, consumers, businesses, systems, etc.)"
    )
    context_info["users"] = users

    console.print("\n[bold cyan]3. What inspired this project?[/bold cyan]")
    console.print(
        "[dim]Share websites, apps, or services you admire (URLs welcome):[/dim]"
    )
    inspiration = enhanced_input(
        "Examples, similar apps, or websites that inspired you"
    )
    context_info["inspiration"] = inspiration

    # Combine original description with context
    if not project_info.get("project_description"):
        project_info["project_description"] = problem
    else:
        project_info["project_description"] += f"\n\nContext: {problem}"

    project_info["context"] = context_info

    # Check AI providers availability with visual feedback
    with console.status("[bold cyan]Checking available AI providers...[/bold cyan]"):
        providers = ai_integration.get_available_ai_providers()
        import time

        time.sleep(1)  # Visual feedback

    if not providers:
        console.print(
            f"[bold yellow]{cli_state.warning_icon} No AI providers available. Please set up API keys in your environment variables.[/bold yellow]"
        )
        return manual_project_type_selection(project_types)

    # Step 5: AI Provider Selection 🤖
    console.print(
        f"\n{cli_state.get_step_header('AI Provider Selection', cli_state.ai_icon)}"
    )
    cli_state.print_separator(console)

    # Enhanced provider selection with better descriptions
    provider_order = ["DeepSeek", "Anthropic", "Perplexity", "OpenAI", "Gemini"]
    provider_descriptions = {
        "DeepSeek": f"{providers.get('DeepSeek', 'deepseek-reasoner')}: Advanced reasoning model designed for complex problem solving and multi-step analysis. Excels at breaking down complex scenarios step-by-step",
        "Anthropic": f"{providers.get('Anthropic', 'claude-sonnet-4-20250514')}: Latest Claude model with superior reasoning and comprehensive project analysis. Excellent for nuanced understanding and planning",
        "Perplexity": f"{providers.get('Perplexity', 'sonar')}: Research-focused model with real-time web access for current tech recommendations. Ideal for finding latest frameworks and best practices",
        "OpenAI": f"{providers.get('OpenAI', 'gpt-4o-mini')}: Fast, cost-effective model optimized for general tasks and rapid responses. Great balance of speed, capability, and reliability for most projects",
        "Gemini": f"{providers.get('Gemini', 'gemini-2.5-flash-preview-05-20')}: Google's latest model optimized for data projects and integration with Google services. Strong multimodal capabilities",
    }

    from rich.table import Table

    table = Table(
        show_header=True, header_style="bold magenta", title="🤖 Available AI Providers"
    )
    table.add_column("#", style="cyan", no_wrap=True, width=3)
    table.add_column("Provider", style="green", width=12)
    table.add_column("Model & Description", style="white")
    table.add_column("Best For", style="dim", width=25)

    ordered_providers = [
        (name, providers[name]) for name in provider_order if name in providers
    ]

    provider_specialties = {
        "DeepSeek": "Strategic planning, complex analysis",
        "Anthropic": "Detailed analysis, documentation",
        "Perplexity": "Research, tech recommendations",
        "OpenAI": "Quick prototyping, general setup",
        "Gemini": "Data science, ML projects, analytics",
    }

    for idx, (name, _) in enumerate(ordered_providers, 1):
        desc = provider_descriptions.get(name, "")
        specialty = provider_specialties.get(name, "General purpose")
        table.add_row(str(idx), name, desc, specialty)

    console.print(table)
    console.print(
        f"[dim]{cli_state.ai_icon} Choose the provider that best matches your project needs. Default is DeepSeek (1).[/dim]"
    )

    console.print("\n[bold yellow]AI Selection:[/bold yellow]")
    console.print("  [dim]• Press Enter or select 1-5 to use AI recommendations[/dim]")

    provider_success, selected_provider = ai_integration.select_ai_provider(
        dict(ordered_providers)
    )

    if not provider_success or not selected_provider:
        console.print(
            f"[bold yellow]{cli_state.warning_icon} Failed to select an AI provider. Using manual selection.[/bold yellow]"
        )
        return manual_project_type_selection(project_types)

    # Step 6: AI Analysis & Complete Project Design 🤖
    console.print(
        f"\n{cli_state.get_step_header('AI Analysis & Complete Project Design', cli_state.ai_icon)}"
    )
    cli_state.print_separator(console)

    # Use AI to get comprehensive analysis with enhanced progress display
    with Progress(
        SpinnerColumn(),
        TextColumn(
            f"[bold cyan]{cli_state.ai_icon} Analyzing your requirements and designing optimal solution...[/bold cyan]"
        ),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing", total=None)

        # Generate comprehensive analysis prompt
        prompt = ai_prompts.get_comprehensive_analysis_prompt(
            project_info["project_name"],
            project_info["project_description"],
            project_info.get("context", {}),
        )

        # Get AI response for comprehensive analysis
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
                f"[bold red]{cli_state.error_icon} Error getting AI analysis:[/bold red] {response}"
            )
            return manual_project_type_selection(project_types)

    # Parse the comprehensive JSON response
    try:
        import json
        import re

        # Handle empty or invalid responses
        if not response or response.strip() == "":
            console.print(
                f"[bold yellow]{cli_state.warning_icon} No analysis received from AI.[/bold yellow]"
            )
            return manual_project_type_selection(project_types)

        # Log the raw response for debugging (file only)
        logger.debug(f"Raw comprehensive analysis response: {response}")

        # Show formatted AI response to user
        console.print("\n[dim]🤖 AI Analysis Response:[/dim]")

        # Clean the response first - handle markdown-wrapped JSON
        cleaned_response = response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]  # Remove ```json
        if cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:]  # Remove ```
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]  # Remove trailing ```
        cleaned_response = cleaned_response.strip()

        # Display clean formatted JSON to user
        try:
            parsed_for_display = json.loads(cleaned_response)
            formatted_json = json.dumps(parsed_for_display, indent=2)

            # Show formatted JSON in a panel
            from rich.syntax import Syntax

            syntax = Syntax(formatted_json, "json", theme="monokai", line_numbers=False)
            console.print(
                Panel(syntax, title="🤖 AI Comprehensive Analysis", border_style="blue")
            )
        except json.JSONDecodeError:
            # Fallback: show raw response in a panel
            console.print(
                Panel(cleaned_response, title="🤖 AI Response", border_style="yellow")
            )

        # Parse the comprehensive analysis
        try:
            analysis_data = json.loads(cleaned_response)
            logger.debug("Successfully parsed comprehensive analysis JSON")
        except json.JSONDecodeError as e:
            # Try multiple regex patterns as fallback
            logger.debug(f"Direct JSON parsing failed: {e}, trying regex extraction")

            patterns = [
                r"(\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\})",  # Complex nested pattern
                r"\{[\s\S]*\}",  # Everything between first { and last }
            ]

            json_match = None
            for pattern in patterns:
                json_match = re.search(pattern, response, re.DOTALL)
                if json_match:
                    break

            if json_match:
                json_str = (
                    json_match.group(1)
                    if len(json_match.groups()) > 0
                    else json_match.group(0)
                )
                try:
                    analysis_data = json.loads(json_str)
                    logger.debug("Successfully parsed extracted JSON")
                except json.JSONDecodeError as e2:
                    logger.error(f"Extracted JSON still invalid: {e2}")
                    raise json.JSONDecodeError(
                        "Extracted JSON is malformed", "", 0
                    ) from None
            else:
                raise json.JSONDecodeError("No valid JSON found", "", 0) from None

        # Extract project type and information
        architecture = analysis_data.get("recommended_architecture", {})
        project_type = architecture.get("type", "basic")

        # Validate project type
        project_types = config.get_project_types()
        if project_type not in project_types:
            logger.warning(
                f"Unknown project type '{project_type}', defaulting to 'basic'"
            )
            project_type = "basic"

        # Store analysis results
        project_info["project_type"] = project_type
        project_info["tech_stack"] = analysis_data.get("technology_stack", {})
        project_info["architecture_analysis"] = analysis_data

        # Display comprehensive analysis results
        console.print(
            f"\n[bold green]{cli_state.success_icon} AI Analysis Complete![/bold green]"
        )

        # Display recommended solution architecture
        console.print("\n[bold cyan]🎯 Recommended Solution Architecture:[/bold cyan]")
        console.print(
            f"[green]{architecture.get('approach', 'Optimized solution for your needs')}[/green]"
        )
        console.print("\n[bold cyan]💡 Why this approach:[/bold cyan]")
        console.print(
            f"[italic]{architecture.get('reasoning', 'Best fit for your requirements')}[/italic]\n"
        )

        # Display project structure preview
        project_structure = analysis_data.get("project_structure", {})
        if project_structure:
            console.print("[bold cyan]🏗️ Project Structure:[/bold cyan]")
            console.print(
                f"[white]{project_structure.get('type', 'Optimized project structure')}[/white]"
            )

            key_features = project_structure.get("key_features", [])
            if key_features:
                console.print("\n[bold cyan]✨ Key Features:[/bold cyan]")
                for feature in key_features:
                    console.print(f"  • {feature}")

            user_experience = project_structure.get("user_experience")
            if user_experience:
                console.print("\n[bold cyan]👤 User Experience:[/bold cyan]")
                console.print(f"[italic]{user_experience}[/italic]")

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        logger.error(f"Error parsing comprehensive analysis: {str(e)}")
        console.print(
            f"[bold yellow]{cli_state.warning_icon} Error parsing AI analysis. Using manual selection.[/bold yellow]"
        )
        return manual_project_type_selection(project_types)

    # Step 7: Technology Stack Review 🔧
    console.print(f"\n{cli_state.get_step_header('Technology Stack Review')}")
    cli_state.print_separator(console)

    # Display technology stack from comprehensive analysis
    tech_stack = project_info.get("tech_stack", {})

    if tech_stack and "categories" in tech_stack:
        from rich.table import Table

        # Create table showing complete technology stack
        console.print("[bold cyan]🔧 Complete Technology Stack:[/bold cyan]")

        table = Table(
            show_header=True,
            header_style="bold magenta",
            title="🤖 AI-Recommended Technologies",
        )
        table.add_column("Component", style="cyan", no_wrap=True, width=15)
        table.add_column("Technology", style="green", width=15)
        table.add_column("Why Recommended", style="white", width=50)

        for category in tech_stack["categories"]:
            recommended = next(
                (o for o in category["options"] if o.get("recommended", False)),
                category["options"][0] if category["options"] else None,
            )
            if recommended:
                reasoning = recommended.get(
                    "reasoning",
                    recommended.get("description", "Optimal for your project"),
                )
                table.add_row(category["name"], recommended["name"], reasoning)

        console.print(table)

        # Display future flexibility if available
        architecture_analysis = project_info.get("architecture_analysis", {})
        future_flexibility = architecture_analysis.get("future_flexibility", {})

        if future_flexibility:
            expansion_options = future_flexibility.get("expansion_options", [])
            alternative_deployments = future_flexibility.get(
                "alternative_deployments", []
            )

            if expansion_options or alternative_deployments:
                console.print("\n[bold cyan]🚀 Future Flexibility:[/bold cyan]")

                if expansion_options:
                    console.print("[bold green]Expansion Options:[/bold green]")
                    for option in expansion_options:
                        console.print(f"  • {option}")

                if alternative_deployments:
                    console.print("[bold green]Alternative Deployments:[/bold green]")
                    for deployment in alternative_deployments:
                        console.print(f"  • {deployment}")

        # Enhanced technology selection options
        console.print("\n[bold cyan]Technology Selection Options:[/bold cyan]")
        console.print(
            "  [dim]• Press Enter to use this complete solution (recommended)[/dim]"
        )
        console.print(
            "  [dim]• Type 'alternatives' to see other architectural approaches[/dim]"
        )
        console.print("  [dim]• Type 'customize' to modify specific technologies[/dim]")

        user_choice = Prompt.ask(
            "", choices=["", "alternatives", "customize"], default=""
        )

        if user_choice == "alternatives":
            console.print("\n[bold cyan]Alternative Approaches:[/bold cyan]")
            console.print(
                "1. [cyan]Pure Desktop Application[/cyan] - Traditional GUI with PyQt/Tkinter"
            )
            console.print(
                "2. [cyan]Command-Line Tool[/cyan] - Terminal-based interface with rich output"
            )
            console.print(
                "3. [cyan]API-First Architecture[/cyan] - Backend service with multiple frontend options"
            )
            console.print(
                "4. [cyan]Hybrid Approach[/cyan] - Web app that can be packaged as desktop"
            )

            alt_choice = Prompt.ask(
                "Select alternative (or Enter to keep recommended)",
                choices=["", "1", "2", "3", "4"],
                default="",
            )

            if alt_choice:
                console.print(
                    "[yellow]Alternative approach noted. Proceeding with recommended solution for now.[/yellow]"
                )

        elif user_choice == "customize":
            # Simplified customization - just show key categories
            key_categories = [
                "Frontend",
                "Backend",
                "Database",
                "Frontend Technology",
                "Backend Framework",
            ]

            for category in tech_stack["categories"]:
                if any(key in category["name"] for key in key_categories):
                    console.print(
                        f"\n[bold magenta]Select {category['name']}:[/bold magenta]"
                    )

                    options = [option["name"] for option in category["options"]]
                    default_option = next(
                        (
                            option["name"]
                            for option in category["options"]
                            if option.get("recommended", False)
                        ),
                        options[0] if options else "Default",
                    )

                    for i, option_name in enumerate(options, 1):
                        is_recommended = option_name == default_option
                        marker = " ⭐ (recommended)" if is_recommended else ""
                        console.print(f"  {i}. {option_name}{marker}")

                    selection = Prompt.ask(
                        "Enter your choice",
                        choices=[str(i) for i in range(1, len(options) + 1)],
                        default=(
                            str(options.index(default_option) + 1)
                            if default_option in options
                            else "1"
                        ),
                    )

                    selected_name = options[int(selection) - 1]

                    # Update recommended flag
                    for option in category["options"]:
                        option["recommended"] = option["name"] == selected_name

            console.print(
                f"\n[bold green]{cli_state.success_icon} Technology selections updated![/bold green]"
            )

        else:
            console.print(
                f"[bold cyan]{cli_state.ai_icon} Using AI-recommended solution for your project.[/bold cyan]"
            )

    else:
        # Fallback if no tech stack provided
        console.print(
            f"[bold yellow]{cli_state.warning_icon} No technology stack provided in analysis. Using default configuration.[/bold yellow]"
        )
        tech_data = create_default_tech_stack(project_type)
        project_info["tech_stack"] = tech_data

        # Get project type info for logging
        project_types = config.get_project_types()
        type_info = project_types.get(project_type, {"name": project_type.capitalize()})

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
            # Enhanced session logging with better formatting
            console.print(
                f"[green]{cli_state.success_icon} Session log saved to:[/green] {session_md}"
            )
        except Exception as e:
            logger.warning(f"Failed to write session markdown or README summary: {e}")
            console.print(
                f"[yellow]{cli_state.warning_icon} Warning: Could not write session log to ai-docs. {e}[/yellow]"
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
    Create the project structure with enhanced visual feedback.

    Args:
        project_info: Dictionary containing project information
        project_type: Type of the project

    Returns:
        Tuple containing success status and message
    """
    # Step 8: Creating Project Structure 🔧
    console.print(f"\n{cli_state.get_step_header('Creating Project Structure')}")
    cli_state.print_separator(console)

    # Show selected project type with enhanced formatting
    project_types = config.get_project_types()
    type_info = project_types.get(project_type, {"name": project_type.capitalize()})
    console.print(
        f"\n[bold yellow]{cli_state.section_icon} Building {type_info['name']} project...[/bold yellow]"
    )

    # Enhanced project creation with detailed progress
    creation_steps = [
        "📁 Creating directory structure",
        "📄 Generating configuration files",
        "🔧 Setting up project templates",
        "📚 Creating documentation",
        "🧪 Setting up testing framework",
        "⚙️ Configuring development tools",
        "✨ Finalizing project setup",
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold green]Building your Python project...[/bold green]"),
        console=console,
    ) as progress:
        task = progress.add_task("Building", total=len(creation_steps))

        for step in creation_steps:
            console.print(f"[dim]{step}[/dim]")
            import time

            time.sleep(0.3)  # Visual feedback for each step
            progress.advance(task)

        # Create project structure with technology stack information
        tech_stack_from_info = project_info.get("tech_stack")
        tech_stack_dict: dict[str, Any] = {}

        # Make sure we have a valid dictionary
        if isinstance(tech_stack_from_info, dict):
            tech_stack_dict = tech_stack_from_info

        # Extract specific parameters to avoid duplicate keyword arguments
        project_name = project_info["project_name"]
        project_dir = project_info["project_dir"]

        # Generate package_name and add it to project_info
        package_name = project_name.replace("-", "_").replace(" ", "_").lower()
        project_info["package_name"] = package_name

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
            console.print(
                f"[bold red]{cli_state.error_icon} Error:[/bold red] {message}"
            )
            return False, message

    console.print(f"\n[bold green]{cli_state.success_icon} {message}[/bold green]")

    # Step 8.1: Workspace Configuration 📋
    console.print(f"\n{cli_state.get_step_header('Workspace Configuration', '📋')}")
    cli_state.print_separator(console)

    setup_workspace = Confirm.ask(
        "[bold cyan]📋 Do you want to create a VS Code workspace file?[/bold cyan]",
        default=True,
    )

    if setup_workspace:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]📋 Creating workspace configuration...[/bold cyan]"),
            console=console,
        ) as progress:
            task = progress.add_task("Creating workspace", total=None)

            (
                workspace_success,
                workspace_message,
            ) = workspace_config.create_workspace_file(
                project_info["project_dir"],
                project_info["project_name"],
                project_type,
                tech_stack_dict,
            )

            progress.update(task, completed=True)

        if workspace_success:
            console.print(
                f"\n[bold green]{cli_state.success_icon} {workspace_message}[/bold green]"
            )
        else:
            console.print(
                f"\n[bold red]{cli_state.error_icon} {workspace_message}[/bold red]"
            )

    # Step 8.2: Development Tools Setup 🛠️
    console.print(f"\n{cli_state.get_step_header('Development Tools Setup', '🛠️')}")
    cli_state.print_separator(console)

    setup_dev_tools = Confirm.ask(
        "[bold cyan]🛠️ Do you want to set up development tools (pre-commit, linting)?[/bold cyan]",
        default=True,
    )

    if setup_dev_tools:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]🛠️ Setting up development tools...[/bold cyan]"),
            console=console,
        ) as progress:
            task = progress.add_task("Setting up tools", total=None)

            (
                dev_tools_success,
                dev_tools_message,
            ) = development_tools.setup_development_tools(
                project_info["project_dir"], tech_stack_dict
            )

            progress.update(task, completed=True)

        if dev_tools_success:
            console.print(
                f"\n[bold green]{cli_state.success_icon} {dev_tools_message}[/bold green]"
            )
        else:
            console.print(
                f"\n[bold red]{cli_state.error_icon} {dev_tools_message}[/bold red]"
            )

    # Step 8.3: Automation Scripts 🤖
    console.print(f"\n{cli_state.get_step_header('Automation Scripts', '🤖')}")
    cli_state.print_separator(console)

    setup_scripts = Confirm.ask(
        "[bold cyan]🤖 Do you want to create automation scripts (commit workflow, testing)?[/bold cyan]",
        default=True,
    )

    if setup_scripts:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]🤖 Creating automation scripts...[/bold cyan]"),
            console=console,
        ) as progress:
            task = progress.add_task("Creating scripts", total=None)

            (
                scripts_success,
                scripts_message,
            ) = script_templates.create_automation_scripts(
                project_info["project_dir"],
                project_info["package_name"],
                project_info["project_name"],
                tech_stack_dict,
            )

            progress.update(task, completed=True)

        if scripts_success:
            console.print(
                f"\n[bold green]{cli_state.success_icon} {scripts_message}[/bold green]"
            )
        else:
            console.print(
                f"\n[bold red]{cli_state.error_icon} {scripts_message}[/bold red]"
            )

    # Step 9: Git Repository Setup 📚
    console.print(
        f"\n{cli_state.get_step_header('Git Repository Setup', cli_state.git_icon)}"
    )
    cli_state.print_separator(console)

    setup_git = Confirm.ask(
        f"[bold cyan]{cli_state.git_icon} Do you want to initialize a Git repository?[/bold cyan]",
        default=True,
    )

    if setup_git:
        # Enhanced remote repository setup
        cli_state.print_subsection(
            console,
            "🌐 Remote Repository Setup (Optional)",
            "Configure remotes for GitHub and GitLab integration",
        )

        # Import the enhanced_input function if not already imported
        from create_python_project.utils.cli import enhanced_input

        # Add option to skip remote setup entirely
        console.print("  [dim]• Press 's' to skip remote repository setup[/dim]")
        console.print("  [dim]• Press Enter to configure GitHub/GitLab remotes[/dim]")

        remote_choice = console.input("Skip remotes or configure? [s/Enter]: ")

        github_username = ""
        gitlab_username = ""

        if remote_choice.lower() != "s":
            github_username = enhanced_input(
                "Enter your GitHub username (optional, press Enter to skip)"
            )

            # Ask for GitLab username
            gitlab_username = enhanced_input(
                "Enter your GitLab username (optional, press Enter to skip)"
            )

        # Enhanced GitHub Copilot configuration
        setup_github_config = False
        if github_username:  # Only ask if GitHub username provided
            setup_github_config = Confirm.ask(
                f"\n[bold cyan]{cli_state.ai_icon} Would you like to set up GitHub Copilot configuration files?[/bold cyan]",
                default=True,
            )

            # If setting up GitHub config, explain the benefits with better formatting
            if setup_github_config:
                cli_state.print_subsection(
                    console,
                    "🤖 GitHub Copilot Integration",
                    "Enhanced AI-powered development experience",
                )
                console.print(
                    "[dim]  • Project-specific coding standards and guidelines[/dim]"
                )
                console.print(
                    "[dim]  • Custom prompt templates for common development tasks[/dim]"
                )
                console.print(
                    "[dim]  • VS Code settings for seamless Copilot integration[/dim]"
                )

        with Progress(
            SpinnerColumn(),
            TextColumn(
                f"[bold cyan]{cli_state.git_icon} Setting up Git repository...[/bold cyan]"
            ),
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
            console.print(
                f"\n[bold green]{cli_state.success_icon} {git_message}[/bold green]"
            )

            if setup_github_config:
                console.print(
                    f"\n[green]{cli_state.success_icon}[/green] GitHub Copilot configuration files created in the .github directory"
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
            console.print(
                f"\n[bold red]{cli_state.error_icon} {git_message}[/bold red]"
            )
            console.print(
                f"[yellow]{cli_state.warning_icon} Continuing without Git repository...[/yellow]"
            )

    # Step 10: Poetry Environment Setup 📦
    console.print(
        f"\n{cli_state.get_step_header('Poetry Environment Setup', cli_state.poetry_icon)}"
    )
    cli_state.print_separator(console)

    setup_venv = Confirm.ask(
        f"[bold cyan]{cli_state.poetry_icon} Do you want to set up Poetry and install dependencies?[/bold cyan]",
        default=True,
    )

    if setup_venv:
        with Progress(
            SpinnerColumn(),
            TextColumn(
                f"[bold yellow]{cli_state.poetry_icon} Setting up Poetry environment...[/bold yellow]"
            ),
            console=console,
        ) as progress:
            task = progress.add_task("Setting up", total=None)

            # Pass tech stack to enable dynamic installation
            tech_stack_for_install = project_info.get("tech_stack", {})
            venv_success, venv_message = core_project_builder.setup_virtual_environment(
                project_info["project_dir"], tech_stack_for_install
            )

            progress.update(task, completed=True)

        if venv_success:
            console.print(
                f"\n[bold green]{cli_state.success_icon} {venv_message}[/bold green]"
            )
            console.print(
                "[dim]To activate the environment, run [bold]poetry env activate[/bold] in your project directory[/dim]"
            )
        else:
            console.print(
                f"\n[bold red]{cli_state.error_icon} {venv_message}[/bold red]"
            )
            console.print(
                f"[yellow]{cli_state.warning_icon} Continuing without Poetry environment setup...[/yellow]"
            )
            console.print(
                "[dim]You can set it up later by running [bold]poetry install[/bold] in your project directory[/dim]"
            )

    # Step 11: MCP Configuration Setup 🤖
    console.print(
        f"\n{cli_state.get_step_header('MCP Configuration Setup', cli_state.ai_icon)}"
    )
    cli_state.print_separator(console)

    setup_mcp = Confirm.ask(
        f"[bold cyan]{cli_state.ai_icon} Do you want to configure MCP servers for your IDE?[/bold cyan]",
        default=True,
    )

    if setup_mcp:
        console.print(
            "[dim]MCP configuration templates have been created in .vscode/ and .cursor/ directories[/dim]"
        )
        console.print(
            "[dim]Edit the mcp.json files and add your API keys to the .env file[/dim]"
        )
        console.print(
            f"[green]{cli_state.success_icon} MCP configuration ready for customization[/green]"
        )

    return True, "Project created successfully"


def main() -> int:
    """Main entry point for the application with enhanced error handling."""

    try:
        # Clear the terminal completely at startup
        os.system("clear")

        # Enhanced startup message with animation
        with console.status(
            "[bold cyan]Initializing Python Project Creator...[/bold cyan]"
        ):
            import time

            time.sleep(1)

        print("🚀 Starting Python Project Initializer...")

        # Log available AI providers for debugging
        available_providers = ai_integration.get_available_ai_providers()
        logger.debug(f"Available AI providers: {available_providers}")

        # Enhanced flow control with better error messages
        success, project_info = get_project_info()
        if not success:
            console.print(
                f"\n[bold red]{cli_state.error_icon} Failed to get project information.[/bold red]"
            )
            return 1

        # Determine project type
        success, project_type = determine_project_type(project_info)
        if not success:
            console.print(
                f"\n[bold red]{cli_state.error_icon} Failed to determine project type.[/bold red]"
            )
            return 1

        # Create the project
        success, message = create_project(project_info, project_type)
        if not success:
            console.print(
                f"\n[bold red]{cli_state.error_icon} Failed to create project: {message}[/bold red]"
            )
            return 1

        # Final Step: Project Created Successfully! 🎉
        console.print(
            f"\n{cli_state.get_step_header('Project Created Successfully!', cli_state.complete_icon)}"
        )
        cli_state.print_separator(console)

        # Enhanced completion message with project summary
        console.print(
            f"\n[bold green]{cli_state.complete_icon} Your new Python project has been created![/bold green]"
        )
        console.print(f"  📁 [cyan]{project_info['project_dir']}[/cyan]")

        # Project summary panel with enhanced project type detection
        from rich.panel import Panel

        from create_python_project.utils.core_project_builder import detect_project_type

        # Use enhanced project type detection with description context
        enhanced_project_type = detect_project_type(
            project_info.get("tech_stack", {}),
            project_info.get("project_description", ""),
        )

        summary_content = f"""[bold]Project Summary:[/bold]
• [cyan]Name:[/cyan] {project_info["project_name"]}
• [cyan]Type:[/cyan] {enhanced_project_type}
• [cyan]Author:[/cyan] {project_info.get("author_name", "Not specified")}
• [cyan]Location:[/cyan] {project_info["project_dir"]}"""

        summary_panel = Panel(
            summary_content,
            title="🎯 Project Overview",
            title_align="left",
            border_style="green",
        )
        console.print(summary_panel)

        # Enhanced next steps with better formatting
        next_steps = f"""
## 🚀 Next steps:

1. **Navigate to your project directory:**
   ```bash
   cd {project_info["project_dir"]}
   ```

2. **Activate the Poetry environment:**
   ```bash
   poetry env use python
   ```

3. **Start coding in the `src/` directory**

4. **Add your tests in the `tests/` directory**

5. **Use Poetry to manage dependencies:**
   ```bash
   # Add a production dependency
   poetry add <package-name>

   # Add a development dependency
   poetry add --group dev <package-name>
   ```

6. **Additional helpful commands:**
   ```bash
   # Run tests
   poetry run pytest

   # Format code
   poetry run black src/

   # Type checking
   poetry run mypy src/
   ```
        """

        console.print(Markdown(next_steps))

        # Final success message with session information
        console.print(
            f"\n[bold green]{cli_state.complete_icon} Happy coding! Your project is ready for development.[/bold green]"
        )

        # Display generated files information
        console.print("\n[bold cyan]📄 Generated Documentation:[/bold cyan]")
        console.print(
            "  • Project session: [green]ai-docs/project_initialization_*.md[/green]"
        )
        console.print(
            "  • Setup logs: [green]logs/project_creation.log[/green] (if enabled)"
        )
        console.print("  • README: [green]README.md[/green] with tech stack summary")

        return 0

    except KeyboardInterrupt:
        console.print(
            f"\n\n[yellow]{cli_state.warning_icon} Operation cancelled by user.[/yellow]"
        )
        return 130
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        console.print(
            f"\n[bold red]{cli_state.error_icon} An error occurred:[/bold red] {str(e)}"
        )
        return 1


def create_default_tech_stack(project_type: str) -> dict[str, Any]:
    """
    Create minimal fallback tech stack when AI recommendations fail.

    Args:
        project_type: Type of the project (web, cli, etc.)

    Returns:
        Dictionary containing minimal generic tech stack
    """
    return {
        "categories": [
            {
                "name": "Testing Framework",
                "description": "Essential testing tools for code quality",
                "options": [
                    {
                        "name": "Pytest",
                        "description": "Modern Python testing framework with powerful features",
                        "recommended": True,
                    }
                ],
            }
        ],
        "analysis": [
            "AI recommendations unavailable - using minimal configuration",
            "Essential testing framework included for code quality",
            f"Consider manually adding {project_type}-specific dependencies",
            "Run the tool again for AI-curated tech stack recommendations",
        ],
    }


if __name__ == "__main__":
    sys.exit(main())
