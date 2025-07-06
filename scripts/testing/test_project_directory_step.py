#!/usr/bin/env python3
"""
Test script to demonstrate the new Project Directory step with remote option.
This shows how the step would appear to users.
"""

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from rich.console import Console
from rich.prompt import Confirm, Prompt

# Rich console
console = Console()


# Simulate CLI state
class CLIState:
    def __init__(self):
        self.step_counter = 2  # We're at step 2
        self.warning_icon = "⚠️"
        self.error_icon = "❌"
        self.success_icon = "✅"
        self.section_icon = "🔧"

    def get_step_header(self, title: str, icon: str | None = None) -> str:
        icon = icon or self.section_icon
        header = (
            f"[bold magenta]Step {self.step_counter}: {title} {icon}[/bold magenta]"
        )
        return header

    def print_separator(self, console: Console) -> None:
        console.print("─" * 80, style="dim")


cli_state = CLIState()


# Enhanced input function
def enhanced_input(prompt: str, default: str | None = None) -> str:
    if not prompt.endswith(":"):
        prompt = f"{prompt}:"
    if default is None:
        return input(f"{prompt} ")
    return input(f"{prompt} [default: {default}] ") or default


# Demo the new Step 2
def demo_project_directory_step():
    # Clear and show context
    console.clear()
    console.print("\n[bold cyan]DEMO: New Project Directory Step[/bold cyan]\n")
    console.print(
        "[dim]This demonstrates how Step 2 now looks with the remote option:[/dim]\n"
    )
    console.print("─" * 80, style="dim")

    # Simulate having already collected project name
    project_name = "my_awesome_project"
    console.print(f"[dim]Project Name (from Step 1): {project_name}[/dim]\n")

    # Step 2: Project Directory
    console.print(f"\n{cli_state.get_step_header('Project Directory')}")
    cli_state.print_separator(console)

    # NEW: Offer choice between local and remote directories
    console.print("[bold cyan]Choose project location:[/bold cyan]")
    console.print("  [cyan]1.[/cyan] Local directory (default)")
    console.print(
        "  [cyan]2.[/cyan] Remote directory (Raspberry Pi via Cloudflare tunnel)"
    )

    location_choice = Prompt.ask(
        "[bold cyan]Select location[/bold cyan]", choices=["1", "2"], default="1"
    )

    if location_choice == "1":
        # Local directory flow
        default_dir = f"~/Projects/{project_name}"
        console.print(f"\n[dim]Default local location: {default_dir}[/dim]")
        console.print("Press Enter to accept the default or type a new path:")
        user_input = input("> ")
        project_dir = user_input if user_input else default_dir

        console.print(
            f"\n[green]{cli_state.success_icon} Local directory selected:[/green] {project_dir}"
        )

    else:
        # Remote directory flow
        remote_path = f"/home/mail2mick/Projects/{project_name}"

        console.print("\n[bold cyan]Remote Directory Setup[/bold cyan]")
        console.print(
            "[dim]Remote host: manjarodell-to-pi (via Cloudflare tunnel)[/dim]"
        )
        console.print(f"[dim]Default remote location: {remote_path}[/dim]")

        use_default_remote = Confirm.ask("Use default remote path?", default=True)

        if not use_default_remote:
            custom_remote = enhanced_input(
                "Enter custom remote path (e.g., /home/mail2mick/custom/path)"
            )
            remote_path = custom_remote

        project_dir = f"sftp://mail2mick@manjarodell-to-pi:8850{remote_path}"

        console.print(
            f"\n[green]{cli_state.success_icon} Remote directory configured:[/green]"
        )
        console.print(f"  [cyan]Path:[/cyan] {remote_path}")
        console.print("  [cyan]Access:[/cyan] SSH via Cloudflare tunnel")
        console.print(
            "\n[dim]Note: Ensure your Cloudflare tunnel is active for remote operations.[/dim]"
        )

    # Summary
    console.print("\n" + "─" * 80, style="dim")
    console.print("\n[bold]Summary:[/bold]")
    console.print(f"Project will be created at: [cyan]{project_dir}[/cyan]")
    console.print(
        f"Is remote: [cyan]{'Yes' if location_choice == '2' else 'No'}[/cyan]"
    )


if __name__ == "__main__":
    demo_project_directory_step()
