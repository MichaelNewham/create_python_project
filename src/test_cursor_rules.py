"""Test module to demonstrate Cursor rule enforcement.

This module contains example functions and classes that follow our style guidelines.
"""

from collections.abc import Sequence


def calculate_sum(numbers: Sequence[float]) -> float:
    """Calculate the sum of a sequence of numbers.

    Args:
        numbers: A sequence of numbers to sum.

    Returns:
        float: The sum of all numbers in the sequence.
    """
    total = 0.0
    for num in numbers:
        total = total + num
    return total


class ExampleClass:
    """Example class demonstrating proper style and documentation."""

    def __init__(self, name: str) -> None:
        """Initialize the ExampleClass.

        Args:
            name: The name to store in the instance.
        """
        self.name = name

    def update_name(self, new_name: str) -> bool:
        """Update the stored name.

        Args:
            new_name: The new name to store.

        Returns:
            bool: True if the name was updated successfully.
        """
        self.name = new_name
        return True


def badly_formatted_function(param1, param2):
    """This is not a Google-style docstring
    Args are not properly formatted
    Returns nothing"""
    x = param1 + param2
    return x


class BadClassName:
    def __init__(self, name):
        self.name = name

    def badly_spaced_method(self, new_name):
        """Another non-Google style docstring"""
        self.name = new_name
        return True


# Violating import order and using relative imports
