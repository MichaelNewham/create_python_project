#!/usr/bin/env python3
"""
Preference Tables Module

This module provides interactive preference table functionality for the enhanced context gathering system.
"""

import sys
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

console = Console()


class PreferenceTable:
    """Interactive preference table with navigation and comment support."""

    def __init__(self, title: str, categories: list[str], context: str = ""):
        self.title = title
        self.categories = categories
        self.context = context
        self.selections: dict[str, int] = {}  # category -> rating (1-5)
        self.current_row = 0
        self.rating_labels = [
            "Totally Against",
            "Not Appropriate",
            "Not Fussed",
            "Appropriate",
            "Highly Appropriate",
        ]
        self.rating_values = [1, 2, 3, 4, 5]

    def display_table(self) -> None:
        """Display the preference table with current selections."""
        console.clear()

        # Display context if provided
        if self.context:
            context_panel = Panel(
                Text(self.context, style="italic"),
                title="Context",
                title_align="left",
                border_style="blue",
            )
            console.print(context_panel)
            console.print()

        # Create the table
        table = Table(
            show_header=True,
            header_style="bold magenta",
            title=self.title,
            title_style="bold cyan",
        )

        # Add columns
        table.add_column("Option", style="white", width=30)
        table.add_column("Totally\nAgainst", style="red", width=8, justify="center")
        table.add_column("Not\nAppropriate", style="yellow", width=8, justify="center")
        table.add_column("Not\nFussed", style="dim", width=8, justify="center")
        table.add_column("Appropriate", style="green", width=8, justify="center")
        table.add_column(
            "Highly\nAppropriate", style="bold green", width=8, justify="center"
        )

        # Add rows
        for i, category in enumerate(self.categories):
            row_style = "bold" if i == self.current_row else ""
            selection = self.selections.get(category, 0)

            # Create rating cells
            rating_cells = []
            for rating in range(1, 6):
                if selection == rating:
                    rating_cells.append("[X]")
                else:
                    rating_cells.append("[ ]")

            # Add row with highlighting for current selection
            if i == self.current_row:
                table.add_row(f"→ {category}", *rating_cells, style=row_style)
            else:
                table.add_row(category, *rating_cells)

        console.print(table)
        console.print()

        # Display instructions
        instructions = """
[bold cyan]Navigation:[/bold cyan]
• ↑/↓ - Navigate between options
• ←/→ - Select rating (1-5)
• Enter - Continue to next section
• 'q' - Quit
        """
        console.print(Panel(instructions, title="Instructions", border_style="green"))

    def get_user_input(self) -> str:
        """Get user input for navigation."""
        try:
            # Use platform-specific input method
            if sys.platform == "win32":
                import msvcrt

                key = msvcrt.getch()
                if key == b"\xe0":  # Arrow key prefix on Windows
                    key = msvcrt.getch()
                    arrow_keys = {b"H": "up", b"P": "down", b"K": "left", b"M": "right"}
                    if key in arrow_keys:
                        return arrow_keys[key]
                elif key == b"\r":  # Enter
                    return "enter"
                elif key == b"q":
                    return "quit"
                return key.decode("utf-8", errors="ignore")
            else:
                # Unix-like systems
                import termios
                import tty

                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    char = sys.stdin.read(1)
                    if char == "\x1b":  # ESC sequence
                        char += sys.stdin.read(2)
                        arrow_keys = {
                            "\x1b[A": "up",
                            "\x1b[B": "down",
                            "\x1b[D": "left",
                            "\x1b[C": "right",
                        }
                        if char in arrow_keys:
                            return arrow_keys[char]
                    elif char == "\r" or char == "\n":
                        return "enter"
                    elif char == "q":
                        return "quit"
                    return char
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except (ImportError, Exception):
            # Fallback to simple input
            return (
                input("Enter command (up/down/left/right/enter/quit): ").strip().lower()
            )

    def navigate(self) -> None:
        """Handle navigation through the preference table."""
        while True:
            self.display_table()

            action = self.get_user_input()

            if action == "up":
                self.current_row = max(0, self.current_row - 1)
            elif action == "down":
                self.current_row = min(len(self.categories) - 1, self.current_row + 1)
            elif action == "left":
                current_category = self.categories[self.current_row]
                current_rating = self.selections.get(current_category, 3)
                self.selections[current_category] = max(1, current_rating - 1)
            elif action == "right":
                current_category = self.categories[self.current_row]
                current_rating = self.selections.get(current_category, 3)
                self.selections[current_category] = min(5, current_rating + 1)
            elif action == "enter":
                break
            elif action == "quit":
                sys.exit(0)
            elif action.isdigit():
                rating = int(action)
                if 1 <= rating <= 5:
                    current_category = self.categories[self.current_row]
                    self.selections[current_category] = rating

    def get_comment(self) -> str:
        """Get additional comments from the user."""
        console.print("\n[bold cyan]Additional Comments:[/bold cyan]")
        console.print(
            "[dim]Please provide any additional context or specific requirements:[/dim]"
        )

        comment = Prompt.ask(
            "[bold green]Your comments", default="", show_default=False
        )

        return comment

    def get_results(self) -> dict[str, Any]:
        """Get the results of the preference table interaction."""
        return {
            "selections": self.selections.copy(),
            "categories": self.categories.copy(),
            "rating_labels": self.rating_labels.copy(),
        }


