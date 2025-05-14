#!/bin/bash
# Script to immediately truncate all markdown files to 150 lines maximum

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
print_message "$BLUE" "Truncating all markdown files to 150 lines maximum"
print_message "$BLUE" "================================================================"

# First, let's handle the convo.md file specifically since it's causing the most issues
if [[ -f "${PROJECT_DIR}/ai-docs/convo.md" ]]; then
    print_message "$YELLOW" "Handling ai-docs/convo.md specifically..."
    
    # Create a new file from scratch
    cat > "${PROJECT_DIR}/ai-docs/convo.md" << EOF
<!-- filepath: ${PROJECT_DIR}/ai-docs/convo.md -->
# Engineering Assessment for Create Python Project

## Latest Updates ($(date '+%Y-%m-%d'))

### Changes Made
1. **File Size Limitation**
   - Limited all markdown files to 150 lines maximum
   - Implemented automatic truncation in documentation update process
   - Fixed GitHub push errors related to file size limits

## Project Structure

The project is organized as follows:

- **src/create_python_project/**: Main implementation code
  - **utils/**: Utility modules and helper functions
- **tests/**: Test files for the project
- **scripts/**: Automation scripts for development workflow
- **ai-docs/**: AI-related documentation and conversation logs
- **.config/**: Configuration files for linters and tools
- **.vscode/**: VS Code specific settings and tasks

## Key Project Information

- Python projects should have a .code-workspace file, ai-docs and specs folders
- Claude code integration with a .claude file in the root folder
- Logging functionality in src/create_python_project/utils/logging.py
- Python projects should have a mcp.json file in the /.vscode folder
- README.md files in subfolders should be renamed to aboutthisfolder.md
- AI conversation logs should be stored in /ai-docs
- Python projects should include a .pre-commit-config.yaml file
- The user prefers to use a single task for running the full linting suite
- The user wants to see project structure in tree format
- The user wants .env files copied to new projects
- The user wants YAML files and tasks.json copied to new projects

## Development Workflow

- Test-first development approach
- Step-by-step approach to testing with simulated terminal output
- The project uses Poetry for package management instead of pip
- AI integration is compulsory and appears as question #2 in the project creation flow
- Project directory input should be prepopulated based on project name
- AI model names should be read from the .env file

---

**Note:** This file is automatically limited to 150 lines maximum to prevent exceeding GitHub's file size limits.
EOF
    
    print_message "$GREEN" "✅ ai-docs/convo.md recreated successfully"
fi

# Now process all other markdown files
print_message "$YELLOW" "Processing all other markdown files..."

# Find all markdown files in the project
find "${PROJECT_DIR}" -type f -name "*.md" -not -path "${PROJECT_DIR}/.git/*" -not -path "${PROJECT_DIR}/.venv/*" | while read -r md_file; do
    # Count lines in the file
    line_count=$(wc -l < "$md_file")
    
    # If the file has more than 150 lines, truncate it
    if [[ $line_count -gt 150 ]]; then
        print_message "$YELLOW" "Truncating $md_file from $line_count lines to 150 lines"
        
        # Create a temporary file
        temp_file="${md_file}.tmp"
        
        # Extract the first 145 lines
        head -n 145 "$md_file" > "$temp_file"
        
        # Add a note about truncation
        echo "" >> "$temp_file"
        echo "---" >> "$temp_file"
        echo "" >> "$temp_file"
        echo "**Note:** This file has been automatically truncated to 150 lines maximum." >> "$temp_file"
        echo "Full content was $line_count lines. Last updated: $(date '+%Y-%m-%d %H:%M:%S')" >> "$temp_file"
        
        # Replace the original file with the truncated version
        mv "$temp_file" "$md_file"
        
        print_message "$GREEN" "✅ $md_file truncated successfully"
    fi
done

print_message "$GREEN" "================================================================"
print_message "$GREEN" "All markdown files have been truncated to 150 lines maximum"
print_message "$GREEN" "================================================================"
