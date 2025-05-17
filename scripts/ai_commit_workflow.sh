#!/bin/bash
# AI-assisted commit workflow script
# This script:
# 1. Runs documentation update
# 2. Runs pre-commit checks
# 3. Generates an AI commit message using the project's AI integration
# 4. Commits with the AI-generated message
# 5. Pushes to both GitLab and GitHub

set -e  # Exit on error

# Get the project root directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required commands
check_required_commands() {
    local missing_commands=()

    # Check for pre-commit
    if ! command_exists pre-commit; then
        missing_commands+=("pre-commit")
    fi

    # Check for poetry
    if ! command_exists poetry; then
        missing_commands+=("poetry")
    fi

    # If any commands are missing, print an error and exit
    if [ ${#missing_commands[@]} -gt 0 ]; then
        print_message "$RED" "❌ The following required commands are missing:"
        for cmd in "${missing_commands[@]}"; do
            print_message "$RED" "  - $cmd"
        done
        print_message "$YELLOW" "Please install the missing commands and try again."
        exit 1
    fi

    # Check if Python dependencies are installed in Poetry environment
    print_message "$YELLOW" "Checking Python dependencies in Poetry environment..."
    
    # Check for python-dotenv in Poetry environment
    if ! poetry run python -c "import dotenv" 2>/dev/null && ! poetry run python -c "from dotenv import load_dotenv" 2>/dev/null; then
        print_message "$YELLOW" "Installing python-dotenv in Poetry environment..."
        poetry add --group dev python-dotenv
    fi

    # Check for requests in Poetry environment
    if ! poetry run python -c "import requests" 2>/dev/null; then
        print_message "$YELLOW" "Installing requests in Poetry environment..."
        poetry add --group dev requests
    fi

    # Check for pylint in Poetry environment
    if ! poetry run python -c "import pylint" 2>/dev/null; then
        print_message "$YELLOW" "Installing pylint in Poetry environment..."
        poetry add --group dev pylint
    fi
}

# Function to generate AI commit message based on changes
generate_ai_commit_message() {
    # These messages are now only displayed to the console, not captured in variables
    print_message "$BLUE" "🤖 Generating AI commit message..."

    # Get the list of changed files
    local changed_files=$(git diff --cached --name-only)

    # Get a summary of changes
    local diff_summary=$(git diff --cached --stat)

    # Get detailed diff for context (limit to 2000 chars to avoid token limits)
    local diff_details=$(git diff --cached | head -c 2000)

    # Create a prompt for the AI
    local prompt="Generate a concise, informative git commit message for the following changes:

Changed files:
${changed_files}

Change summary:
${diff_summary}

Diff details (partial):
${diff_details}

The commit message should follow best practices:
1. Start with a short summary line (max 50 chars)
2. Follow with a blank line
3. Then add a more detailed explanation if needed
4. Focus on WHY the change was made, not just WHAT was changed
5. Use imperative mood (\"Add feature\" not \"Added feature\")"

    # Try to use DeepSeek API first
    if command_exists poetry; then
        print_message "$CYAN" "Using DeepSeek API..."

        # Use DeepSeek to generate commit message
        local commit_message=$(poetry run python -c "
import requests
import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up DeepSeek API
api_key = os.environ.get('DEEPSEEK_API_KEY')
model = os.environ.get('DEEPSEEK_MODEL', 'deepseek-chat')

if not api_key:
    print('No DeepSeek API key found. Update project files')
    sys.exit(0)

try:
    # Set up the API request
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant that generates git commit messages.'},
            {'role': 'user', 'content': '''$prompt'''}
        ],
        'max_tokens': 300
    }
    
    # Make the API request
    response = requests.post(
        'https://api.deepseek.com/v1/chat/completions',
        headers=headers,
        data=json.dumps(data)
    )
    
    if response.status_code == 200:
        # Extract the commit message
        result = response.json()
        commit_message = result['choices'][0]['message']['content'].strip()
        print(commit_message)
    else:
        print(f'Error from DeepSeek API: {response.status_code}')
        print('Update project files')
        
except Exception as e:
    print(f'Exception: {e}')
    print('Update project files')
    sys.exit(0)
")
    # Try to use the project's AI integration utilities if DeepSeek fails
    elif command_exists poetry && poetry run python -c "import sys; sys.path.append('${PROJECT_DIR}'); from create_python_project.utils.ai_integration import OpenAIProvider; print('OK')" 2>/dev/null | grep -q "OK"; then
        # Display message to console only, not captured in variables
        print_message "$CYAN" "Using project's AI integration utilities..."

        # Use the project's AI integration to generate commit message
        local commit_message=$(poetry run python -c "
import sys
sys.path.append('${PROJECT_DIR}')
from create_python_project.utils.ai_integration import OpenAIProvider
import os

try:
    # Create OpenAI provider
    provider = OpenAIProvider()

    # Check if API key is available
    if not provider.api_key:
        print('Update project files')
        sys.exit(0)

    # Generate response
    success, response = provider.generate_response('''$prompt''')

    if success:
        print(response)
    else:
        print('Update project files')
except Exception as e:
    print('Update project files')
    sys.exit(0)
")
    # Fallback to direct OpenAI API if project utilities and DeepSeek aren't available
    elif command_exists python && python -c "import openai" >/dev/null 2>&1; then
        print_message "$CYAN" "Using direct OpenAI API..."

        # Use OpenAI to generate commit message
        local commit_message=$(python -c "
import openai
import os
import sys

# Set up OpenAI API
openai.api_key = os.environ.get('OPENAI_API_KEY')

if not openai.api_key:
    print('Update project files')
    sys.exit(0)

try:
    # Create a chat completion
    response = openai.chat.completions.create(
        model=os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo'),
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant that generates git commit messages.'},
            {'role': 'user', 'content': '''$prompt'''}
        ],
        max_tokens=300
    )

    # Extract the commit message
    commit_message = response.choices[0].message.content.strip()
    print(commit_message)
except Exception as e:
    print('Update project files')
    sys.exit(0)
")
    # Try Anthropic if OpenAI isn't available
    elif command_exists python && python -c "import anthropic" >/dev/null 2>&1; then
        print_message "$CYAN" "Using Anthropic API..."

        # Use Anthropic to generate commit message
        local commit_message=$(python -c "
import anthropic
import os
import sys

# Set up Anthropic API
api_key = os.environ.get('ANTHROPIC_API_KEY')

if not api_key:
    print('Update project files')
    sys.exit(0)

try:
    # Create Anthropic client
    client = anthropic.Anthropic(api_key=api_key)

    # Create a message
    message = client.messages.create(
        model=os.environ.get('ANTHROPIC_MODEL', 'claude-3-haiku-20240307'),
        max_tokens=300,
        system='You are a helpful assistant that generates git commit messages.',
        messages=[{'role': 'user', 'content': '''$prompt'''}]
    )

    # Extract the commit message
    content = message.content
    if content and len(content) > 0:
        if isinstance(content[0], dict) and 'text' in content[0]:
            print(content[0]['text'])
        else:
            print('Update project files')
    else:
        print('Update project files')
except Exception as e:
    print('Update project files')
    sys.exit(0)
")
    else
        # Fallback to a simple commit message
        print_message "$YELLOW" "No AI providers available. Using default commit message."
        commit_message="Update project files"
    fi

    # Filter out debug messages and return the clean commit message
    # Remove lines containing debug messages and AI responses that aren't proper commit messages
    filtered_message=$(echo "$commit_message" |
        grep -v "Generating AI commit message" |
        grep -v "Using project's AI integration utilities" |
        grep -v "Certainly!" |
        grep -v "I'll need" |
        grep -v "In order to generate" |
        grep -v "I need more information" |
        grep -v "Please provide more details")

    # If filtering removed everything or the message is asking for more information, use a default message
    if [ -z "$filtered_message" ] || echo "$filtered_message" | grep -q "need more information"; then
        echo "Update project files"
    else
        # Trim leading and trailing whitespace
        filtered_message=$(echo "$filtered_message" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
        echo "$filtered_message"
    fi
}

# Banner
print_message "$GREEN" "================================================================"
print_message "$GREEN" "                  AI-ASSISTED COMMIT WORKFLOW                   "
print_message "$GREEN" "================================================================"

# Check for required commands
check_required_commands

# Load environment variables from .env file
if command_exists poetry && poetry run python -c "from dotenv import load_dotenv; load_dotenv(); print('OK')" 2>/dev/null | grep -q "OK"; then
    print_message "$YELLOW" "Loaded environment variables from .env file."
    
    # Check if DeepSeek API key is set
    DEEPSEEK_API_KEY=$(poetry run python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.environ.get('DEEPSEEK_API_KEY', ''))")
    DEEPSEEK_MODEL=$(poetry run python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.environ.get('DEEPSEEK_MODEL', 'deepseek-chat'))")
    
    if [ -z "$DEEPSEEK_API_KEY" ]; then
        print_message "$YELLOW" "⚠️ Warning: DeepSeek API key not found in .env file."
    else
        print_message "$GREEN" "✅ DeepSeek API key found."
        print_message "$GREEN" "   Using model: $DEEPSEEK_MODEL"
    fi
else
    print_message "$YELLOW" "⚠️ Warning: Could not load environment variables from .env file."
fi

# Step 1: Clean up and add specific files for this commit
print_message "$BLUE" "📋 Step 1: Cleaning up and adding specific files for this commit"

# Clean up any problematic files
print_message "$YELLOW" "Cleaning up problematic files..."
rm -f ai-docs/*.bak ai-docs/*.tmp mypy_report.txt pylint_report.txt
git rm --cached ai-docs/*.bak 2>/dev/null || true
git rm --cached ai-docs/*.tmp 2>/dev/null || true
git rm --cached mypy_report.txt 2>/dev/null || true
git rm --cached pylint_report.txt 2>/dev/null || true

# Add only the files we created/modified
print_message "$YELLOW" "Adding workflow files..."
git add scripts/ai_commit_workflow.sh
git add .vscode/tasks.json
git add ai-docs/git_workflow.md
git add scripts/aboutthisfolder.md
git add .gitignore

print_message "$GREEN" "Files added successfully"

# Step 2: Run focused documentation update
print_message "$BLUE" "📚 Step 2: Running focused documentation update"

# Update only specific documentation files
print_message "$YELLOW" "Updating git_workflow.md..."
if ! grep -q "AI-assisted commit workflow" ai-docs/git_workflow.md; then
    print_message "$RED" "❌ Documentation update check failed. Please fix the issues before committing."
    exit 1
fi

print_message "$YELLOW" "Updating scripts/aboutthisfolder.md..."
if ! grep -q "ai_commit_workflow.sh" scripts/aboutthisfolder.md; then
    print_message "$RED" "❌ Documentation update check failed. Please fix the issues before committing."
    exit 1
fi

print_message "$GREEN" "Documentation checks passed"

# Add any documentation changes
print_message "$BLUE" "📎 Adding documentation changes to git"
git add ai-docs/git_workflow.md
git add scripts/aboutthisfolder.md

# Step 3: Run full linting and code quality checks
print_message "$BLUE" "🔍 Step 3: Running full linting and code quality checks"

# First, remove any backup or temporary files that might cause issues
print_message "$YELLOW" "Removing backup and temporary files..."
rm -f ai-docs/*.bak ai-docs/*.tmp mypy_report.txt pylint_report.txt

# Create a temporary pre-commit config without the documentation hook
if [ -f ".config/.pre-commit-config.yaml.no-docs" ]; then
    cp .pre-commit-config.yaml .pre-commit-config.yaml.bak
    cp .config/.pre-commit-config.yaml.no-docs .pre-commit-config.yaml
    RESTORE_CONFIG=true
else
    print_message "$YELLOW" "Warning: .config/.pre-commit-config.yaml.no-docs not found. Using default config."
    RESTORE_CONFIG=false
fi

# Function to run a specific linter
run_linter() {
    local linter=$1
    local description=$2
    local success=false
    local attempt=1
    local max_attempts=2

    while [ $attempt -le $max_attempts ] && [ "$success" = "false" ]; do
        print_message "$YELLOW" "Running $description (attempt $attempt/$max_attempts)..."

        if poetry run pre-commit run $linter --all-files; then
            print_message "$GREEN" "✅ $description passed!"
            success=true
        else
            if [ $attempt -lt $max_attempts ]; then
                print_message "$YELLOW" "⚠️ $description failed. Attempting to fix issues automatically..."

                case $linter in
                    black)
                        poetry run black .
                        ;;
                    isort)
                        poetry run isort .
                        ;;
                    ruff)
                        poetry run ruff --fix .
                        ;;
                    flake8)
                        # No auto-fix for flake8
                        ;;
                    mypy)
                        # No auto-fix for mypy
                        ;;
                    pylint)
                        # No auto-fix for pylint
                        ;;
                esac

                # Re-add files after auto-fixing
                git add .
            else
                print_message "$RED" "❌ $description failed after $max_attempts attempts."
                return 1
            fi
        fi

        attempt=$((attempt + 1))
    done

    return 0
}

# Run each linter individually
LINTING_FAILED=false

# 1. Black (code formatting)
if ! run_linter "black" "Black code formatting"; then
    LINTING_FAILED=true
fi

# 2. isort (import sorting)
if ! run_linter "isort" "isort import sorting"; then
    LINTING_FAILED=true
fi

# 3. ruff (linting)
if ! run_linter "ruff" "Ruff linting"; then
    LINTING_FAILED=true
fi

# 4. flake8 (linting)
if ! run_linter "flake8" "Flake8 linting"; then
    LINTING_FAILED=true
fi

# 5. mypy (type checking)
if ! run_linter "mypy" "mypy type checking"; then
    LINTING_FAILED=true
fi

# 6. pylint (comprehensive linting)
print_message "$YELLOW" "Running Pylint comprehensive linting..."
pylint_output=$(poetry run pylint --rcfile=.config/pylintrc --ignore=.venv,venv,build,dist src tests scripts 2>&1)
pylint_exit_code=$?

# Extract the score from pylint output
pylint_score=$(echo "$pylint_output" | grep -oP 'Your code has been rated at \K[0-9.]+')

if [ -z "$pylint_score" ]; then
    pylint_score="0.0"
fi

print_message "$YELLOW" "Pylint score: $pylint_score/10.0"

# Check if pylint score is acceptable (>= 9.0)
# Using awk for floating-point comparison instead of bc
if awk "BEGIN {exit !($pylint_score >= 9.0)}"; then
    print_message "$GREEN" "✅ Pylint check passed (score >= 9.0)!"
else
    print_message "$RED" "❌ Pylint score is below 9.0."
    LINTING_FAILED=true
fi

# Restore original pre-commit config if needed
if [ "$RESTORE_CONFIG" = "true" ]; then
    mv .pre-commit-config.yaml.bak .pre-commit-config.yaml
fi

# Handle linting failures
if [ "$LINTING_FAILED" = "true" ]; then
    print_message "$RED" "❌ Some linting checks failed."
    print_message "$YELLOW" "You can:"
    print_message "$YELLOW" "1. Fix the issues and run the workflow again"
    print_message "$YELLOW" "2. Continue anyway (not recommended)"

    read -p "Do you want to continue anyway? (y/n): " ignore_linting
    if [[ "$ignore_linting" != "y" && "$ignore_linting" != "Y" ]]; then
        print_message "$RED" "Aborting commit due to linting failures."
        exit 1
    else
        print_message "$YELLOW" "⚠️ Continuing despite linting failures."
    fi
else
    print_message "$GREEN" "✅ All linting and code quality checks passed!"
fi

# Step 4: Generate AI commit message
print_message "$BLUE" "💭 Step 4: Generating commit message"

# Generate the commit message without the colored output
COMMIT_MESSAGE=$(generate_ai_commit_message)

# Display the commit message
print_message "$GREEN" "Generated commit message: "
echo ""
echo "$COMMIT_MESSAGE" | sed 's/^/    /'
echo ""

# Ask user if they want to edit the commit message
print_message "$YELLOW" "Do you want to edit this commit message? (y/n): "
read -r edit_message
if [[ "$edit_message" == "y" || "$edit_message" == "Y" ]]; then
    # Create a temporary file with the commit message
    TEMP_FILE=$(mktemp)
    echo "$COMMIT_MESSAGE" > "$TEMP_FILE"

    # Open the file in the default editor
    if [ -n "$EDITOR" ]; then
        $EDITOR "$TEMP_FILE"
    elif command_exists nano; then
        nano "$TEMP_FILE"
    elif command_exists vim; then
        vim "$TEMP_FILE"
    elif command_exists vi; then
        vi "$TEMP_FILE"
    else
        print_message "$YELLOW" "No editor found. Using the generated message."
    fi

    # Read the edited message
    COMMIT_MESSAGE=$(cat "$TEMP_FILE")
    rm "$TEMP_FILE"

    print_message "$GREEN" "Using edited commit message."
else
    print_message "$GREEN" "Using AI-generated commit message."
fi

# Step 5: Commit changes (bypassing hooks)
print_message "$BLUE" "✅ Step 5: Committing changes (bypassing hooks)"

# Temporarily disable post-commit hook to prevent documentation update loop
if [ -f ".git/hooks/post-commit" ]; then
    print_message "$YELLOW" "Temporarily disabling post-commit hook..."
    mv .git/hooks/post-commit .git/hooks/post-commit.bak
    POST_COMMIT_DISABLED=true
else
    POST_COMMIT_DISABLED=false
fi

# Run documentation update manually first
print_message "$YELLOW" "Running documentation update before commit..."
if [ -f "./scripts/update_documentation.sh" ]; then
    ./scripts/update_documentation.sh
    # Add any files that were modified by the documentation update
    git add .
fi

# Clean up the commit message one more time to ensure it's properly formatted
# Remove any remaining debug messages and ensure proper formatting
CLEAN_COMMIT_MESSAGE=$(echo "$COMMIT_MESSAGE" |
    grep -v "🤖" |
    grep -v "Using project's" |
    grep -v "Certainly" |
    grep -v "I'll" |
    grep -v "need more information" |
    sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')

# If the message is empty after cleaning, use a default message
if [ -z "$CLEAN_COMMIT_MESSAGE" ]; then
    CLEAN_COMMIT_MESSAGE="Update project files"
fi

# Commit changes with --no-verify to bypass pre-commit hooks
# This is necessary because the documentation hook would run again otherwise
print_message "$YELLOW" "Committing with --no-verify to avoid documentation hook loop..."
git commit --no-verify -m "$CLEAN_COMMIT_MESSAGE"

# Restore post-commit hook if it was disabled
if [ "$POST_COMMIT_DISABLED" = "true" ]; then
    print_message "$YELLOW" "Restoring post-commit hook..."
    mv .git/hooks/post-commit.bak .git/hooks/post-commit
fi

# Step 6: Push changes
print_message "$BLUE" "🚀 Step 6: Pushing changes"

# Get list of remotes
REMOTES=$(git remote)

# Function to handle pushing to a remote
push_to_remote() {
    local remote=$1
    local force_push=$2

    if [[ "$force_push" == "true" ]]; then
        print_message "$PURPLE" "Force pushing to $remote..."
        if ! git push --force $remote; then
            print_message "$YELLOW" "⚠️ Force push to $remote failed. This might be due to branch protection."
            print_message "$YELLOW" "Trying normal push instead..."
            if ! git push $remote; then
                print_message "$YELLOW" "⚠️ Normal push to $remote also failed, continuing anyway..."
            fi
        fi
    else
        print_message "$PURPLE" "Pushing to $remote..."
        if ! git push $remote; then
            print_message "$YELLOW" "⚠️ Push to $remote failed, continuing anyway..."
        fi
    fi
}

# Ask if force push is needed
print_message "$YELLOW" "Do you need to force push? (Only use if you've rewritten git history)"
read -p "Force push? (y/n): " force_push_choice
if [[ "$force_push_choice" == "y" || "$force_push_choice" == "Y" ]]; then
    FORCE_PUSH=true
else
    FORCE_PUSH=false
fi

# Check if both GitLab and GitHub remotes exist
if echo "$REMOTES" | grep -q "gitlab" && echo "$REMOTES" | grep -q "github"; then
    # Push to GitHub first (usually less restrictive)
    push_to_remote "github" "$FORCE_PUSH"

    # For GitLab, ask if it has branch protection
    if [[ "$FORCE_PUSH" == "true" ]]; then
        print_message "$YELLOW" "GitLab often has branch protection enabled on main branches."
        read -p "Does GitLab have branch protection enabled? (y/n): " gitlab_protected

        if [[ "$gitlab_protected" == "y" || "$gitlab_protected" == "Y" ]]; then
            print_message "$YELLOW" "Skipping force push to GitLab. You have these options:"
            print_message "$YELLOW" "1. Temporarily disable branch protection in GitLab settings"
            print_message "$YELLOW" "2. Create a new branch and merge it via GitLab's interface"
            print_message "$YELLOW" "3. Push to GitLab without force (may fail if history was rewritten)"

            read -p "Try normal push to GitLab anyway? (y/n): " try_gitlab_push
            if [[ "$try_gitlab_push" == "y" || "$try_gitlab_push" == "Y" ]]; then
                push_to_remote "gitlab" "false"
            else
                print_message "$YELLOW" "Skipping push to GitLab"
            fi
        else
            push_to_remote "gitlab" "$FORCE_PUSH"
        fi
    else
        push_to_remote "gitlab" "false"
    fi
else
    # Push to origin
    push_to_remote "origin" "$FORCE_PUSH"
fi

print_message "$GREEN" "✨ Push completed (any errors are shown above)"

print_message "$GREEN" "================================================================"
print_message "$GREEN" "✨ AI-assisted commit workflow completed successfully!"
print_message "$GREEN" "================================================================"
