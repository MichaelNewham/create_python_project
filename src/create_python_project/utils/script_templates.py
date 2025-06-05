#!/usr/bin/env python3
"""
Script Templates Module

Generates automation scripts for development workflow, including commit workflow,
deployment scripts, and project maintenance tools.
"""

import os
from typing import Any


def create_automation_scripts(
    project_dir: str, package_name: str, project_name: str, tech_stack: dict[str, Any]
) -> tuple[bool, str]:
    """
    Create all automation scripts for the project.

    Args:
        project_dir: Project directory path
        package_name: Python package name
        project_name: Human-readable project name
        tech_stack: AI-recommended technology stack

    Returns:
        Tuple of success status and message
    """
    try:
        scripts_dir = os.path.join(project_dir, "scripts")
        os.makedirs(scripts_dir, exist_ok=True)

        # Create commit workflow script
        _create_commit_workflow(scripts_dir, package_name)

        # Create clean run script
        _create_clean_run_script(scripts_dir, package_name)

        # Create deployment scripts
        _create_deployment_scripts(scripts_dir, package_name, tech_stack)

        # Create maintenance scripts
        _create_maintenance_scripts(scripts_dir, project_name)

        # Create testing scripts
        _create_testing_scripts(scripts_dir)

        # Create project-specific scripts
        _create_project_specific_scripts(scripts_dir, tech_stack, package_name)

        return True, "Automation scripts created successfully"

    except Exception as e:
        return False, f"Failed to create automation scripts: {str(e)}"


