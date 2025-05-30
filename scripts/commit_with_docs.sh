#!/bin/bash
# Script to commit changes with documentation updates

set -e

# Get the project root directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# Check if there are changes to commit
if [ -z "$(git status --porcelain)" ]; then
    echo "No changes to commit."
    exit 0
fi

# Get commit message from argument or use default
COMMIT_MESSAGE="${1:-Update project files}"

echo "=== Committing with documentation updates ==="
echo "1. Adding all changes to git staging"
git add .

echo "2. Creating a backup of pre-commit config"
cp .pre-commit-config.yaml .pre-commit-config.yaml.bak

echo "3. Updating documentation"
./scripts/update_documentation.sh

echo "4. Adding documentation changes"
git add .

echo "5. Running pre-commit hooks"
pre-commit run --all-files || {
    echo "Pre-commit hooks failed. Restoring original pre-commit config."
    mv .pre-commit-config.yaml.bak .pre-commit-config.yaml
    exit 1
}

echo "6. Committing changes"
git commit -m "$COMMIT_MESSAGE"

echo "7. Restoring original pre-commit config"
mv .pre-commit-config.yaml.bak .pre-commit-config.yaml

echo "8. Pushing changes"
./scripts/post_commit_push.sh

echo "=== Commit completed successfully ==="
