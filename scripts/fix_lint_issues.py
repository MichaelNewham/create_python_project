#!/usr/bin/env python
"""
Automatic Linting Fix Script for Python Projects.

This script automates the process of fixing common linting issues:
1. Code formatting with Black
2. Import sorting with isort
3. Removing unused imports with autoflake
4. Fixing common pylint issues
5. Checking types with mypy

Usage:
    python fix_lint_issues.py [--path PATH] [--all] [--verbose]

Options:
    --path PATH     Specify the path to fix (default: src/)
    --all           Fix all files, including tests
    --verbose       Show detailed output
"""

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class LintResult:
    """Container for linting results."""

    success: bool
    fixed_count: int
    error_count: int
    output: str


class LintFixer:
    """Class to handle running linters and fixing issues."""

    def __init__(
        self, path: str = "src/", include_tests: bool = False, verbose: bool = False
    ):
        """Initialize with the path to lint and fix.

        Args:
            path: Directory path to lint
            include_tests: Whether to include test files
            verbose: Whether to show detailed output
        """
        self.base_path = Path(path)
        self.include_tests = include_tests
        self.verbose = verbose
        self.log_file = Path("logs/pylint_fixes.log")
        self.ensure_log_dir()

        # Make sure required tools are installed
        self.required_tools = ["black", "isort", "autoflake", "pylint", "mypy"]
        self.check_requirements()

    def ensure_log_dir(self) -> None:
        """Ensure the logs directory exists."""
        log_dir = self.log_file.parent
        if not log_dir.exists():
            log_dir.mkdir(parents=True)

    def check_requirements(self) -> None:
        """Check if all required tools are installed."""
        missing = []
        for tool in self.required_tools:
            try:
                subprocess.run(
                    f"which {tool}",
                    shell=True,
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except subprocess.CalledProcessError:
                missing.append(tool)

        if missing:
            print(f"Missing required tools: {', '.join(missing)}")
            print("Please install with: poetry add --group dev " + " ".join(missing))
            sys.exit(1)

    def find_python_files(self) -> list[Path]:
        """Find all Python files in the specified path.

        Returns:
            List of Path objects pointing to Python files
        """
        python_files = []
        search_paths = [self.base_path]

        # Add tests directory if requested
        if self.include_tests and Path("tests").exists():
            search_paths.append(Path("tests"))

        for search_path in search_paths:
            if not search_path.exists():
                print(f"Warning: Path {search_path} does not exist")
                continue

            if search_path.is_file() and search_path.suffix == ".py":
                python_files.append(search_path)
            elif search_path.is_dir():
                python_files.extend(search_path.glob("**/*.py"))

        # Filter out __pycache__ files
        python_files = [
            f
            for f in python_files
            if "__pycache__" not in str(f) and ".tox" not in str(f)
        ]

        return python_files

    def run_black(self, files: list[Path]) -> LintResult:
        """Run Black code formatter on the files.

        Args:
            files: List of files to format

        Returns:
            LintResult with the results
        """
        print("Running Black formatter...")

        file_paths = [str(f) for f in files]

        # First check how many files would be reformatted
        check_cmd = ["black", "--check"] + file_paths
        check_result = subprocess.run(check_cmd, capture_output=True, text=True)

        # Count files that would be reformatted
        would_reformat = len(re.findall(r"would be reformatted", check_result.stderr))

        # Now actually run Black to format
        cmd = ["black"] + file_paths
        result = subprocess.run(cmd, capture_output=True, text=True)

        success = result.returncode == 0
        output = result.stdout + "\n" + result.stderr

        if success:
            print(f"✅ Black formatted {would_reformat} files")
        else:
            print("❌ Black formatter failed")
            if self.verbose:
                print(output)

        return LintResult(
            success=success,
            fixed_count=would_reformat,
            error_count=0 if success else 1,
            output=output,
        )

    def run_isort(self, files: list[Path]) -> LintResult:
        """Run isort to sort imports.

        Args:
            files: List of files to process

        Returns:
            LintResult with the results
        """
        print("Running isort to sort imports...")

        file_paths = [str(f) for f in files]

        # First check how many files would be modified
        check_cmd = ["isort", "--check-only", "--diff"] + file_paths
        check_result = subprocess.run(check_cmd, capture_output=True, text=True)

        # Count files that would be modified (look for "Fixing" in output)
        would_fix_count = len(re.findall(r"^--- ", check_result.stdout, re.MULTILINE))

        # Now actually run isort
        cmd = ["isort"] + file_paths
        result = subprocess.run(cmd, capture_output=True, text=True)

        success = result.returncode == 0
        output = result.stdout + "\n" + result.stderr

        if success:
            print(f"✅ isort fixed imports in {would_fix_count} files")
        else:
            print("❌ isort failed")
            if self.verbose:
                print(output)

        return LintResult(
            success=success,
            fixed_count=would_fix_count,
            error_count=0 if success else 1,
            output=output,
        )

    def run_autoflake(self, files: list[Path]) -> LintResult:
        """Run autoflake to remove unused imports.

        Args:
            files: List of files to process

        Returns:
            LintResult with the results
        """
        print("Running autoflake to remove unused imports...")

        fixed_count = 0
        error_count = 0
        output = ""

        for file_path in files:
            cmd = [
                "autoflake",
                "--in-place",
                "--remove-unused-variables",
                "--remove-all-unused-imports",
                str(file_path),
            ]

            # First check if there are changes needed
            check_cmd = cmd.copy()
            check_cmd.remove("--in-place")
            check_cmd.append("--check")

            check_result = subprocess.run(check_cmd, capture_output=True, text=True)

            needs_fixing = check_result.returncode == 1

            if needs_fixing:
                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode == 0:
                    fixed_count += 1
                    output += f"Fixed unused imports in {file_path}\n"
                else:
                    error_count += 1
                    output += f"Failed to fix unused imports in {file_path}\n"
                    output += result.stderr + "\n"

        if fixed_count > 0:
            print(f"✅ autoflake removed unused imports in {fixed_count} files")
        else:
            print("✅ No unused imports found")

        if error_count > 0:
            print(f"❌ autoflake failed on {error_count} files")
            if self.verbose:
                print(output)

        return LintResult(
            success=error_count == 0,
            fixed_count=fixed_count,
            error_count=error_count,
            output=output,
        )

    def run_pylint(self, files: list[Path]) -> LintResult:
        """Run pylint to check for issues.

        Args:
            files: List of files to check

        Returns:
            LintResult with the results
        """
        print("Running pylint to find issues...")

        file_paths = [str(f) for f in files]

        # First run pylint to get issues
        rcfile = ""
        if Path(".pylintrc").exists():
            rcfile = "--rcfile=.pylintrc"
        elif Path(".config/pylintrc").exists():
            rcfile = "--rcfile=.config/pylintrc"

        cmd = ["pylint"] + ([rcfile] if rcfile else []) + file_paths
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Extract score from output
        score_match = re.search(
            r"Your code has been rated at (\d+\.\d+)/10", result.stdout
        )
        score = float(score_match.group(1)) if score_match else 0.0

        # Extract warnings and errors
        issues = re.findall(
            r"^(.+):(\d+):(\d+): ([A-Z]\d+): (.+)$", result.stdout, re.MULTILINE
        )

        # Log issues to the log file
        with open(self.log_file, "a") as f:
            f.write(
                f"Pylint run at {os.path.basename(sys.argv[0])} {' '.join(sys.argv[1:])}\n"
            )
            f.write(f"Found {len(issues)} issues\n")
            f.write(f"Score: {score}/10\n\n")

            for file_path, line, col, code, message in issues:
                f.write(f"{file_path}:{line}:{col}: {code}: {message}\n")

            f.write("\n\n")

        # Try to fix some issues automatically
        fixed_count = self._fix_common_pylint_issues(files, issues)

        if score >= 9.0:
            print(f"✅ Pylint score: {score}/10.0")
        else:
            print(f"⚠️ Pylint score: {score}/10.0 (< 9.0)")

        print(f"✅ Fixed {fixed_count} pylint issues automatically")
        print(f"📝 Remaining issues logged to {self.log_file}")

        return LintResult(
            success=score >= 9.0,
            fixed_count=fixed_count,
            error_count=len(issues) - fixed_count,
            output=result.stdout,
        )

    def _fix_common_pylint_issues(
        self, files: list[Path], issues: list[tuple[str, str, str, str, str]]
    ) -> int:
        """Try to fix some common pylint issues automatically.

        Args:
            files: List of Path objects
            issues: List of (file_path, line, col, code, message) tuples

        Returns:
            Number of issues fixed
        """
        fixed_count = 0

        # Group issues by file
        file_issues: dict[str, list[tuple[str, str, str, str, str]]] = {}
        for file_path, line, col, code, message in issues:
            if file_path not in file_issues:
                file_issues[file_path] = []
            file_issues[file_path].append((file_path, line, col, code, message))

        # Set of fixable issues
        fixable_codes = {
            "C0303",  # Trailing whitespace
            "C0304",  # Final newline missing
            "C0305",  # Trailing newlines
            "C0321",  # Multiple statements on one line
            "W0404",  # Reimport
            "W0611",  # Unused import
            "W0612",  # Unused variable
            "W0702",  # No exception type(s) specified
        }

        # Process each file
        for file_path, file_issue_list in file_issues.items():
            # Filter for fixable issues
            fixable = [
                (int(line), int(col), code, message)
                for _, line, col, code, message in file_issue_list
                if code in fixable_codes
            ]

            if not fixable:
                continue

            # Read file content
            path = Path(file_path)
            try:
                with open(path, encoding="utf-8") as f:
                    content = f.read()

                # Apply fixes
                lines = content.splitlines()
                modified = False

                # First handle trailing whitespace, which is simple
                for i in range(len(lines)):
                    stripped = lines[i].rstrip()
                    if stripped != lines[i]:
                        lines[i] = stripped
                        modified = True
                        fixed_count += 1

                # Handle final newline
                if content and not content.endswith("\n"):
                    lines.append("")
                    modified = True
                    fixed_count += 1

                # Handle trailing newlines
                while len(lines) > 1 and lines[-1] == "" and lines[-2] == "":
                    lines.pop()
                    modified = True
                    fixed_count += 1

                # Re-join content
                new_content = "\n".join(lines)

                # Write back if modified
                if modified:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)

            except Exception as e:
                print(f"Error fixing {file_path}: {e}")

        return fixed_count

    def run_mypy(self, files: list[Path]) -> LintResult:
        """Run mypy to check types.

        Args:
            files: List of files to check

        Returns:
            LintResult with the results
        """
        print("Running mypy to check types...")

        file_paths = [str(f) for f in files]

        # Check if mypy.ini exists
        mypy_config = ""
        if Path("mypy.ini").exists():
            mypy_config = "--config-file=mypy.ini"
        elif Path(".config/mypy.ini").exists():
            mypy_config = "--config-file=.config/mypy.ini"

        cmd = ["mypy"] + ([mypy_config] if mypy_config else []) + file_paths
        result = subprocess.run(cmd, capture_output=True, text=True)

        success = result.returncode == 0
        output = result.stdout + "\n" + result.stderr

        # Count errors
        error_count = len(re.findall(r"^.+\.py:\d+: error: ", output, re.MULTILINE))

        if success:
            print("✅ mypy found no type errors")
        else:
            print(f"❌ mypy found {error_count} type errors")
            if self.verbose:
                print(output)

        return LintResult(
            success=success,
            fixed_count=0,  # mypy doesn't fix issues
            error_count=error_count,
            output=output,
        )

    def run_all(self) -> dict[str, LintResult]:
        """Run all linters and fixers.

        Returns:
            Dictionary of linter name to LintResult
        """
        files = self.find_python_files()
        print(f"Found {len(files)} Python files to fix")

        results = {}

        # Run linters in sequence
        results["black"] = self.run_black(files)
        results["isort"] = self.run_isort(files)
        results["autoflake"] = self.run_autoflake(files)
        results["pylint"] = self.run_pylint(files)
        results["mypy"] = self.run_mypy(files)

        return results

    def print_summary(self, results: dict[str, LintResult]) -> None:
        """Print a summary of all linting results.

        Args:
            results: Dictionary of linter name to LintResult
        """
        print("\n" + "=" * 60)
        print("LINTING SUMMARY")
        print("=" * 60)

        total_fixed = sum(result.fixed_count for result in results.values())
        total_errors = sum(result.error_count for result in results.values())

        print(f"Total issues fixed: {total_fixed}")
        print(f"Remaining issues: {total_errors}")
        print()

        for linter, result in results.items():
            status = "✅" if result.success else "❌"
            print(
                f"{status} {linter.ljust(10)}: Fixed {result.fixed_count} issues, {result.error_count} remaining"
            )

        print("\nRun with --verbose to see detailed output for failed linters")
        print("=" * 60)


def main() -> None:
    """Main function to parse args and run the fixer."""
    parser = argparse.ArgumentParser(description="Fix linting issues in Python code")
    parser.add_argument(
        "--path", "-p", default="src/", help="Path to lint and fix (default: src/)"
    )
    parser.add_argument("--all", "-a", action="store_true", help="Include test files")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show verbose output"
    )

    args = parser.parse_args()

    fixer = LintFixer(path=args.path, include_tests=args.all, verbose=args.verbose)

    results = fixer.run_all()
    fixer.print_summary(results)


if __name__ == "__main__":
    main()
