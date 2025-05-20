#!/bin/bash
# Script to remove sensitive files from git repository history
# This script will rewrite git history to remove specified files
set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Parse command line arguments
DRY_RUN=0
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=1
    shift
fi

echo -e "${YELLOW}WARNING: This script will rewrite git history.${NC}"
echo -e "${YELLOW}Make sure all collaborators are aware of this operation.${NC}"
echo -e "${YELLOW}They will need to re-clone or carefully rebase after this change.${NC}"
echo

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is not installed.${NC}"
    exit 1
fi

# Check if git-filter-repo is installed in Poetry environment
if ! poetry run python -c "import git_filter_repo" &> /dev/null; then
    echo -e "${YELLOW}git-filter-repo not found. Installing in Poetry environment...${NC}"
    poetry run pip install git-filter-repo
fi

# Get the sensitive file path from command line argument or prompt the user
SENSITIVE_FILE="${1}"
if [ -z "$SENSITIVE_FILE" ]; then
    read -p "Enter the path of the sensitive file to remove (e.g., .vscode/mcp.json): " SENSITIVE_FILE
fi

# Confirm with the user
echo -e "${YELLOW}You are about to remove ${SENSITIVE_FILE} from the entire git history.${NC}"
if [[ $DRY_RUN -eq 1 ]]; then
    echo -e "${GREEN}DRY RUN: No changes will be made.${NC}"
else
    read -p "Are you sure you want to proceed? (y/N): " CONFIRM
    if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Operation cancelled.${NC}"
        exit 0
    fi
fi

# Create a backup of the current state
if [[ $DRY_RUN -eq 0 ]]; then
    TIMESTAMP=$(date "+%Y%m%d%H%M%S")
    BACKUP_DIR="../git_backup_${TIMESTAMP}"
    echo -e "${GREEN}Creating a backup in ${BACKUP_DIR}${NC}"
    mkdir -p "$BACKUP_DIR"
    git bundle create "${BACKUP_DIR}/backup.bundle" --all
fi

# Remove the sensitive file from git history
echo -e "${GREEN}Removing ${SENSITIVE_FILE} from git history...${NC}"
if [[ $DRY_RUN -eq 1 ]]; then
    echo -e "${GREEN}DRY RUN: Would execute: poetry run git-filter-repo --invert-paths --path \"$SENSITIVE_FILE\" --force${NC}"
    echo -e "${GREEN}DRY RUN: This would remove the file from git history.${NC}"
else
    # Use git-filter-repo from the Poetry environment
    poetry run git-filter-repo --invert-paths --path "$SENSITIVE_FILE" --force
    
    echo -e "${GREEN}File has been removed from git history.${NC}"
    echo -e "${YELLOW}You will need to force push these changes:${NC}"
    echo -e "  git push origin --force"
    echo
    echo -e "${YELLOW}Collaborators will need to re-clone the repository or carefully rebase.${NC}"
    echo -e "${GREEN}A backup of the repository before this operation is available at: ${BACKUP_DIR}/backup.bundle${NC}"
fi
