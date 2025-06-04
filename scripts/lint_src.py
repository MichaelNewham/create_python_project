#!/usr/bin/env python3
"""
Lint and format the source code of the create_python_project module.

This script runs code quality checks on the src/create_python_project directory,
applying best practices for Python code linting and formatting:
- Black for code formatting
- Ruff for linting and import sorting
- Mypy for type checking

The script focuses on the core source code while excluding tests, generated files,
and documentation.
"""

import argparse
import os
import subprocess
import sys


def get_project_root() -> str:
    """Get the project root directory."""
    # If script is in scripts/ directory, go up one level
    if os.path.basename(os.path.dirname(os.path.abspath(__file__))) == "scripts":
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.dirname(os.path.abspath(__file__))


def run_command(cmd, description, show_output=True) -> bool:
    """Run a command and print its result."""
    print(f"\n=== {description} ===")
    print(f"Running: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)
    success = result.returncode == 0

    if success:
        print("✅ Success!")
        if show_output and result.stdout.strip():
            print("\nOutput:")
            print(result.stdout)
    else:
        print("❌ Failed!")
        if result.stdout.strip():
            print("\nOutput:")
            print(result.stdout)
        if result.stderr.strip():
            print("\nErrors:")
            print(result.stderr)

    return success


def main():
    """Main function to lint the source code."""
    parser = argparse.ArgumentParser(description="Lint and format the source code")
    parser.add_argument(
        "--check", action="store_true", help="Only check code without modifying"
    )
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    parser.add_argument(
        "--src-only",
        action="store_true",
        help="Only check files in src/create_python_project (exclude tests)",
    )
    args = parser.parse_args()

    # Change to project root
    project_root = get_project_root()
    os.chdir(project_root)

    # Source directory to lint
    src_dir = "src/create_python_project"

    # Define test directory if needed
    test_dir = "tests" if not args.src_only else None

    # Track overall success
    all_success = True

    # 1. Black: Code Formatting
    black_args = ["--check"] if args.check else []
    black_cmd = ["poetry", "run", "black"] + black_args + [src_dir]
    if test_dir and not args.src_only:
        black_cmd.append(test_dir)

    black_success = run_command(
        black_cmd,
        "Running Black (code formatter)" + (" (check only)" if args.check else ""),
        args.verbose,
    )
    all_success = all_success and black_success

    # 2. Ruff: Linting and Import Sorting
    ruff_args = [] if args.check else ["--fix", "--unsafe-fixes"]
    ruff_cmd = (
        ["poetry", "run", "ruff", "check", "--config=.config/ruff.toml"]
        + ruff_args
        + [src_dir]
    )
    if test_dir and not args.src_only:
        ruff_cmd.append(test_dir)

    ruff_success = run_command(
        ruff_cmd,
        "Running Ruff (linter)" + (" (check only)" if args.check else " (with fixes)"),
        args.verbose,
    )
    all_success = all_success and ruff_success

    # 3. Mypy: Type Checking
    mypy_cmd = ["poetry", "run", "mypy", "--config-file=.config/mypy.ini", src_dir]

    mypy_success = run_command(mypy_cmd, "Running Mypy (type checker)", args.verbose)
    all_success = all_success and mypy_success

    # Summary
    print("\n=== Linting Summary ===")
    if all_success:
        print("✅ All checks passed successfully!")
    else:
        print("❌ Some checks failed:")
        if not black_success:
            print("  - Black formatting")
        if not ruff_success:
            print("  - Ruff linting")
        if not mypy_success:
            print("  - Mypy type checking")

        if args.check:
            print(
                "\nRun the script without --check to fix formatting issues automatically."
            )

    return 0 if all_success else 1


if __name__ == "__main__":
    sys.exit(main())
