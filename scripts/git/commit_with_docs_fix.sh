#!/bin/bash
# Script to update documentation and commit changes without running into pre-commit loops

set -e

# Get the project root directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# Get commit message from argument or use default
COMMIT_MESSAGE="${1:-Update project files}"

echo "=== Documentation Update and Commit Process ==="

# Step 1: Add all changes to git staging
echo "1. Adding all changes to git staging"
git add .

# Step 2: Run documentation update separately (not as part of pre-commit)
echo "2. Running documentation update"
../update_documentation.sh --list-only

# Ask user if they want to proceed with documentation update
# Skip interactive prompts in VS Code/Cursor tasks
if [ -n "$VSCODE_GIT_ASKPASS_NODE" ] || [ "$TERM_PROGRAM" = "vscode" ]; then
    echo "Skipping interactive prompt (IDE task)"
    continue
fi
read -p "Do you want to proceed with documentation update? (y/n): " proceed
if [[ "$proceed" != "y" && "$proceed" != "Y" ]]; then
    echo "Documentation update skipped."
else
    echo "Running documentation update..."
    ../update_documentation.sh

    # Add documentation changes to git
    echo "Adding documentation changes to git"
    git add .
fi

# Step 3: Run pre-commit checks without documentation hook
echo "3. Running pre-commit checks (without documentation hook)"
# Use the modified pre-commit config
cp .pre-commit-config.yaml .pre-commit-config.yaml.bak
cp .config/.pre-commit-config.yaml.no-docs .pre-commit-config.yaml

# Run pre-commit
pre-commit run --all-files
PRE_COMMIT_STATUS=$?

# Restore original pre-commit config
mv .pre-commit-config.yaml.bak .pre-commit-config.yaml

# Check if pre-commit passed
if [ $PRE_COMMIT_STATUS -ne 0 ]; then
    echo "❌ Pre-commit checks failed. Please fix the issues before committing."
    exit 1
fi

# Step 4: Commit changes
echo "4. Committing changes"
git commit -m "$COMMIT_MESSAGE"

# Step 5: Push changes
echo "5. Pushing changes"
../post_commit_push.sh

echo "=== Process completed successfully ==="
