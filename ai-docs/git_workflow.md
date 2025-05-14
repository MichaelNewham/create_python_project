# Advanced Git Workflow

This document describes the advanced Git workflow setup for the Create Python Project repository.

## Components

1. **Pre-commit hooks (.pre-commit-config.yaml)**: Run automatically before each commit to format code, run linters, and generate documentation.
2. **Post-commit hook (.post-commit-config.yaml)**: Runs after each commit to stage any generated documentation, create a follow-up commit, and push changes to all remotes.
3. **AI-assisted commit workflow (scripts/ai_commit_workflow.sh)**: Generates commit messages using AI based on the changes made.
4. **VS Code tasks**: Provides convenient ways to run the entire workflow from VS Code.

## Configuration Files

### Pre-commit Configuration (.pre-commit-config.yaml)

The pre-commit configuration file controls which hooks run before each commit. The current setup includes:

- Code formatting with Black and isort
- Linting with flake8, mypy, and ruff
- Documentation generation with our custom script

### Post-commit Configuration (.post-commit-config.yaml)

The post-commit configuration file controls what happens after each commit. Options include:

- `auto_stage`: Whether to automatically stage documentation changes (default: true)
- `auto_commit`: Whether to create a separate commit for documentation (default: true)
- `auto_push`: Whether to push changes automatically (default: true)
- `doc_commit_message`: The commit message for documentation updates
- `push_all`: Whether to push to all remotes (default: true)
- `run_tests`: Whether to run tests after commit (default: false)
- `build_package`: Whether to build the package after commit (default: false)
- `notify`: Whether to send a notification after pushing (default: false)

## Workflow Steps

When you make changes to the repository, the workflow proceeds as follows:

1. You stage your changes with `git add`
2. Pre-commit hooks run:
   - Code formatters (Black, isort) fix any style issues
   - Linters (flake8, mypy, ruff) check for code quality issues
   - Documentation generator updates all documentation files
3. **If any pre-commit hook fails, the workflow stops** and you need to fix the issues before continuing
4. If all hooks pass, your commit is created
5. The post-commit hook automatically:
   - Runs tests (if configured)
   - Builds the package (if configured)
   - Stages any newly generated documentation files (if `auto_stage: true`)
   - Creates a separate commit for documentation changes (if `auto_commit: true`)
   - Pushes all changes to GitHub and GitLab (if `auto_push: true`)
6. **If any step in the post-commit process fails, it will stop with an error message**

## Using the VS Code Tasks

### AI-Assisted Commit Workflow (Recommended)

The AI-assisted commit workflow automates the entire process and generates intelligent commit messages:

1. Press `Ctrl+P` (or `Cmd+P` on Mac)
2. Type `>Tasks: Run Task`
3. Select "AI Commit Workflow"

The task will:
- Stage all changes
- Run documentation update
- Run pre-commit hooks (formatting, linting)
- Generate a commit message using AI based on your changes
- Allow you to review and optionally edit the AI-generated message
- Commit with the final message
- Push to all configured remotes (GitHub and GitLab)

### Standard Commit Workflow

If you prefer to write your own commit messages, you can use the standard workflow:

1. Press `Ctrl+P` (or `Cmd+P` on Mac)
2. Type `>Tasks: Run Task`
3. Select "Check, Commit, Push"
4. Enter a commit message when prompted

The task will:
- Stage all changes
- Run pre-commit hooks (formatting, linting, documentation)
- Create a commit with your message
- Run the post-commit hook to handle documentation updates and pushing

## Manual Workflow

If you prefer to run the workflow manually:

1. Stage your changes: `git add .`
2. Run pre-commit hooks: `pre-commit run --all-files`
3. Commit your changes: `git commit -m "Your message"`
4. The post-commit hook will automatically run and handle the rest

## Customizing the Workflow

To customize the workflow:

1. Edit `.pre-commit-config.yaml` to change pre-commit behavior
2. Edit `.post-commit-config.yaml` to change post-commit behavior
3. Edit `.vscode/tasks.json` to modify VS Code tasks

## Troubleshooting

If you encounter issues with the workflow:

1. **Pre-commit hook failures**:
   - The workflow will stop with an error message
   - Fix the issues reported by the pre-commit hooks (formatting, linting, etc.)
   - Run `pre-commit run --all-files` to verify that all issues are fixed
   - Then run the workflow again

2. **Test failures**:
   - If tests are configured to run and they fail, the post-commit process will stop
   - Check the test output for details on what failed
   - Fix the issues and try again

3. **Push failures**:
   - If pushing to remotes fails, you may need to pull changes first
   - Run `git pull --rebase` to incorporate remote changes
   - Resolve any conflicts and try again

4. **Documentation generation issues**:
   - Check the output of the update_documentation.sh script
   - Look for specific error messages about missing files or paths
   - Check if any sensitive information was detected that might be causing issues

## Last Updated

This documentation was updated on: 2025-05-14
