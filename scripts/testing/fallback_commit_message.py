#!/usr/bin/env python3
"""
Simple fallback commit message generator.
"""

import sys


def main():
    """Simple function that just uses the prompt directly."""
    if len(sys.argv) < 2:
        print("Update project files")
        return

    prompt = sys.argv[1]

    # Simple keyword-based commit message generation
    if "fix" in prompt.lower():
        if "mypy" in prompt.lower() or "type" in prompt.lower():
            print("Fix type checking errors")
        elif "arm64" in prompt.lower():
            print("Fix ARM64 compatibility issues")
        else:
            print("Fix code issues")
    elif "add" in prompt.lower():
        if "arm64" in prompt.lower():
            print("Add ARM64 compatibility")
        else:
            print("Add new features")
    elif "update" in prompt.lower():
        print("Update project components")
    else:
        # Try to create a meaningful message from the prompt
        words = prompt.split()
        if len(words) > 3:
            print(f"{words[0].capitalize()} {' '.join(words[1:4])}")
        else:
            print(prompt[:50])


if __name__ == "__main__":
    main()
