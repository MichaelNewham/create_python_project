#!/bin/bash
# AI-assisted commit workflow script

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

print_message() {
    echo -e "${1}${2}${NC}"
}

generate_ai_commit_message() {
    # Find the last successful push commit
    local last_pushed_commit=""
    local current_branch=$(git branch --show-current)
    
    # Try to find the last commit that was pushed to GitHub
    if git remote | grep -q "github"; then
        # Get the last common commit between local and remote
        if git ls-remote --heads github "$current_branch" &>/dev/null; then
            last_pushed_commit=$(git merge-base HEAD "github/$current_branch" 2>/dev/null || echo "")
        fi
    fi
    
    # If no remote tracking, use the last commit from the log that shows a successful push
    if [ -z "$last_pushed_commit" ]; then
        # Fallback: use HEAD~1 if no remote info available
        last_pushed_commit="HEAD~1"
    fi
    
    # Get changes since last successful push
    local changed_files=$(git diff --name-status "$last_pushed_commit" 2>/dev/null || git diff --name-status --cached)
    local commit_stats=$(git diff --stat "$last_pushed_commit" 2>/dev/null || git diff --stat --cached)
    local added_files=$(echo "$changed_files" | grep "^A" | cut -f2- | head -5)
    local modified_files=$(echo "$changed_files" | grep "^M" | cut -f2- | head -5)
    local deleted_files=$(echo "$changed_files" | grep "^D" | cut -f2- | head -5)
    
    # Build contextual prompt
    local prompt="Generate a concise git commit message for these changes since the last push:

ANALYSIS OF CHANGES:
Files Added: $(echo "$added_files" | tr '\n' ', ' | sed 's/,$//')
Files Modified: $(echo "$modified_files" | tr '\n' ', ' | sed 's/,$//')
Files Deleted: $(echo "$deleted_files" | tr '\n' ', ' | sed 's/,$//')

CHANGE STATISTICS:
$commit_stats

INSTRUCTIONS:
- For substantial changes (multiple files, new features): Generate 2-3 line message with title + brief description
- For minor changes (1-2 files, small fixes): Generate single line message
- Use action words: Add, Update, Refactor, Fix, Remove, Implement
- Focus on the main purpose, not just file names
- Be specific about what was accomplished"
    
    # Log the analysis
    echo "$(date '+%Y-%m-%d %H:%M:%S'): COMMIT: Analyzing changes since $last_pushed_commit" >> "${PROJECT_DIR}/logs/commit_workflow.log"
    
    # Try DeepSeek API
    if [ -f "${PROJECT_DIR}/scripts/testing/deepseek_commit_message.py" ]; then
        local deepseek_result=$(poetry run python "${PROJECT_DIR}/scripts/testing/deepseek_commit_message.py" "$prompt" 2>/dev/null)
        if [ "$deepseek_result" != "Update project files" ] && [ -n "$deepseek_result" ]; then
            echo "$(date '+%Y-%m-%d %H:%M:%S'): COMMIT: AI generated: $deepseek_result" >> "${PROJECT_DIR}/logs/commit_workflow.log"
            echo "$deepseek_result"
            return
        fi
    fi
    
    # Intelligent fallback based on changes
    if [ -n "$added_files" ] && [ -n "$modified_files" ]; then
        echo "Add new features and update existing components"
    elif [ -n "$added_files" ]; then
        echo "Add new $(echo "$added_files" | wc -l) files"
    elif [ -n "$modified_files" ]; then
        echo "Update $(echo "$modified_files" | wc -l) files"
    elif [ -n "$deleted_files" ]; then
        echo "Remove $(echo "$deleted_files" | wc -l) files"
    else
        echo "Update project files"
    fi
}

print_message "$GREEN" "================================================================"
print_message "$GREEN" "                AI-ASSISTED COMMIT WORKFLOW                   "
print_message "$GREEN" "================================================================"

# Create logs directory if it doesn't exist
mkdir -p "${PROJECT_DIR}/logs"

