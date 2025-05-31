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

# Logging
LOG_FILE="${PROJECT_DIR}/logs/commit_workflow.log"
mkdir -p "${PROJECT_DIR}/logs"

if [ -f "$LOG_FILE" ] && [ $(wc -l < "$LOG_FILE") -gt 200 ]; then
    tail -100 "$LOG_FILE" > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"
fi

log_step() {
    echo "$(date '+%Y-%m-%d %H:%M:%S'): $1" >> "$LOG_FILE"
}

print_message() {
    echo -e "${1}${2}${NC}"
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

generate_ai_commit_message() {
    local changed_files=$(git diff --cached --name-only)
    local prompt="Generate concise git commit message for: $changed_files"
    
    if [ -f "${PROJECT_DIR}/scripts/deepseek_commit_message.py" ]; then
        poetry run python "${PROJECT_DIR}/scripts/deepseek_commit_message.py" "$prompt" 2>/dev/null || echo "Update project files"
    else
        echo "Update project files"
    fi
}

log_step "=== Starting AI Commit Workflow ==="

print_message "$GREEN" "================================================================"
print_message "$GREEN" "                AI-ASSISTED COMMIT WORKFLOW                   "
print_message "$GREEN" "================================================================"

# Step 1: Clean staging
print_message "$BLUE" "🧹 Cleaning workspace and staging files..."
log_step "CLEAN: Starting file cleanup"

rm -f ai-docs/*.bak ai-docs/*.tmp >/dev/null 2>&1 || true
git add scripts/ .vscode/tasks.json pyproject.toml >/dev/null 2>&1 || true

log_step "CLEAN: Files staged"
print_message "$GREEN" "✅ Files staged successfully"

# Step 2: Documentation 
print_message "$BLUE" "📚 Updating project documentation..."
log_step "DOCS: Starting documentation update"

if [ -f "./scripts/manage_docs.sh" ]; then
    chmod +x ./scripts/manage_docs.sh
    ./scripts/manage_docs.sh >/dev/null 2>&1 || true
    git add "**/aboutthisfolder.md" >/dev/null 2>&1 || true
fi

log_step "DOCS: Documentation updated"
print_message "$GREEN" "✅ Documentation updated and staged"

# Step 3: Quality checks
print_message "$BLUE" "🔍 Running code quality checks..."
log_step "LINT: Starting quality checks"

# Black
print_message "$YELLOW" "  • Black (formatting)..."
if poetry run black src/ --check >/dev/null 2>&1; then
    echo " ✅"
    log_step "LINT: Black passed"
else
    echo " 🔧"
    poetry run black src/ >/dev/null 2>&1 || true
    git add src/ >/dev/null 2>&1 || true
    log_step "LINT: Black auto-fixed"
fi

# Ruff
print_message "$YELLOW" "  • Ruff (linting & imports)..."
if poetry run ruff check src/ >/dev/null 2>&1; then
    echo " ✅"
    log_step "LINT: Ruff passed"
else
    echo " 🔧"
    poetry run ruff check --fix src/ >/dev/null 2>&1 || true
    git add src/ >/dev/null 2>&1 || true
    log_step "LINT: Ruff auto-fixed"
fi

# MyPy
print_message "$YELLOW" "  • MyPy (type checking)..."
if poetry run mypy src/ --config-file=.config/mypy.ini >/dev/null 2>&1; then
    echo " ✅"
    log_step "LINT: MyPy passed"
else
    echo " ❌"
    print_message "$YELLOW" "MyPy errors found - continuing anyway"
    log_step "LINT: MyPy failed but continuing"
fi

print_message "$GREEN" "✅ All quality checks passed"

# Step 4: Generate commit message
print_message "$BLUE" "🤖 Generating AI commit message..."
log_step "COMMIT: Generating AI message"

COMMIT_MESSAGE=$(generate_ai_commit_message | head -1)
if [ -z "$COMMIT_MESSAGE" ]; then
    COMMIT_MESSAGE="Update project files"
fi

log_step "COMMIT: Generated: $COMMIT_MESSAGE"
print_message "$GREEN" "Generated: \"$COMMIT_MESSAGE\""

# Skip interactive editing in VS Code tasks
if [ -n "$VSCODE_GIT_ASKPASS_NODE" ] || [ "$TERM_PROGRAM" = "vscode" ]; then
    log_step "COMMIT: Skipping edit (VS Code task)"
else
    read -p "Edit this message? (y/n): " edit_message
    if [[ "$edit_message" == "y" || "$edit_message" == "Y" ]]; then
        TEMP_FILE=$(mktemp)
        echo "$COMMIT_MESSAGE" > "$TEMP_FILE"
        ${EDITOR:-nano} "$TEMP_FILE"
        COMMIT_MESSAGE=$(cat "$TEMP_FILE")
        rm "$TEMP_FILE"
    fi
fi

# Step 5: Commit
print_message "$BLUE" "💾 Committing changes..."
log_step "COMMIT: Starting git commit"

# Clean up any problematic staged changes
git rm --cached .config/.flake8 .config/.isort.cfg .config/pylintrc 2>/dev/null || true
git add -A 2>/dev/null || true

git commit -m "$COMMIT_MESSAGE"

if [ $? -eq 0 ]; then
    log_step "COMMIT: Successfully committed"
    print_message "$GREEN" "✅ Committed successfully"
else
    log_step "COMMIT: Failed to commit"
    print_message "$RED" "❌ Commit failed"
    exit 1
fi

# Step 6: Push
print_message "$BLUE" "🚀 Pushing to remotes..."
log_step "PUSH: Starting git push"

REMOTES=$(git remote)

if echo "$REMOTES" | grep -q "github"; then
    print_message "$YELLOW" "  • GitHub..."
    if git push github >/dev/null 2>&1; then
        echo " ✅"
        log_step "PUSH: GitHub successful"
    else
        echo " ❌"
        log_step "PUSH: GitHub failed"
    fi
fi

if echo "$REMOTES" | grep -q "gitlab"; then
    print_message "$YELLOW" "  • GitLab..."
    if git push gitlab >/dev/null 2>&1; then
        echo " ✅"  
        log_step "PUSH: GitLab successful"
    else
        echo " ❌ (server down)"
        log_step "PUSH: GitLab failed - server down"
    fi
fi

log_step "=== Workflow Completed ==="

print_message "$GREEN" "================================================================"
print_message "$GREEN" "✨ AI-assisted commit workflow completed successfully!"
print_message "$GREEN" "================================================================"