def _create_commit_workflow(scripts_dir: str, package_name: str):
    """Create enhanced commit workflow script."""

    commit_script = f'''#!/usr/bin/env python3
"""
AI-powered commit workflow for {package_name}.

This script provides an intelligent commit workflow with:
- Automated staging
- Pre-commit hook execution
- Smart commit message generation
- Push automation
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


class CommitWorkflow:
    """Manages the entire commit workflow."""

    def __init__(self):
        self.project_root = Path.cwd()

    def run_pre_commit_checks(self) -> bool:
        """Run all pre-commit checks and return success status."""
        print("🔍 Running pre-commit checks...")

        try:
            result = subprocess.run(
                ["poetry", "run", "pre-commit", "run", "--all-files"],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                print("✅ All pre-commit checks passed!")
                return True
            else:
                print("❌ Pre-commit checks failed!")
                print("\\nSTDOUT:")
                print(result.stdout)
                print("\\nSTDERR:")
                print(result.stderr)
                print("\\n💡 Fix the issues above and run the script again.")
                return False

        except subprocess.TimeoutExpired:
            print("⏰ Pre-commit checks timed out after 5 minutes")
            return False
        except FileNotFoundError:
            print("❌ Poetry not found. Make sure Poetry is installed.")
            return False

    def analyze_changes(self) -> Tuple[List[str], List[str], List[str]]:
        """Analyze git changes and categorize them."""
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-status"],
                capture_output=True,
                text=True
            )

            if not result.stdout:
                return [], [], []

            changes = result.stdout.strip().split("\\n")
            added, modified, deleted = [], [], []

            for change in changes:
                if not change:
                    continue

                status, file_path = change.split("\\t", 1)

                if status == "A":
                    added.append(file_path)
                elif status == "M":
                    modified.append(file_path)
                elif status == "D":
                    deleted.append(file_path)

            return added, modified, deleted

        except Exception:
            return [], [], []

    def generate_smart_commit_message(self) -> str:
        """Generate intelligent commit message based on changes."""
        added, modified, deleted = self.analyze_changes()

        if not any([added, modified, deleted]):
            return "chore: update project files"

        # Detect file types and patterns
        file_categories = {{
            "tests": [],
            "docs": [],
            "config": [],
            "core": [],
            "frontend": [],
            "backend": []
        }}

        all_files = added + modified + deleted

        for file_path in all_files:
            file_lower = file_path.lower()

            if "test" in file_lower or file_path.startswith("tests/"):
                file_categories["tests"].append(file_path)
            elif any(ext in file_lower for ext in [".md", ".rst", ".txt", "readme"]):
                file_categories["docs"].append(file_path)
            elif any(ext in file_lower for ext in [".yml", ".yaml", ".toml", ".ini", ".json", ".cfg"]):
                file_categories["config"].append(file_path)
            elif any(ext in file_lower for ext in [".js", ".jsx", ".ts", ".tsx", ".css", ".html"]):
                file_categories["frontend"].append(file_path)
            elif file_path.startswith("backend/") or "django" in file_lower or "flask" in file_lower:
                file_categories["backend"].append(file_path)
            else:
                file_categories["core"].append(file_path)

        # Generate message based on primary change type
        primary_category = max(file_categories.keys(), key=lambda k: len(file_categories[k]))

        if len(all_files) == 1:
            action = "add" if added else "update" if modified else "remove"
            return f"{{self._get_commit_type(primary_category)}}: {{action}} {{all_files[0]}}"

        # Multi-file commit message
        commit_type = self._get_commit_type(primary_category)

        if len(added) > len(modified) + len(deleted):
            return f"{{commit_type}}: add {{len(added)}} new files"
        elif len(modified) > len(added) + len(deleted):
            return f"{{commit_type}}: update {{len(modified)}} files"
        elif len(deleted) > 0:
            return f"{{commit_type}}: remove {{len(deleted)}} files and update {{len(modified)}}"
        else:
            return f"{{commit_type}}: update {{primary_category}} files"

    def _get_commit_type(self, category: str) -> str:
        """Get conventional commit type based on file category."""
        commit_types = {{
            "tests": "test",
            "docs": "docs",
            "config": "chore",
            "core": "feat",
            "frontend": "feat",
            "backend": "feat"
        }}
        return commit_types.get(category, "chore")

    def stage_changes(self) -> bool:
        """Stage all changes for commit."""
        print("📦 Staging all changes...")

        try:
            subprocess.run(["git", "add", "."], check=True)
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to stage changes")
            return False

    def check_for_changes(self) -> bool:
        """Check if there are staged changes to commit."""
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            capture_output=True
        )
        return result.returncode != 0  # Non-zero means there are changes

    def commit_changes(self, message: str) -> bool:
        """Commit staged changes with the given message."""
        try:
            subprocess.run(["git", "commit", "-m", message], check=True)
            print(f"✅ Changes committed: {{message}}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to commit changes: {{e}}")
            return False

    def push_changes(self) -> bool:
        """Push changes to remote repository."""
        try:
            # Check if there's a remote
            result = subprocess.run(
                ["git", "remote"],
                capture_output=True,
                text=True
            )

            if not result.stdout.strip():
                print("ℹ️  No remote repository configured")
                return True

            # Push to remote
            subprocess.run(["git", "push"], check=True)
            print("✅ Changes pushed to remote repository")
            return True

        except subprocess.CalledProcessError:
            print("❌ Failed to push changes to remote")
            return False

    def run(self):
        """Execute the complete commit workflow."""
        print("🚀 Starting commit workflow...")

        # Check if we're in a git repository
        if not Path(".git").exists():
            print("❌ Not in a git repository!")
            sys.exit(1)

        # Stage changes
        if not self.stage_changes():
            sys.exit(1)

        # Check for changes
        if not self.check_for_changes():
            print("ℹ️  No changes to commit")
            return

        # Run pre-commit checks
        if not self.run_pre_commit_checks():
            print("\\n💡 Fix the issues above and run the script again")
            sys.exit(1)

        # Generate commit message
        suggested_message = self.generate_smart_commit_message()
        print(f"\\n📝 Suggested commit message: {{suggested_message}}")

        # Allow user to edit message
        user_message = input("\\nPress Enter to use this message or type a new one: ").strip()
        final_message = user_message if user_message else suggested_message

        # Commit changes
        if not self.commit_changes(final_message):
            sys.exit(1)

        # Ask about pushing
        push_choice = input("\\nPush to remote? [Y/n]: ").lower().strip()
        if push_choice != 'n':
            self.push_changes()

        print("\\n🎉 Commit workflow completed successfully!")


if __name__ == "__main__":
    workflow = CommitWorkflow()
    workflow.run()
'''

    with open(os.path.join(scripts_dir, "commit_workflow.py"), "w") as f:
        f.write(commit_script)
    os.chmod(os.path.join(scripts_dir, "commit_workflow.py"), 0o755)


