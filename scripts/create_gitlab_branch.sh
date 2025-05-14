#!/bin/bash
# Script to create a new branch for GitLab when branch protection is enabled

set -e  # Exit on error

# Get the project root directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_message "$BLUE" "================================================================"
print_message "$BLUE" "Creating a new branch for GitLab with branch protection"
print_message "$BLUE" "================================================================"

# Get the current branch
CURRENT_BRANCH=$(git branch --show-current)

# Ask for the new branch name
print_message "$YELLOW" "Enter a name for the new branch (e.g., update-history):"
read -p "Branch name: " NEW_BRANCH

if [[ -z "$NEW_BRANCH" ]]; then
    print_message "$RED" "Branch name cannot be empty."
    exit 1
fi

# Create the new branch
print_message "$YELLOW" "Creating new branch: $NEW_BRANCH"
git checkout -b "$NEW_BRANCH"

# Push the new branch to GitLab
print_message "$YELLOW" "Pushing new branch to GitLab..."
git push -u gitlab "$NEW_BRANCH"

print_message "$GREEN" "================================================================"
print_message "$GREEN" "New branch '$NEW_BRANCH' created and pushed to GitLab"
print_message "$GREEN" "================================================================"
print_message "$YELLOW" "Next steps:"
print_message "$YELLOW" "1. Go to GitLab and create a merge request from '$NEW_BRANCH' to 'main'"
print_message "$YELLOW" "2. After the merge request is approved and merged, you can delete this branch"
print_message "$YELLOW" "3. To switch back to your original branch, run:"
print_message "$YELLOW" "   git checkout $CURRENT_BRANCH"
print_message "$GREEN" "================================================================"
