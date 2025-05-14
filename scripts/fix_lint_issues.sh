#!/bin/bash
# Quick script to fix common linting issues in the codebase

set -e

# Get the project root directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "Fixing common linting issues..."

# Fix missing imports
echo "1. Adding missing imports..."
for file in $(grep -l "Any" --include="*.py" . | grep -v "__pycache__"); do
    if ! grep -q "from typing import Any" "$file"; then
        # Check if there's a typing import already
        if grep -q "from typing import" "$file"; then
            # Add Any to existing import
            sed -i 's/from typing import \(.*\)/from typing import Any, \1/g' "$file"
        else
            # Add new import
            sed -i '1s/^/from typing import Any\n\n/' "$file"
        fi
        echo "  Added Any import to $file"
    fi
done

# Run isort to fix import formatting
echo "2. Running isort to organize imports..."
poetry run isort src/ tests/

# Run black to fix code formatting and line length where possible
echo "3. Running black to format code..."
poetry run black src/ tests/

# Run isort to fix import formatting
echo "4. Running pre-commit to fix remaining issues..."
pre-commit run -a

echo "Fixed common issues. Please check pre-commit output for any remaining issues."
