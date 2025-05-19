#!/usr/bin/env python3
"""
CLI Utilities Module

This module provides utilities for handling command-line interface operations.
It manages user input, displays, and interactive prompts.
"""


def enhanced_input(prompt: str, default: str | None = None) -> str:
    """
    Enhanced input function with support for default values and better editing.

    Args:
        prompt: The prompt to display
        default: Default value

    Returns:
        User input
    """
    if default is None:
        return input(prompt)

    # Note the space after the prompt and before the brackets
    return input(f"{prompt} [{default}]: ") or default


def select_from_list(
    items: list[str],
    prompt: str,
    allow_custom: bool = False,
) -> tuple[bool, str]:
    """
    Allow the user to select an item from a list.

    Args:
        items: List of items to select from
        prompt: The prompt to display
        allow_custom: Whether to allow custom input

    Returns:
        Tuple containing success status and selected item
    """
    if not items:
        return False, "No items to select from"

    # Display the items with numbers
    print("\n" + prompt)
    for i, item in enumerate(items, 1):
        print(f"{i}. {item}")

    if allow_custom:
        print(f"{len(items) + 1}. Enter custom value")

    # Get user selection
    try:
        selection = input("\nEnter your choice (number): ").strip()

        # Handle custom input
        if (
            allow_custom
            and selection.lower() == "custom"
            or (selection.isdigit() and int(selection) == len(items) + 1)
        ):
            custom_value = input("Enter custom value: ").strip()
            return True, custom_value

        # Handle numerical selection
        if selection.isdigit() and 1 <= int(selection) <= len(items):
            return True, items[int(selection) - 1]

        # Handle direct text input that matches an item
        if selection in items:
            return True, selection

        # If we get here with allow_custom, treat input as custom
        if allow_custom:
            return True, selection

        print("Invalid selection. Please try again.")
        return False, ""
    except Exception as e:
        print(f"Error: {e}")
        return False, ""


def confirm(prompt: str, default: bool = True) -> bool:
    """
    Ask for confirmation from the user.

    Args:
        prompt: The prompt to display
        default: Default value

    Returns:
        True if confirmed, False otherwise
    """
    default_text = " [Y/n]" if default else " [y/N]"
    response = input(f"{prompt}{default_text}: ").lower().strip()

    if not response:
        return default

    return response.startswith("y")