def _create_clean_run_script(scripts_dir: str, package_name: str):
    """Create clean run script for the application."""

    clean_run = f'''#!/usr/bin/env python3
"""
Clean run script for {package_name}.

This script provides a clean way to run the application with:
- Environment setup
- Clear terminal
- Error handling
- Development-friendly output
"""

import os
import sys
from pathlib import Path


def setup_environment():
    """Set up the development environment."""
    # Add src to Python path
    src_path = Path(__file__).parent.parent / "src"
    if src_path.exists():
        sys.path.insert(0, str(src_path))

    # Set environment variables for development
    os.environ.setdefault("ENVIRONMENT", "development")
    os.environ.setdefault("DEBUG", "true")


def clear_terminal():
    """Clear the terminal for a clean start."""
    os.system('clear' if os.name != 'nt' else 'cls')


def main():
    """Main execution function."""
    print(f"🚀 Starting {{package_name}}...")
    print("=" * 50)

    try:
        # Set up environment
        setup_environment()

        # Try to import and run the main module
        try:
            from {{package_name}} import main as app_main
            app_main()
        except ImportError:
            # Fallback: try to run as module
            import subprocess
            result = subprocess.run([
                sys.executable, "-m", "{{package_name}}"
            ], cwd=Path(__file__).parent.parent)
            sys.exit(result.returncode)

    except KeyboardInterrupt:
        print("\\n\\n⏹️  Application stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\\n❌ Error running application: {{{{e}}}}")
        print("\\n🔧 Troubleshooting:")
        print("  - Check that all dependencies are installed: poetry install")
        print("  - Ensure you're in the correct directory")
        print("  - Check logs for more details")
        sys.exit(1)


if __name__ == "__main__":
    clear_terminal()
    main()
'''

    with open(os.path.join(scripts_dir, "clean_run.py"), "w") as f:
        f.write(clean_run)
    os.chmod(os.path.join(scripts_dir, "clean_run.py"), 0o755)


def _create_deployment_scripts(
    scripts_dir: str, package_name: str, tech_stack: dict[str, Any]
):
    """Create deployment automation scripts."""

    deploy_script = f'''#!/usr/bin/env python3
"""
Deployment script for {package_name}.

Handles building and deploying the application to various environments.
"""

import subprocess
import sys
import argparse
from pathlib import Path


def build_application():
    """Build the application for deployment."""
    print("🏗️  Building application...")

    try:
        # Install dependencies
        subprocess.run(["poetry", "install", "--without", "dev"], check=True)

        # Run tests
        subprocess.run(["poetry", "run", "pytest"], check=True)

        # Build package
        subprocess.run(["poetry", "build"], check=True)

        print("✅ Application built successfully")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {{e}}")
        return False


def deploy_to_production():
    """Deploy to production environment."""
    print("🚀 Deploying to production...")

    # Add production deployment logic here
    # This could include:
    # - Docker image building
    # - Cloud deployment
    # - Server configuration
    # - Database migrations

    print("✅ Deployment completed")


def deploy_to_staging():
    """Deploy to staging environment."""
    print("🧪 Deploying to staging...")

    # Add staging deployment logic here
    print("✅ Staging deployment completed")


def main():
    """Main deployment function."""
    parser = argparse.ArgumentParser(description=f"Deploy {{package_name}}")
    parser.add_argument(
        "environment",
        choices=["staging", "production"],
        help="Deployment environment"
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip the build step"
    )

    args = parser.parse_args()

    # Build application
    if not args.skip_build:
        if not build_application():
            sys.exit(1)

    # Deploy to specified environment
    if args.environment == "staging":
        deploy_to_staging()
    elif args.environment == "production":
        deploy_to_production()

    print("🎉 Deployment workflow completed!")


if __name__ == "__main__":
    main()
'''

    with open(os.path.join(scripts_dir, "deploy.py"), "w") as f:
        f.write(deploy_script)
    os.chmod(os.path.join(scripts_dir, "deploy.py"), 0o755)