def create_preference_table(
    title: str, categories: list[str], context: str = ""
) -> tuple[dict[str, Any], str]:
    """
    Create and run an interactive preference table.

    Args:
        title: Title of the preference table
        categories: List of categories to rate
        context: Context information to display

    Returns:
        Tuple of (preference results, user comments)
    """
    # Fallback to simple selection if terminal doesn't support interactive mode
    try:
        table = PreferenceTable(title, categories, context)
        table.navigate()
        comment = table.get_comment()
        return table.get_results(), comment
    except Exception:
        # Fallback to simple text-based selection
        console.print(f"\n[bold cyan]{title}[/bold cyan]")
        if context:
            console.print(f"[italic]{context}[/italic]")

        console.print("\nRate each option (1-5 scale):")
        console.print(
            "1 = Totally Against, 2 = Not Appropriate, 3 = Not Fussed, 4 = Appropriate, 5 = Highly Appropriate"
        )

        selections = {}
        for category in categories:
            while True:
                try:
                    rating = Prompt.ask(f"Rate '{category}' (1-5)", default="3")
                    rating_int = int(rating)
                    if 1 <= rating_int <= 5:
                        selections[category] = rating_int
                        break
                    else:
                        console.print(
                            "[red]Please enter a number between 1 and 5[/red]"
                        )
                except ValueError:
                    console.print("[red]Please enter a valid number[/red]")

        comment = Prompt.ask(
            "[bold green]Additional comments", default="", show_default=False
        )

        results = {
            "selections": selections,
            "categories": categories,
            "rating_labels": [
                "Totally Against",
                "Not Appropriate",
                "Not Fussed",
                "Appropriate",
                "Highly Appropriate",
            ],
        }

        return results, comment


def display_preference_summary(results: dict[str, Any], comment: str) -> None:
    """Display a summary of preference selections."""
    console.print("\n[bold green]✅ Preference Summary:[/bold green]")

    # Create summary table
    summary_table = Table(show_header=True, header_style="bold magenta")
    summary_table.add_column("Option", style="white")
    summary_table.add_column("Rating", style="cyan")
    summary_table.add_column("Description", style="dim")

    rating_labels = results["rating_labels"]

    for category in results["categories"]:
        rating = results["selections"].get(category, 3)
        rating_label = rating_labels[rating - 1]
        summary_table.add_row(category, str(rating), rating_label)

    console.print(summary_table)

    if comment:
        console.print(f"\n[bold green]Comments:[/bold green] {comment}")
