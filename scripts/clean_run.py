#!/usr/bin/env python3
"""
Clean runner for the Create Python Project application.
This script ensures a clean terminal environment before launching the main application.
"""

import os
import subprocess
import sys
import time


def main():
    """Main entry point for the clean runner."""
    # Clear the terminal
    os.system("clear")

    # Print a simple message
    print("Starting Python Project Initializer...\n")
    time.sleep(0.5)  # Short delay to ensure terminal is ready

    # Clear again to remove any activation messages
    os.system("clear")

    # Get the path to the poetry executable
    poetry_path = subprocess.check_output(["which", "poetry"]).decode().strip()

    # Build the command to run the main application
    cmd = [
        poetry_path,
        "run",
        "python",
        "-m",
        "create_python_project.create_python_project",
    ]

    # Execute the command with a clean environment
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    # Use execvpe to replace the current process with the new one
    # This avoids showing the activation message
    os.execvpe(cmd[0], cmd, env)


if __name__ == "__main__":
    sys.exit(main())
