#!/usr/bin/env python
"""
Script to fix specific linting issues identified in the create_python_project codebase.

This script targets the following linting issues:
1. F841 - Unused variable 'status' in create_python_project.py
2. F821 - Undefined name 'e', 'ext', 'column' in core_project_builder.py
3. E201/E202 - Whitespace around braces in ai_prompts.py and core_project_builder.py
4. E501 - Line too long in core_project_builder.py
5. Various mypy type errors

Usage:
    python fix_specific_lint_issues.py
"""

import os
import re
import sys


def fix_unused_status_variable(filepath: str) -> bool:
    """
    Fix the unused 'status' variable in create_python_project.py.

    This addresses error F841: Local variable 'status' is assigned to but never used.

    Args:
        filepath: Path to the file to fix

    Returns:
        bool: True if changes were made, False otherwise
    """
    with open(filepath, encoding="utf-8") as file:
        content = file.read()

    # Find and fix the console.status pattern with unused 'status' variable
    pattern = r'with console\.status\(\s*"[^"]+",\s*spinner="[^"]+"\s*\)\s*as status:'
    replacement = r'with console.status(\n        "[bold green]Building your Python project 🐍[/bold green]", spinner="dots"\n    ):'

    if re.search(pattern, content):
        new_content = re.sub(pattern, replacement, content)

        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(new_content)
            print(f"✅ Fixed unused 'status' variable in {filepath}")
            return True

    return False


def fix_undefined_names(filepath: str) -> bool:
    """
    Fix undefined names in core_project_builder.py.

    This addresses error F821: Undefined name 'e', 'ext', 'column'.

    Args:
        filepath: Path to the file to fix

    Returns:
        bool: True if changes were made, False otherwise
    """
    with open(filepath, encoding="utf-8") as file:
        content = file.read()

    made_changes = False

    # Fix 1: Undefined name 'e' in Exception handler
    pattern1 = r'except Exception as e:\s*\n\s*return f"Error: {str\(e\)}"'
    replacement1 = (
        r'except Exception as error:\n            return f"Error: {str(error)}"'
    )

    if re.search(pattern1, content):
        content = re.sub(pattern1, replacement1, content)
        made_changes = True

    # Fix 2: Undefined name 'ext' in load_data function
    pattern2 = r'raise ValueError\(f"Unsupported file extension: {ext}"\)'
    replacement2 = r'raise ValueError(f"Unsupported file extension: {file_extension}")'

    # Also fix the line that should define ext
    pattern2b = r"_, ext = os\.path\.splitext\(file_path\)"
    replacement2b = r"_, file_extension = os.path.splitext(file_path)"

    if re.search(pattern2, content):
        content = re.sub(pattern2, replacement2, content)
        content = re.sub(pattern2b, replacement2b, content)
        made_changes = True

    # Fix 3: Undefined name 'column' in visualize_data function
    pattern3 = r'plt\.title\(f"Histogram of {column}"\)'
    replacement3 = r'plt.title(f"Histogram of {column_name}")'

    pattern3b = r'plt\.title\(f"Value counts of {column}"\)'
    replacement3b = r'plt.title(f"Value counts of {column_name}")'

    # Also modify the function signature to rename the parameter
    pattern3c = r"def visualize_data\(df: pd\.DataFrame, column: str,"
    replacement3c = r"def visualize_data(df: pd.DataFrame, column_name: str,"

    # And fix any references to the column parameter in the body
    pattern3d = r"if pd\.api\.types\.is_numeric_dtype\(df\[column\]\):"
    replacement3d = r"if pd.api.types.is_numeric_dtype(df[column_name]):"

    pattern3e = r"df\[column\]\.hist\(\)"
    replacement3e = r"df[column_name].hist()"

    pattern3f = r"df\[column\]\.value_counts\(\)\.plot\(kind=\'bar\'\)"
    replacement3f = r"df[column_name].value_counts().plot(kind=\'bar\')"

    if re.search(pattern3, content) or re.search(pattern3b, content):
        content = re.sub(pattern3, replacement3, content)
        content = re.sub(pattern3b, replacement3b, content)
        content = re.sub(pattern3c, replacement3c, content)
        content = re.sub(pattern3d, replacement3d, content)
        content = re.sub(pattern3e, replacement3e, content)
        content = re.sub(pattern3f, replacement3f, content)
        made_changes = True

    if made_changes:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"✅ Fixed undefined names in {filepath}")

    return made_changes


def fix_whitespace_around_braces(filepath: str) -> bool:
    """
    Fix whitespace around braces in Python files.

    This addresses errors E201 (whitespace after '{') and E202 (whitespace before '}').

    Args:
        filepath: Path to the file to fix

    Returns:
        bool: True if changes were made, False otherwise
    """
    with open(filepath, encoding="utf-8") as file:
        content = file.read()

    # Fix E201: whitespace after '{'
    pattern1 = r"{\s+([^{}]*?)\s*}"

    # Fix E202: whitespace before '}'
    pattern2 = r"{([^{}]*?)\s+}"

    # Iterate to ensure all instances are fixed
    original_content = content
    iterations = 0
    max_iterations = 10  # Safety limit

    while iterations < max_iterations:
        # Apply the pattern replacements
        content_new = re.sub(pattern1, r"{\1}", content)
        content_new = re.sub(pattern2, r"{\1}", content_new)

        if content_new == content:
            break  # No more changes to make

        content = content_new
        iterations += 1

    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"✅ Fixed whitespace around braces in {filepath}")
        return True

    return False


