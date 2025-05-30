#!/usr/bin/env python3
"""
Clean runner for the Create Python Project application.
This script ensures a clean terminal environment before launching the main application.
"""

import os
import platform
import subprocess
import sys
import time
from pathlib import Path


def clear_screen() -> None:
    """Clear the terminal screen in a cross-platform way."""
    if platform.system().lower() == "windows":
        os.system("cls")
    else:
        os.system("clear")


def find_poetry() -> str | None:
    """Find the poetry executable path."""
    try:
        return subprocess.check_output(["which", "poetry"]).decode().strip()
    except subprocess.CalledProcessError:
        # On Windows, try where instead of which
        if platform.system().lower() == "windows":
            try:
                return (
                    subprocess.check_output(["where", "poetry"])
                    .decode()
                    .splitlines()[0]
                    .strip()
                )
            except subprocess.CalledProcessError:
                return None
        return None


def get_clean_env() -> dict[str, str]:
    """Get a clean environment with necessary variables."""
    env = os.environ.copy()

    # Ensure proper encoding
    env["PYTHONIOENCODING"] = "utf-8"

    # Add poetry and local bin to PATH if not already there
    local_bin = str(Path.home() / ".local" / "bin")
    if local_bin not in env.get("PATH", ""):
        env["PATH"] = f"{local_bin}:{env.get('PATH', '')}"

    return env


def build_command(poetry_path: str) -> list[str]:
    """Build the command to run the main application."""
    return [
        poetry_path,
        "run",
        "python",
        "-m",
        "create_python_project.create_python_project",
    ]


def main() -> int:
    """Main entry point for the clean runner."""
    try:
        # Clear the terminal
        clear_screen()

        # Print a simple message
        print("Starting Python Project Initializer...\n")
        time.sleep(0.5)  # Short delay to ensure terminal is ready

        # Clear again to remove any activation messages
        clear_screen()

        # Get the path to the poetry executable
        poetry_path = find_poetry()
        if not poetry_path:
            print("❌ Error: Poetry not found. Please install poetry first.")
            print(
                "Visit https://python-poetry.org/docs/#installation for installation instructions."
            )
            return 1

        # Build the command and environment
        cmd = build_command(poetry_path)
        env = get_clean_env()

        # Use execvpe to replace the current process with the new one
        os.execvpe(cmd[0], cmd, env)

    except Exception as e:
        print(f"❌ Error: Failed to start the application: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
