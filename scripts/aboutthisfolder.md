<!-- filepath: /home/michaelnewham/bin/python_projects/create_python_project/scripts/aboutthisfolder.md -->
# Scripts Folder

Utility scripts for the Create Python Project.

## Purpose

Contains helper scripts for development, documentation, and automation tasks.

## Structure

```
scripts/
├── aboutthisfolder.md
├── ai_commit_workflow.sh
├── commit_with_docs_fix.sh
├── commit_with_docs.sh
├── create_gitlab_branch.sh
├── fix_lint_issues.sh
├── fix_pylint_issues.sh
├── post_commit_push.sh
├── remove_large_file.sh
├── run_mypy.sh
├── truncate_md_files.sh
├── update_documentation.sh
```

## Script Descriptions

- **ai_commit_workflow.sh**: AI-assisted commit workflow that generates commit messages using AI based on your changes
- **commit_with_docs.sh**: Commits changes with documentation updates (skips pylint)
- **commit_with_docs_fix.sh**: Commits changes with documentation updates (interactive mode)
- **create_gitlab_branch.sh**: Creates a new branch for GitLab when branch protection is enabled
- **fix_lint_issues.sh**: Automatically fixes common linting issues
- **fix_pylint_issues.sh**: Automatically fixes common pylint issues
- **post_commit_push.sh**: Pushes changes to all configured remotes after a commit
- **remove_large_file.sh**: Removes a large file from git history (use with caution)
- **run_mypy.sh**: Runs mypy type checking with proper configuration
- **truncate_md_files.sh**: Limits all markdown files to 150 lines maximum
- **update_documentation.sh**: Updates all project documentation

## Last Updated

This documentation was automatically generated on: 2025-05-14 21:00:01
