#!/usr/bin/env python3
"""
Test script to verify AI providers work within Create Python Project workflow.
Tests DeepSeek, Perplexity, OpenAI, and Gemini providers.
"""

import os
import sys
from typing import Any

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add the source directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from create_python_project.utils import ai_integration, ai_prompts

# Load environment variables
load_dotenv(override=True)

console = Console()


def test_provider(
    provider_name: str, provider_instance: ai_integration.AIProvider
) -> dict[str, Any]:
    """Test a single AI provider with project-specific prompts."""
    results: dict[str, Any] = {
        "provider": provider_name,
        "model": provider_instance.display_name,
        "simple_test": False,
        "project_type_test": False,
        "tech_stack_test": False,
        "errors": [],
    }

    # Test 1: Simple connectivity test
    console.print(f"[cyan]Testing {provider_name} connectivity...[/cyan]")
    simple_prompt = "Respond with exactly these words: 'AI Provider Test Successful'"

    try:
        success, response = provider_instance.generate_response(simple_prompt)
        if success and "AI Provider Test Successful" in response:
            results["simple_test"] = True
            console.print(f"[green]✓ {provider_name} connectivity: PASS[/green]")
        else:
            results["errors"].append(f"Simple test failed: {response}")
            console.print(
                f"[red]✗ {provider_name} connectivity: FAIL - {response}[/red]"
            )
    except Exception as e:
        results["errors"].append(f"Simple test exception: {str(e)}")
        console.print(f"[red]✗ {provider_name} connectivity: ERROR - {str(e)}[/red]")

    # Test 2: Project type detection (real workflow prompt)
    console.print(f"[cyan]Testing {provider_name} project type detection...[/cyan]")
    project_prompt = ai_prompts.get_project_type_prompt(
        "test_web_app",
        "A web application for managing todo lists with user authentication",
        {
            "problem": "Managing daily tasks",
            "users": "Individual users",
            "inspiration": "Notion, Todoist",
        },
    )

    try:
        success, response = provider_instance.generate_response(project_prompt)
        if success and any(
            ptype in response.lower()
            for ptype in ["web", "api", "cli", "data", "ai", "gui"]
        ):
            results["project_type_test"] = True
            console.print(f"[green]✓ {provider_name} project type: PASS[/green]")
        else:
            results["errors"].append(f"Project type test failed: {response}")
            console.print(
                f"[red]✗ {provider_name} project type: FAIL - No valid project type detected[/red]"
            )
    except Exception as e:
        results["errors"].append(f"Project type test exception: {str(e)}")
        console.print(f"[red]✗ {provider_name} project type: ERROR - {str(e)}[/red]")

    # Test 3: Technology stack recommendations (real workflow prompt)
    console.print(f"[cyan]Testing {provider_name} tech stack recommendations...[/cyan]")
    tech_prompt = ai_prompts.get_technology_stack_prompt(
        "test_web_app",
        "A web application for managing todo lists with user authentication",
        "web",
    )

    try:
        success, response = provider_instance.generate_response(tech_prompt)
        if success and (
            "{" in response and "}" in response
        ):  # Basic JSON structure check
            results["tech_stack_test"] = True
            console.print(f"[green]✓ {provider_name} tech stack: PASS[/green]")
        else:
            results["errors"].append(f"Tech stack test failed: {response}")
            console.print(
                f"[red]✗ {provider_name} tech stack: FAIL - No JSON response detected[/red]"
            )
    except Exception as e:
        results["errors"].append(f"Tech stack test exception: {str(e)}")
        console.print(f"[red]✗ {provider_name} tech stack: ERROR - {str(e)}[/red]")

    return results


