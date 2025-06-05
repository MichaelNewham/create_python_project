#!/usr/bin/env python3
"""
Test AI provider selection and API calls for Create Python Project workflow
"""

import os
import sys
from typing import Any

from dotenv import load_dotenv
from rich.console import Console

# Add the source directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from create_python_project.utils import ai_integration

# Load environment variables
load_dotenv(override=True)

console = Console()


def test_provider_selection_and_call(provider_number: int) -> dict[str, Any]:
    """Test a specific provider by number (1-5)."""

    # Get available providers
    providers = ai_integration.get_available_ai_providers()

    if not providers:
        return {
            "success": False,
            "error": "No AI providers available",
            "provider": None,
            "model": None,
        }

    # Convert to ordered list matching the UI
    provider_order = ["DeepSeek", "Anthropic", "Perplexity", "OpenAI", "Gemini"]
    ordered_providers = [
        (name, providers[name]) for name in provider_order if name in providers
    ]

    if provider_number < 1 or provider_number > len(ordered_providers):
        return {
            "success": False,
            "error": f"Invalid provider number {provider_number}",
            "provider": None,
            "model": None,
        }

    # Get selected provider info
    provider_name, model_name = ordered_providers[provider_number - 1]

    console.print(
        f"\n[bold cyan]Testing Provider {provider_number}: {provider_name}[/bold cyan]"
    )
    console.print(f"[cyan]Model from .env: {model_name}[/cyan]")

    # Create provider instance (same logic as select_ai_provider)
    selected_provider: ai_integration.AIProvider | None = None

    if provider_name == "OpenAI":
        selected_provider = ai_integration.OpenAIProvider(model=model_name)
    elif provider_name == "Anthropic":
        selected_provider = ai_integration.AnthropicProvider(model=model_name)
    elif provider_name == "Perplexity":
        selected_provider = ai_integration.PerplexityProvider(model=model_name)
    elif provider_name == "DeepSeek":
        selected_provider = ai_integration.DeepSeekProvider(model=model_name)
    elif provider_name == "Gemini":
        selected_provider = ai_integration.GeminiProvider(model=model_name)

    if not selected_provider:
        return {
            "success": False,
            "error": f"Could not create provider instance for {provider_name}",
            "provider": provider_name,
            "model": model_name,
        }

    console.print(
        f"[green]✓ Provider instance created with display name: {selected_provider.display_name}[/green]"
    )

    # Test API call with simple prompt
    test_prompt = (
        "Hello, please respond with exactly: 'Test successful for [provider name]'"
    )

    try:
        success, response = selected_provider.generate_response(test_prompt)

        return {
            "success": success,
            "error": None if success else response,
            "provider": provider_name,
            "model": model_name,
            "display_name": selected_provider.display_name,
            "response": response if success else None,
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Exception during API call: {str(e)}",
            "provider": provider_name,
            "model": model_name,
            "display_name": selected_provider.display_name,
            "response": None,
        }


def main():
    """Test all AI providers in the Create Python Project workflow."""

    console.clear()
    console.print("[bold blue]AI Provider Selection & API Call Test Suite[/bold blue]")
    console.print(
        "[italic]Testing each provider option (1-5) as they appear in Create Python Project[/italic]\n"
    )

    # Show current .env configuration
    console.print("[bold yellow]Current .env Configuration:[/bold yellow]")
    env_vars = {
        "OPENAI_MODEL": os.environ.get("OPENAI_MODEL", "Not set"),
        "ANTHROPIC_MODEL": os.environ.get("ANTHROPIC_MODEL", "Not set"),
        "PERPLEXITY_MODEL": os.environ.get("PERPLEXITY_MODEL", "Not set"),
        "DEEPSEEK_MODEL": os.environ.get("DEEPSEEK_MODEL", "Not set"),
        "GEMINI_MODEL": os.environ.get("GEMINI_MODEL", "Not set"),
    }

    for var, value in env_vars.items():
        console.print(f"  {var}: [cyan]{value}[/cyan]")

    console.print(f"\n{'='*60}")

    # Test each provider option
    results = []

    for i in range(1, 6):
        result = test_provider_selection_and_call(i)
        results.append(result)

        if result["success"]:
            console.print(
                f"[bold green]✅ Provider {i} ({result['provider']}) - SUCCESS[/bold green]"
            )
            console.print(
                f"[green]Response: {result['response'][:100]}{'...' if len(result['response']) > 100 else ''}[/green]"
            )
        else:
            console.print(
                f"[bold red]❌ Provider {i} ({result.get('provider', 'Unknown')}) - FAILED[/bold red]"
            )
            console.print(f"[red]Error: {result['error']}[/red]")

        console.print()

    # Summary
    console.print(f"{'='*60}")
    console.print("[bold blue]Test Results Summary:[/bold blue]")

    passed = sum(1 for r in results if r["success"])
    total = len(
        [r for r in results if r["provider"]]
    )  # Only count configured providers

    console.print(f"\n[bold]Providers tested: {total}[/bold]")
    console.print(f"[bold green]Passed: {passed}[/bold green]")
    console.print(f"[bold red]Failed: {total - passed}[/bold red]")

    # Detailed results table
    from rich.table import Table

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Option", style="cyan", width=6)
    table.add_column("Provider", style="green", width=10)
    table.add_column("Model", style="yellow", width=25)
    table.add_column("Status", style="white", width=10)

    for i, result in enumerate(results, 1):
        if result["provider"]:
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            status_style = "green" if result["success"] else "red"

            table.add_row(
                str(i),
                result["provider"],
                result["model"],
                f"[{status_style}]{status}[/{status_style}]",
            )

    console.print(f"\n{table}")

    if passed == total and total > 0:
        console.print(
            f"\n[bold green]🎉 All {total} configured AI providers are working correctly![/bold green]"
        )
    else:
        console.print(
            f"\n[bold yellow]⚠️ {total - passed} providers failed. Check API keys and network connectivity.[/bold yellow]"
        )

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
