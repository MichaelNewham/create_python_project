#!/usr/bin/env python3
"""
Comprehensive linting and code quality check script for create_python_project.

This script runs all code quality checks (black, ruff, mypy) on the codebase,
focusing on the core source code while excluding test files, documentation,
and generated files.

Run this script to ensure code quality before committing changes.
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


def run_command(cmd: list[str], description: str) -> tuple[bool, str]:
    """Run a command and return its success status and output."""
    print(f"\n{'='*80}")
    print(f"🔍 {description}")
    print(f"{'='*80}")
    print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)

        output = result.stdout
        if result.stderr:
            output += "\n" + result.stderr

        success = result.returncode == 0
        status = "✅ Passed" if success else "❌ Failed"
        print(f"{status} (exit code: {result.returncode})")

        return success, output
    except Exception as e:
        print(f"❌ Error executing command: {e}")
        return False, str(e)


def run_black(src_path: str, check_only: bool = False) -> tuple[bool, str]:
    """Run black formatter."""
    cmd = ["poetry", "run", "black"]
    if check_only:
        cmd.append("--check")
    cmd.append(src_path)

    return run_command(
        cmd, "Running Black (code formatter)" + (" [check only]" if check_only else "")
    )


def run_ruff(src_path: str, fix: bool = False) -> tuple[bool, str]:
    """Run ruff linter."""
    cmd = ["poetry", "run", "ruff", "check"]
    if fix:
        cmd.extend(
            ["--fix", "--unsafe-fixes"]
        )  # Enable unsafe fixes for more thorough linting
    cmd.extend(["--config=.config/ruff.toml", src_path])

    return run_command(cmd, "Running Ruff (linter)" + (" with auto-fix" if fix else ""))


def run_mypy(src_path: str) -> tuple[bool, str]:
    """Run mypy type checker."""
    cmd = ["poetry", "run", "mypy", "--config-file=.config/mypy.ini", src_path]

    return run_command(cmd, "Running Mypy (type checker)")


def main() -> int:
    """Main function for the linting script."""
    parser = argparse.ArgumentParser(description="Run linting and code quality checks")
    parser.add_argument(
        "--check", action="store_true", help="Check only, don't modify files"
    )
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    args = parser.parse_args()

    # Get project root
    project_root = get_project_root()
    os.chdir(project_root)

    # Define paths
    src_path = "src/create_python_project"

    # Initialize results
    all_passed = True
    results = []

    # Run black
    success, output = run_black(src_path, check_only=args.check)
    all_passed = all_passed and success
    results.append(("Black", success, output))

    # Run ruff
    success, output = run_ruff(src_path, fix=not args.check)
    all_passed = all_passed and success
    results.append(("Ruff", success, output))

    # Run mypy
    success, output = run_mypy(src_path)
    all_passed = all_passed and success
    results.append(("Mypy", success, output))

    # Print results summary
    print("\n" + "=" * 80)
    print("📊 RESULTS SUMMARY")
    print("=" * 80)

    for tool, success, output in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{tool:10} {status}")
        if not success or args.verbose:
            print(f"\nOutput:\n{output}")

    # Final result
    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 All code quality checks passed! 🎉")
    else:
        print("❌ Some code quality checks failed! See above for details.")
    print("=" * 80)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
