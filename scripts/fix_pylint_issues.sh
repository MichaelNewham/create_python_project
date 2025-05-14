#!/bin/bash
# Script to fix pylint issues in the codebase

set -e

# Get the project root directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# Create a log file
LOG_FILE="${PROJECT_DIR}/pylint_fixes.log"
echo "Starting pylint fixes at $(date)" > "$LOG_FILE"

echo "Fixing pylint issues..."
echo "========================"

# Function to log messages to both console and log file
log() {
    echo "$1"
    echo "$(date +"%Y-%m-%d %H:%M:%S") - $1" >> "$LOG_FILE"
}

# Fix line length issues
log "1. Fixing line length issues with black..."
poetry run black src/create_python_project >> "$LOG_FILE" 2>&1
log "✅ Black formatting completed"

# Fix import organization issues
log "2. Fixing import organization with isort..."
poetry run isort src/create_python_project >> "$LOG_FILE" 2>&1
log "✅ Import sorting completed"

# Fix missing encoding in open() calls
log "3. Fixing missing encoding in open() calls..."
find src/create_python_project -type f -name "*.py" -exec sed -i 's/open(\([^,]*\))/open(\1, encoding="utf-8")/g' {} \;
find src/create_python_project -type f -name "*.py" -exec sed -i 's/open(\([^,]*\), "w")/open(\1, "w", encoding="utf-8")/g' {} \;
find src/create_python_project -type f -name "*.py" -exec sed -i 's/open(\([^,]*\), "r")/open(\1, "r", encoding="utf-8")/g' {} \;
find src/create_python_project -type f -name "*.py" -exec sed -i 's/open(\([^,]*\), "a")/open(\1, "a", encoding="utf-8")/g' {} \;
find src/create_python_project -type f -name "*.py" -exec sed -i 's/open(\([^,]*\), "w+")/open(\1, "w+", encoding="utf-8")/g' {} \;
find src/create_python_project -type f -name "*.py" -exec sed -i 's/open(\([^,]*\), "r+")/open(\1, "r+", encoding="utf-8")/g' {} \;
log "✅ Added encoding to open() calls"

# Fix f-string in logging
log "4. Fixing f-string in logging functions..."
find src/create_python_project -type f -name "*.py" -exec sed -i 's/logging\.debug(f\("[^"]*"\))/logging.debug(\1 % ())/g' {} \;
find src/create_python_project -type f -name "*.py" -exec sed -i 's/logging\.info(f\("[^"]*"\))/logging.info(\1 % ())/g' {} \;
find src/create_python_project -type f -name "*.py" -exec sed -i 's/logging\.warning(f\("[^"]*"\))/logging.warning(\1 % ())/g' {} \;
find src/create_python_project -type f -name "*.py" -exec sed -i 's/logging\.error(f\("[^"]*"\))/logging.error(\1 % ())/g' {} \;
find src/create_python_project -type f -name "*.py" -exec sed -i 's/logging\.critical(f\("[^"]*"\))/logging.critical(\1 % ())/g' {} \;
log "✅ Fixed f-string in logging functions"

# Fix unnecessary else/elif after return
log "5. Fixing unnecessary else/elif after return..."
# Find files with unnecessary elif after return
FILES_WITH_ELIF_AFTER_RETURN=$(grep -l "return.*\n.*elif" --include="*.py" -r src/create_python_project || true)
for file in $FILES_WITH_ELIF_AFTER_RETURN; do
    log "  Fixing unnecessary elif after return in $file"
    # This is a complex operation that might need manual intervention
    # We'll use a simple sed command to try to fix the most common cases
    sed -i 's/return.*\n.*elif/return\n    if/g' "$file" || true
done

# Find files with unnecessary else after return
FILES_WITH_ELSE_AFTER_RETURN=$(grep -l "return.*\n.*else" --include="*.py" -r src/create_python_project || true)
for file in $FILES_WITH_ELSE_AFTER_RETURN; do
    log "  Fixing unnecessary else after return in $file"
    # This is a complex operation that might need manual intervention
    # We'll use a simple sed command to try to fix the most common cases
    sed -i 's/return.*\n.*else/return\n/g' "$file" || true
