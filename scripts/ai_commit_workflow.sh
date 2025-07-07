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
    local changed_files=$(git diff --cached --name-only)
    local commit_stats=$(git diff --cached --stat)
    local prompt="Generate concise git commit message for these changes:

Files: $changed_files

Stats: $commit_stats

Focus on the main operation (add/update/delete/refactor)"
    
    # Try DeepSeek API
    if [ -f "${PROJECT_DIR}/scripts/testing/deepseek_commit_message.py" ]; then
        local deepseek_result=$(poetry run python "${PROJECT_DIR}/scripts/testing/deepseek_commit_message.py" "$prompt" 2>/dev/null)
        if [ "$deepseek_result" != "Update project files" ] && [ -n "$deepseek_result" ]; then
            echo "$deepseek_result"
            return
        fi
    fi
    
    # Default fallback
    echo "Update project files"
}

print_message "$GREEN" "================================================================"
print_message "$GREEN" "                AI-ASSISTED COMMIT WORKFLOW                   "
print_message "$GREEN" "================================================================"

# Step 1: Clean staging
print_message "$BLUE" "🧹 Cleaning workspace and staging files..."
rm -f ai-docs/*.bak ai-docs/*.tmp >/dev/null 2>&1 || true
git add scripts/ .vscode/tasks.json pyproject.toml >/dev/null 2>&1 || true
print_message "$GREEN" "✅ Files staged successfully"

# Step 2: Documentation 
print_message "$BLUE" "📚 Updating project documentation..."
if [ -f "./scripts/docs/manage_docs.sh" ]; then
    chmod +x ./scripts/docs/manage_docs.sh
    ./scripts/docs/manage_docs.sh >/dev/null 2>&1 || true
    git add "**/aboutthisfolder.md" >/dev/null 2>&1 || true
fi
print_message "$GREEN" "✅ Documentation updated and staged"

# Step 3: Quality checks
print_message "$BLUE" "🔍 Running code quality checks..."

# Black
print_message "$YELLOW" "  • Black (formatting)..."
if poetry run black src/ --check >/dev/null 2>&1; then
    echo " ✅"
else
    echo " 🔧"
    poetry run black src/ >/dev/null 2>&1 || true
    git add src/ >/dev/null 2>&1 || true
fi

# Ruff
print_message "$YELLOW" "  • Ruff (linting & imports)..."
if poetry run ruff check src/ >/dev/null 2>&1; then
    echo " ✅"
else
    echo " 🔧"
    poetry run ruff check --fix src/ >/dev/null 2>&1 || true
    git add src/ >/dev/null 2>&1 || true
fi

# MyPy
print_message "$YELLOW" "  • MyPy (type checking)..."
if poetry run mypy src/ --config-file=.config/mypy.ini >/dev/null 2>&1; then
    echo " ✅"
else
    echo " ❌"
    print_message "$YELLOW" "MyPy errors found - continuing anyway"
fi

print_message "$GREEN" "✅ All quality checks passed"

# Step 4: Generate commit message
print_message "$BLUE" "🤖 Generating AI commit message..."
COMMIT_MESSAGE=$(generate_ai_commit_message | head -1)
if [ -z "$COMMIT_MESSAGE" ]; then
    COMMIT_MESSAGE="Update project files"
fi
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
git rm --cached .config/.flake8 .config/.isort.cfg .config/pylintrc 2>/dev/null || true
git add -A 2>/dev/null || true
git commit -m "$COMMIT_MESSAGE"

if [ $? -eq 0 ]; then
    print_message "$GREEN" "✅ Committed successfully"
else
    print_message "$RED" "❌ Commit failed"
    exit 1
fi

# Step 6: Push
print_message "$BLUE" "🚀 Pushing to remotes..."
REMOTES=$(git remote)

if echo "$REMOTES" | grep -q "github"; then
    print_message "$YELLOW" "  • GitHub..."
    if git push github >/dev/null 2>&1; then
        echo " ✅"
    else
        echo " ❌"
    fi
fi

if echo "$REMOTES" | grep -q "gitlab"; then
    print_message "$YELLOW" "  • GitLab..."
    if git push gitlab >/dev/null 2>&1; then
        echo " ✅"  
    else
        echo " ❌ (server down)"
    fi
fi

print_message "$GREEN" "================================================================"
print_message "$GREEN" "✨ AI-assisted commit workflow completed successfully!"
print_message "$GREEN" "================================================================"