def _create_maintenance_scripts(scripts_dir: str, project_name: str):
    """Create project maintenance scripts."""

    maintenance_script = f'''#!/usr/bin/env python3
"""
Maintenance script for {project_name}.

Handles routine maintenance tasks like:
- Dependency updates
- Cache clearing
- Log cleanup
- Database maintenance
"""

import subprocess
import sys
import shutil
from pathlib import Path
from datetime import datetime, timedelta


def update_dependencies():
    """Update project dependencies."""
    print("📦 Updating dependencies...")

    try:
        # Update Python dependencies
        subprocess.run(["poetry", "update"], check=True)

        # Update Node.js dependencies if package.json exists
        if Path("package.json").exists():
            subprocess.run(["npm", "update"], check=True)

        # Update pre-commit hooks
        subprocess.run(["poetry", "run", "pre-commit", "autoupdate"], check=True)

        print("✅ Dependencies updated successfully")

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to update dependencies: {{e}}")


def clean_cache():
    """Clean various cache directories."""
    print("🧹 Cleaning cache directories...")

    cache_dirs = [
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "__pycache__",
        "htmlcov",
        ".coverage",
        "node_modules/.cache" if Path("node_modules").exists() else None
    ]

    for cache_dir in cache_dirs:
        if cache_dir and Path(cache_dir).exists():
            try:
                if Path(cache_dir).is_file():
                    Path(cache_dir).unlink()
                else:
                    shutil.rmtree(cache_dir)
                print(f"  ✅ Cleaned {{{{cache_dir}}}}")
            except Exception as e:
                print(f"  ❌ Failed to clean {{{{cache_dir}}}}: {{{{e}}}}")


def clean_logs():
    """Clean old log files."""
    print("📋 Cleaning old log files...")

    logs_dir = Path("logs")
    if not logs_dir.exists():
        print("  ℹ️  No logs directory found")
        return

    # Remove log files older than 30 days
    cutoff_date = datetime.now() - timedelta(days=30)

    for log_file in logs_dir.glob("*.log"):
        try:
            file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
            if file_time < cutoff_date:
                log_file.unlink()
                print(f"  ✅ Removed old log file: {{{{log_file.name}}}}")
        except Exception as e:
            print(f"  ❌ Failed to remove {{{{log_file.name}}}}: {{{{e}}}}")


def generate_project_report():
    """Generate project health report."""
    print("📊 Generating project report...")

    report_lines = [
        f"# Project Report - {{{{datetime.now().strftime('%Y-%m-%d %H:%M')}}}}",
        "",
        "## Dependencies Status"
    ]

    try:
        # Check for outdated dependencies
        result = subprocess.run(
            ["poetry", "show", "--outdated"],
            capture_output=True,
            text=True
        )

        if result.stdout:
            report_lines.append("### Outdated Python packages:")
            report_lines.append("```")
            report_lines.append(result.stdout)
            report_lines.append("```")
        else:
            report_lines.append("✅ All Python packages are up to date")

    except Exception:
        report_lines.append("❌ Could not check Python package status")

    # Write report to file
    report_file = Path("maintenance_report.md")
    with open(report_file, "w") as f:
        f.write("\\n".join(report_lines))

    print(f"✅ Report generated: {{{{report_file}}}}")


def main():
    """Main maintenance function."""
    import argparse

    parser = argparse.ArgumentParser(description="Project maintenance tasks")
    parser.add_argument("--update", action="store_true", help="Update dependencies")
    parser.add_argument("--clean", action="store_true", help="Clean cache and logs")
    parser.add_argument("--report", action="store_true", help="Generate project report")
    parser.add_argument("--all", action="store_true", help="Run all maintenance tasks")

    args = parser.parse_args()

    if args.all or (not any([args.update, args.clean, args.report])):
        # Run all tasks if --all or no specific task specified
        update_dependencies()
        clean_cache()
        clean_logs()
        generate_project_report()
    else:
        if args.update:
            update_dependencies()
        if args.clean:
            clean_cache()
            clean_logs()
        if args.report:
            generate_project_report()

    print("🎉 Maintenance tasks completed!")


if __name__ == "__main__":
    main()
'''

    with open(os.path.join(scripts_dir, "maintenance.py"), "w") as f:
        f.write(maintenance_script)
    os.chmod(os.path.join(scripts_dir, "maintenance.py"), 0o755)


def _create_testing_scripts(scripts_dir: str):
    """Create testing automation scripts."""

    test_script = '''#!/usr/bin/env python3
"""
Enhanced testing script with multiple test modes and reporting.
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_unit_tests():
    """Run unit tests only."""
    print("🧪 Running unit tests...")

    try:
        subprocess.run([
            "poetry", "run", "pytest",
            "-m", "not integration and not e2e",
            "-v"
        ], check=True)
        print("✅ Unit tests passed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Unit tests failed")
        return False


def run_integration_tests():
    """Run integration tests."""
    print("🔧 Running integration tests...")

    try:
        subprocess.run([
            "poetry", "run", "pytest",
            "-m", "integration",
            "-v"
        ], check=True)
        print("✅ Integration tests passed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Integration tests failed")
        return False


def run_all_tests_with_coverage():
    """Run all tests with coverage reporting."""
    print("📊 Running all tests with coverage...")

    try:
        subprocess.run([
            "poetry", "run", "pytest",
            "--cov=src",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-fail-under=80",
            "-v"
        ], check=True)
        print("✅ All tests passed with coverage")
        return True
    except subprocess.CalledProcessError:
        print("❌ Tests failed or coverage too low")
        return False


def run_performance_tests():
    """Run performance benchmarks."""
    print("⚡ Running performance tests...")

    try:
        # Run pytest-benchmark if available
        subprocess.run([
            "poetry", "run", "pytest",
            "-m", "benchmark",
            "--benchmark-only",
            "-v"
        ], check=True)
        print("✅ Performance tests completed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Performance tests failed")
        return False


def main():
    """Main testing function."""
    parser = argparse.ArgumentParser(description="Run project tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--all", action="store_true", help="Run all test types")

    args = parser.parse_args()

    success = True

    if args.all:
        success &= run_unit_tests()
        success &= run_integration_tests()
        success &= run_all_tests_with_coverage()
        success &= run_performance_tests()
    else:
        if args.unit:
            success &= run_unit_tests()
        if args.integration:
            success &= run_integration_tests()
        if args.coverage:
            success &= run_all_tests_with_coverage()
        if args.performance:
            success &= run_performance_tests()

        # Default: run unit tests with coverage
        if not any([args.unit, args.integration, args.coverage, args.performance]):
            success &= run_all_tests_with_coverage()

    if success:
        print("\\n🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("\\n❌ Some tests failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
'''

    with open(os.path.join(scripts_dir, "test_runner.py"), "w") as f:
        f.write(test_script)
    os.chmod(os.path.join(scripts_dir, "test_runner.py"), 0o755)