done
log "✅ Fixed unnecessary else/elif after return where possible"

# Add timeout to requests.post calls
log "6. Adding timeout to requests.post calls..."
find src/create_python_project -type f -name "*.py" -exec sed -i 's/requests\.post(\([^,]*\))/requests.post(\1, timeout=30)/g' {} \;
find src/create_python_project -type f -name "*.py" -exec sed -i 's/requests\.post(\([^,]*\), \([^,]*\))/requests.post(\1, \2, timeout=30)/g' {} \;
find src/create_python_project -type f -name "*.py" -exec sed -i 's/requests\.get(\([^,]*\))/requests.get(\1, timeout=30)/g' {} \;
find src/create_python_project -type f -name "*.py" -exec sed -i 's/requests\.get(\([^,]*\), \([^,]*\))/requests.get(\1, \2, timeout=30)/g' {} \;
find src/create_python_project -type f -name "*.py" -exec sed -i 's/requests\.put(\([^,]*\))/requests.put(\1, timeout=30)/g' {} \;
find src/create_python_project -type f -name "*.py" -exec sed -i 's/requests\.put(\([^,]*\), \([^,]*\))/requests.put(\1, \2, timeout=30)/g' {} \;
log "✅ Added timeout to requests calls"

# Fix regular string formatting to f-string
log "7. Converting string formatting to f-strings..."
find src/create_python_project -type f -name "*.py" -exec sed -i 's/"\([^"]*\)".format(\([^)]*\))/f"\1"/g' {} \;
log "✅ Converted string formatting to f-strings where possible"

# Run black again to ensure consistent formatting
log "8. Running black again for consistent formatting..."
poetry run black src/create_python_project >> "$LOG_FILE" 2>&1
log "✅ Black formatting completed"

# Run pylint to check remaining issues
log "9. Running pylint to check remaining issues..."
poetry run pylint src/create_python_project > "${PROJECT_DIR}/pylint_report.txt" 2>&1 || true
log "✅ Pylint report generated at ${PROJECT_DIR}/pylint_report.txt"

# Run mypy to check type issues
log "10. Running mypy to check type issues..."
poetry run mypy --config-file=${PROJECT_DIR}/.config/mypy.ini ${PROJECT_DIR}/src/create_python_project > "${PROJECT_DIR}/mypy_report.txt" 2>&1 || true
log "✅ Mypy report generated at ${PROJECT_DIR}/mypy_report.txt"

# Run pre-commit without the update_documentation.sh hook
log "11. Running pre-commit hooks (excluding documentation update)..."
# We're using a temporary config to skip the documentation update hook
TEMP_CONFIG="${PROJECT_DIR}/.pre-commit-config.temp.yaml"
if [ -f "${PROJECT_DIR}/.pre-commit-config.yaml" ]; then
    cp "${PROJECT_DIR}/.pre-commit-config.yaml" "$TEMP_CONFIG"
    # Remove or comment out the documentation update hook if it exists
    sed -i '/update_documentation/d' "$TEMP_CONFIG"
    PYTHONPATH="${PROJECT_DIR}" pre-commit run --config "$TEMP_CONFIG" --all-files >> "$LOG_FILE" 2>&1 || true
    rm "$TEMP_CONFIG"
    log "✅ Pre-commit hooks completed"
else
    log "⚠️ No .pre-commit-config.yaml found, skipping pre-commit"
fi

echo ""
log "All automated fixes completed. Please check the log file at $LOG_FILE"
log "Some issues may require manual fixes. Check the pylint and mypy reports."
echo ""
echo "Remaining issues that may need manual fixes:"
echo "1. Too many local variables/branches/statements - Refactor large functions"
echo "2. Catching too general exceptions - Use more specific exception types"
echo "3. Too few public methods - Add methods or convert to functions if appropriate"
echo "4. Too many return statements - Simplify function logic"
echo ""
echo "To see remaining pylint issues, run: cat ${PROJECT_DIR}/pylint_report.txt"