def fix_long_lines(filepath: str, max_length: int = 150) -> bool:
    """
    Fix lines that exceed the maximum allowed length.

    This addresses error E501: line too long.

    Args:
        filepath: Path to the file to fix
        max_length: Maximum allowed line length

    Returns:
        bool: True if changes were made, False otherwise
    """
    with open(filepath, encoding="utf-8") as file:
        lines = file.readlines()

    made_changes = False
    new_lines = []

    for line in lines:
        if len(line.rstrip("\n")) > max_length:
            # Try to break the line at a reasonable point
            if "=" in line:
                # Split at the equals sign
                parts = line.split("=", 1)
                indent = len(parts[0]) - len(parts[0].lstrip())
                new_line = parts[0] + "=\\\n" + " " * (indent + 4) + parts[1].lstrip()
                new_lines.append(new_line)
                made_changes = True
            elif "," in line:
                # Split at the last comma before the max_length
                last_comma_idx = line[:max_length].rfind(",")
                if last_comma_idx > 0:
                    indent = len(line) - len(line.lstrip())
                    new_line = (
                        line[: last_comma_idx + 1]
                        + "\n"
                        + " " * indent
                        + line[last_comma_idx + 1 :].lstrip()
                    )
                    new_lines.append(new_line)
                    made_changes = True
                else:
                    new_lines.append(line)
            else:
                # Can't find a good break point, leave it for now
                new_lines.append(line)
        else:
            new_lines.append(line)

    if made_changes:
        with open(filepath, "w", encoding="utf-8") as file:
            file.writelines(new_lines)
        print(f"✅ Fixed long lines in {filepath}")

    return made_changes


def fix_mypy_issues(filepath: str) -> bool:
    """
    Fix common mypy type checking issues.

    Args:
        filepath: Path to the file to fix

    Returns:
        bool: True if changes were made, False otherwise
    """
    with open(filepath, encoding="utf-8") as file:
        content = file.read()

    made_changes = False

    # Fix 1: tech_stack parameter with None default but dict[Any, Any] type
    pattern1 = r"tech_stack: dict\[Any, Any\] = None"
    replacement1 = r"tech_stack: Optional[Dict[Any, Any]] = None"

    # Check if Optional is already imported, if not add it
    imported_optional = bool(re.search(r"from typing import [^)]*Optional", content))

    if re.search(pattern1, content):
        content = re.sub(pattern1, replacement1, content)
        made_changes = True

        if not imported_optional:
            # Add Optional to the typing imports
            pattern_typing = r"from typing import ([^)]*)"
            match = re.search(pattern_typing, content)
            if match:
                existing_imports = match.group(1)
                if "Optional" not in existing_imports:
                    if existing_imports.strip().endswith(","):
                        new_imports = existing_imports + " Optional,"
                    else:
                        new_imports = existing_imports + ", Optional,"
                    content = re.sub(
                        pattern_typing, f"from typing import {new_imports}", content
                    )
            else:
                # No existing typing import, add one with Optional
                content = re.sub(
                    r"import ([^\n]*)\n",
                    r"import \1\nfrom typing import Optional\n",
                    content,
                    count=1,
                )

    # Fix 2: Type checking for cases where an 'object' is used where a Dict is expected
    # This typically requires more context-specific fixes that are hard to automate

    if made_changes:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"✅ Fixed mypy issues in {filepath}")

    return made_changes


def main() -> int:
    """Main function."""
    # Define the files to fix
    create_python_project_path = os.path.join(
        "src", "create_python_project", "create_python_project.py"
    )
    core_project_builder_path = os.path.join(
        "src", "create_python_project", "utils", "core_project_builder.py"
    )
    ai_prompts_path = os.path.join(
        "src", "create_python_project", "utils", "ai_prompts.py"
    )

    # Store the current directory
    current_dir = os.getcwd()

    # Handle the case when running from different directories
    src_dir = None
    for path in [".", "..", "../.."]:
        test_path = os.path.join(current_dir, path, create_python_project_path)
        if os.path.exists(test_path):
            src_dir = os.path.join(current_dir, path)
            break

    if not src_dir:
        print(
            "❌ Could not find source files. Please run this script from the project root or scripts directory."
        )
        return 1

    # Update paths to be absolute
    create_python_project_path = os.path.join(src_dir, create_python_project_path)
    core_project_builder_path = os.path.join(src_dir, core_project_builder_path)
    ai_prompts_path = os.path.join(src_dir, ai_prompts_path)

    # Check if files exist
    for filepath in [
        create_python_project_path,
        core_project_builder_path,
        ai_prompts_path,
    ]:
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return 1

    # Fix specific issues
    fixes_made = []

    # Fix 1: Unused 'status' variable
    fixes_made.append(fix_unused_status_variable(create_python_project_path))

    # Fix 2: Undefined names in core_project_builder.py
    fixes_made.append(fix_undefined_names(core_project_builder_path))

    # Fix 3: Whitespace around braces
    fixes_made.append(fix_whitespace_around_braces(ai_prompts_path))
    fixes_made.append(fix_whitespace_around_braces(core_project_builder_path))

    # Fix 4: Long lines
    fixes_made.append(fix_long_lines(core_project_builder_path))

    # Fix 5: mypy issues
    fixes_made.append(fix_mypy_issues(core_project_builder_path))

    # Report results
    if any(fixes_made):
        print(
            "\n✅ Successfully fixed lint issues. Run Black and linting again to verify."
        )
        return 0
    else:
        print("\n⚠️ No changes were made. The issues may need manual fixing.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