def _create_project_specific_scripts(
    scripts_dir: str, tech_stack: dict[str, Any], package_name: str
):
    """Create scripts specific to the technology stack."""

    # Django-specific scripts
    if _extract_tech_choice(tech_stack, "Backend Framework") == "Django":
        django_script = f'''#!/usr/bin/env python3
"""
Django management script for {package_name}.
"""

import subprocess
import sys
import os
from pathlib import Path


def manage_django(command: str, *args):
    """Run Django management command."""
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        sys.exit(1)

    cmd = ["poetry", "run", "python", "manage.py", command] + list(args)
    subprocess.run(cmd, cwd=backend_dir)


def main():
    """Main Django management function."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/django_manage.py <command> [args...]")
        print("Common commands:")
        print("  runserver    - Start development server")
        print("  shell        - Open Django shell")
        print("  migrate      - Run migrations")
        print("  makemigrations - Create new migrations")
        print("  createsuperuser - Create admin user")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    manage_django(command, *args)


if __name__ == "__main__":
    main()
'''

        with open(os.path.join(scripts_dir, "django_manage.py"), "w") as f:
            f.write(django_script)
        os.chmod(os.path.join(scripts_dir, "django_manage.py"), 0o755)

    # Data science specific scripts
    if "data" in package_name.lower() or "Pandas" in str(tech_stack):
        data_script = '''#!/usr/bin/env python3
"""
Data processing automation script.
"""

import subprocess
import sys
from pathlib import Path


def start_jupyter():
    """Start Jupyter Lab."""
    print("🚀 Starting Jupyter Lab...")
    subprocess.run(["poetry", "run", "jupyter", "lab"])


def convert_notebooks():
    """Convert notebooks to Python scripts."""
    print("📝 Converting notebooks to scripts...")

    notebooks_dir = Path("notebooks")
    if not notebooks_dir.exists():
        print("❌ Notebooks directory not found")
        return

    for notebook in notebooks_dir.glob("*.ipynb"):
        print(f"Converting {notebook.name}...")
        subprocess.run([
            "poetry", "run", "jupyter", "nbconvert",
            "--to", "script",
            str(notebook)
        ])


def main():
    """Main data science function."""
    import argparse

    parser = argparse.ArgumentParser(description="Data science utilities")
    parser.add_argument("--jupyter", action="store_true", help="Start Jupyter Lab")
    parser.add_argument("--convert", action="store_true", help="Convert notebooks to scripts")

    args = parser.parse_args()

    if args.jupyter:
        start_jupyter()
    elif args.convert:
        convert_notebooks()
    else:
        print("No action specified. Use --help for options.")


if __name__ == "__main__":
    main()
'''

        with open(os.path.join(scripts_dir, "data_tools.py"), "w") as f:
            f.write(data_script)
        os.chmod(os.path.join(scripts_dir, "data_tools.py"), 0o755)


def _extract_tech_choice(tech_stack: dict[str, Any], category_name: str) -> str:
    """Extract the recommended technology for a given category."""
    if isinstance(tech_stack, dict) and "categories" in tech_stack:
        for category in tech_stack["categories"]:
            if category.get("name") == category_name:
                for option in category.get("options", []):
                    if option.get("recommended", False):
                        return str(option["name"])
    return ""