# Log workflow start
echo "$(date '+%Y-%m-%d %H:%M:%S'): === Starting AI Commit Workflow ===" >> "${PROJECT_DIR}/logs/commit_workflow.log"

# Step 1: Clean staging
print_message "$BLUE" "🧹 Cleaning workspace and staging files..."
echo "$(date '+%Y-%m-%d %H:%M:%S'): CLEAN: Starting file cleanup" >> "${PROJECT_DIR}/logs/commit_workflow.log"
rm -f ai-docs/*.bak ai-docs/*.tmp >/dev/null 2>&1 || true
git add scripts/ .vscode/tasks.json pyproject.toml >/dev/null 2>&1 || true
echo "$(date '+%Y-%m-%d %H:%M:%S'): CLEAN: Files staged" >> "${PROJECT_DIR}/logs/commit_workflow.log"
print_message "$GREEN" "✅ Files staged successfully"

# Step 2: Documentation 
print_message "$BLUE" "📚 Updating project documentation..."
echo "$(date '+%Y-%m-%d %H:%M:%S'): DOCS: Starting documentation update" >> "${PROJECT_DIR}/logs/commit_workflow.log"
if [ -f "./scripts/docs/manage_docs.sh" ]; then
    chmod +x ./scripts/docs/manage_docs.sh
    ./scripts/docs/manage_docs.sh >/dev/null 2>&1 || true
    git add "**/aboutthisfolder.md" >/dev/null 2>&1 || true
fi
echo "$(date '+%Y-%m-%d %H:%M:%S'): DOCS: Documentation updated" >> "${PROJECT_DIR}/logs/commit_workflow.log"
print_message "$GREEN" "✅ Documentation updated and staged"

# Step 3: Quality checks
print_message "$BLUE" "🔍 Running code quality checks..."
echo "$(date '+%Y-%m-%d %H:%M:%S'): LINT: Starting quality checks" >> "${PROJECT_DIR}/logs/commit_workflow.log"

# Black
print_message "$YELLOW" "  • Black (formatting)..."
if poetry run black src/ --check >/dev/null 2>&1; then
    echo " ✅"
    echo "$(date '+%Y-%m-%d %H:%M:%S'): LINT: Black passed" >> "${PROJECT_DIR}/logs/commit_workflow.log"
else
    echo " 🔧"
    poetry run black src/ >/dev/null 2>&1 || true
    git add src/ >/dev/null 2>&1 || true
    echo "$(date '+%Y-%m-%d %H:%M:%S'): LINT: Black auto-fixed" >> "${PROJECT_DIR}/logs/commit_workflow.log"
fi

# Ruff
print_message "$YELLOW" "  • Ruff (linting & imports)..."
if poetry run ruff check src/ >/dev/null 2>&1; then
    echo " ✅"
    echo "$(date '+%Y-%m-%d %H:%M:%S'): LINT: Ruff passed" >> "${PROJECT_DIR}/logs/commit_workflow.log"
else
    echo " 🔧"
    poetry run ruff check --fix src/ >/dev/null 2>&1 || true
    git add src/ >/dev/null 2>&1 || true
    echo "$(date '+%Y-%m-%d %H:%M:%S'): LINT: Ruff auto-fixed" >> "${PROJECT_DIR}/logs/commit_workflow.log"
fi

# MyPy
print_message "$YELLOW" "  • MyPy (type checking)..."
if poetry run mypy src/ --config-file=.config/mypy.ini >/dev/null 2>&1; then
    echo " ✅"
    echo "$(date '+%Y-%m-%d %H:%M:%S'): LINT: MyPy passed" >> "${PROJECT_DIR}/logs/commit_workflow.log"
else
    echo " ❌"
    print_message "$YELLOW" "MyPy errors found - continuing anyway"
    echo "$(date '+%Y-%m-%d %H:%M:%S'): LINT: MyPy errors found - continuing" >> "${PROJECT_DIR}/logs/commit_workflow.log"
