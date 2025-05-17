#!/bin/bash
# This script bypasses pre-commit hooks and pushes to both GitHub and GitLab

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the project root directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# Check if there are any changes to commit
if [[ -z $(git status -s) ]]; then
    echo -e "${YELLOW}No changes to commit.${NC}"
else
    # Stage all changes
    echo -e "${GREEN}Staging changes...${NC}"
    git add .
    
    # Commit with given message or default
    MESSAGE=${1:-"Force commit bypassing hooks"}
    echo -e "${GREEN}Committing changes with message: ${MESSAGE}${NC}"
    git commit --no-verify -m "$MESSAGE"
fi

# Push to GitHub
echo -e "${GREEN}Pushing to GitHub...${NC}"
git push github $(git branch --show-current) || {
    echo -e "${RED}❌ Error: Push to GitHub failed. You may need to pull changes first or resolve conflicts.${NC}"
    exit 1
}
echo -e "${GREEN}✅ Push to GitHub completed successfully.${NC}"

# Push to GitLab
echo -e "${GREEN}Pushing to GitLab...${NC}"
git push gitlab $(git branch --show-current) || {
    echo -e "${RED}❌ Error: Push to GitLab failed. Please check your GitLab connection or configuration.${NC}"
    # Continue even if GitLab push fails
    echo -e "${YELLOW}⚠️ Warning: Changes pushed to GitHub but not to GitLab.${NC}"
    exit 0
}
echo -e "${GREEN}✅ Push to GitLab completed successfully.${NC}"

echo -e "${GREEN}✨ All changes pushed to all remotes successfully.${NC}"
