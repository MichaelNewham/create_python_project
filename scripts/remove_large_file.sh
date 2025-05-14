#!/bin/bash
# Script to remove a large file from git history

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
print_message "$BLUE" "Removing large file from git history"
print_message "$BLUE" "================================================================"

# The file to remove
FILE_TO_REMOVE="ai-docs/convo.md"

print_message "$YELLOW" "This script will remove $FILE_TO_REMOVE from the git history."
print_message "$YELLOW" "This is a destructive operation that rewrites git history."
print_message "$YELLOW" "Make sure you have a backup of your repository before proceeding."
print_message "$YELLOW" "After running this script, all collaborators will need to re-clone the repository."
echo ""
read -p "Do you want to proceed? (y/n): " proceed

if [[ "$proceed" != "y" && "$proceed" != "Y" ]]; then
    print_message "$RED" "Operation cancelled."
    exit 1
fi

# Create a backup of the current state
print_message "$YELLOW" "Creating a backup of the current state..."
BACKUP_DIR="${PROJECT_DIR}_backup_$(date '+%Y%m%d_%H%M%S')"
cp -r "$PROJECT_DIR" "$BACKUP_DIR"
print_message "$GREEN" "Backup created at $BACKUP_DIR"

# Remove the file from git history
print_message "$YELLOW" "Removing $FILE_TO_REMOVE from git history..."
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch $FILE_TO_REMOVE" --prune-empty --tag-name-filter cat -- --all

# Clean up
print_message "$YELLOW" "Cleaning up..."
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now
git gc --aggressive --prune=now

print_message "$GREEN" "================================================================"
print_message "$GREEN" "$FILE_TO_REMOVE has been removed from git history"
print_message "$GREEN" "================================================================"
print_message "$YELLOW" "Next steps:"
print_message "$YELLOW" "1. Force push to remote repositories:"
print_message "$YELLOW" "   git push origin --force --all"
print_message "$YELLOW" "   git push origin --force --tags"
print_message "$YELLOW" "2. Ask collaborators to re-clone the repository"
print_message "$GREEN" "================================================================"