fi

print_message "$GREEN" "✅ All quality checks passed"

# Step 4: Generate commit message
print_message "$BLUE" "🤖 Generating AI commit message..."
echo "$(date '+%Y-%m-%d %H:%M:%S'): COMMIT: Generating AI message" >> "${PROJECT_DIR}/logs/commit_workflow.log"
COMMIT_MESSAGE=$(generate_ai_commit_message | head -1)
if [ -z "$COMMIT_MESSAGE" ]; then
    COMMIT_MESSAGE="Update project files"
fi
echo "$(date '+%Y-%m-%d %H:%M:%S'): COMMIT: Generated: $COMMIT_MESSAGE" >> "${PROJECT_DIR}/logs/commit_workflow.log"
print_message "$GREEN" "Generated: \"$COMMIT_MESSAGE\""

read -p "Edit this message? (y/n): " edit_message
if [[ "$edit_message" == "y" || "$edit_message" == "Y" ]]; then
    TEMP_FILE=$(mktemp)
    echo "$COMMIT_MESSAGE" > "$TEMP_FILE"
    ${EDITOR:-nano} "$TEMP_FILE"
    COMMIT_MESSAGE=$(cat "$TEMP_FILE")
    rm "$TEMP_FILE"
fi

# Step 5: Commit
print_message "$BLUE" "💾 Committing changes..."
echo "$(date '+%Y-%m-%d %H:%M:%S'): COMMIT: Starting git commit" >> "${PROJECT_DIR}/logs/commit_workflow.log"
git rm --cached .config/.flake8 .config/.isort.cfg .config/pylintrc 2>/dev/null || true
git add -A 2>/dev/null || true
git commit -m "$COMMIT_MESSAGE"

if [ $? -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S'): COMMIT: Successfully committed" >> "${PROJECT_DIR}/logs/commit_workflow.log"
    print_message "$GREEN" "✅ Committed successfully"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S'): COMMIT: Failed to commit" >> "${PROJECT_DIR}/logs/commit_workflow.log"
    print_message "$RED" "❌ Commit failed"
    exit 1
fi

# Step 6: Push
print_message "$BLUE" "🚀 Pushing to remotes..."
echo "$(date '+%Y-%m-%d %H:%M:%S'): PUSH: Starting git push" >> "${PROJECT_DIR}/logs/commit_workflow.log"
REMOTES=$(git remote)

if echo "$REMOTES" | grep -q "github"; then
    print_message "$YELLOW" "  • GitHub..."
    if git push github >/dev/null 2>&1; then
        echo " ✅"
        echo "$(date '+%Y-%m-%d %H:%M:%S'): PUSH: GitHub successful" >> "${PROJECT_DIR}/logs/commit_workflow.log"
    else
        echo " ❌"
        echo "$(date '+%Y-%m-%d %H:%M:%S'): PUSH: GitHub failed" >> "${PROJECT_DIR}/logs/commit_workflow.log"
    fi
fi

if echo "$REMOTES" | grep -q "gitlab"; then
    print_message "$YELLOW" "  • GitLab..."
    if git push gitlab >/dev/null 2>&1; then
        echo " ✅"
        echo "$(date '+%Y-%m-%d %H:%M:%S'): PUSH: GitLab successful" >> "${PROJECT_DIR}/logs/commit_workflow.log"
    else
        echo " ❌ (server down)"
        echo "$(date '+%Y-%m-%d %H:%M:%S'): PUSH: GitLab failed - server down" >> "${PROJECT_DIR}/logs/commit_workflow.log"
    fi
fi

echo "$(date '+%Y-%m-%d %H:%M:%S'): === Workflow Completed ===" >> "${PROJECT_DIR}/logs/commit_workflow.log"
print_message "$GREEN" "================================================================"
print_message "$GREEN" "✨ AI-assisted commit workflow completed successfully!"
print_message "$GREEN" "================================================================"