def main():
    """Main test function."""
    console.clear()

    # Display test banner
    banner = Panel(
        "[bold blue]AI Provider Workflow Test Suite[/bold blue]\n"
        "[italic]Testing DeepSeek, Perplexity, OpenAI, and Gemini within Create Python Project context[/italic]",
        style="blue",
        expand=True,
    )
    console.print(banner)

    # Get available providers
    providers = ai_integration.get_available_ai_providers()
    console.print(f"\n[bold]Available providers:[/bold] {', '.join(providers.keys())}")

    # Test target providers: DeepSeek, Perplexity, OpenAI, Gemini
    target_providers = ["DeepSeek", "Perplexity", "OpenAI", "Gemini"]
    test_results = []

    for provider_name in target_providers:
        if provider_name not in providers:
            console.print(
                f"[yellow]⚠ {provider_name}: Not configured (missing API key)[/yellow]"
            )
            continue

        console.print(f"\n[bold magenta]{'='*50}[/bold magenta]")
        console.print(f"[bold magenta]Testing {provider_name}[/bold magenta]")
        console.print(f"[bold magenta]{'='*50}[/bold magenta]")

        # Create provider instance
        model = providers[provider_name]
        provider_instance: ai_integration.AIProvider | None = None

        if provider_name == "DeepSeek":
            provider_instance = ai_integration.DeepSeekProvider(model=model)
        elif provider_name == "Perplexity":
            provider_instance = ai_integration.PerplexityProvider(model=model)
        elif provider_name == "OpenAI":
            provider_instance = ai_integration.OpenAIProvider(model=model)
        elif provider_name == "Gemini":
            provider_instance = ai_integration.GeminiProvider(model=model)

        if provider_instance:
            results = test_provider(provider_name, provider_instance)
            test_results.append(results)
        else:
            console.print(
                f"[red]✗ Failed to create {provider_name} provider instance[/red]"
            )

    # Display summary table
    console.print(f"\n[bold blue]{'='*60}[/bold blue]")
    console.print("[bold blue]Test Results Summary[/bold blue]")
    console.print(f"[bold blue]{'='*60}[/bold blue]")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Provider", style="cyan", no_wrap=True)
    table.add_column("Model", style="green")
    table.add_column("Connectivity", style="white", justify="center")
    table.add_column("Project Type", style="white", justify="center")
    table.add_column("Tech Stack", style="white", justify="center")
    table.add_column("Overall", style="white", justify="center")

    for result in test_results:
        connectivity = "✓" if result["simple_test"] else "✗"
        project_type = "✓" if result["project_type_test"] else "✗"
        tech_stack = "✓" if result["tech_stack_test"] else "✗"

        # Overall status
        all_passed = (
            result["simple_test"]
            and result["project_type_test"]
            and result["tech_stack_test"]
        )
        overall = "✓ PASS" if all_passed else "✗ FAIL"
        overall_style = "green" if all_passed else "red"

        table.add_row(
            result["provider"],
            result["model"],
            f"[green]{connectivity}[/green]"
            if connectivity == "✓"
            else f"[red]{connectivity}[/red]",
            f"[green]{project_type}[/green]"
            if project_type == "✓"
            else f"[red]{project_type}[/red]",
            f"[green]{tech_stack}[/green]"
            if tech_stack == "✓"
            else f"[red]{tech_stack}[/red]",
            f"[{overall_style}]{overall}[/{overall_style}]",
        )

    console.print(table)

    # Display any errors
    for result in test_results:
        if result["errors"]:
            console.print(f"\n[bold red]Errors for {result['provider']}:[/bold red]")
            for error in result["errors"]:
                console.print(f"  [red]• {error}[/red]")

    # Final summary
    passed_count = sum(
        1
        for r in test_results
        if r["simple_test"] and r["project_type_test"] and r["tech_stack_test"]
    )
    total_count = len(test_results)

    if passed_count == total_count and total_count > 0:
        console.print(
            f"\n[bold green]🎉 All {total_count} providers are working correctly![/bold green]"
        )
    elif passed_count > 0:
        console.print(
            f"\n[bold yellow]⚠ {passed_count}/{total_count} providers are working correctly[/bold yellow]"
        )
    else:
        console.print("\n[bold red]❌ No providers are working correctly[/bold red]")

    return 0 if passed_count == total_count else 1


if __name__ == "__main__":
    sys.exit(main())
