<!-- filepath: /home/michaelnewham/Projects/create_python_project/scripts/aboutthisfolder.md -->
# Scripts Folder

Documentation for the scripts directory.

## Directory Structure

```
scripts/
├── ai_commit_workflow.sh
├── check_ai_services.sh
├── check_gitlab_connection.sh
├── check_perplexity_config.sh
├── clean_run.py
├── commit_with_docs_fix.sh
├── commit_with_docs.sh
├── create_gitlab_branch.sh
├── deepseek_commit_message.py
├── .doc_history
├── download_pexels_image.sh
├── fix_lint_issues.sh
├── fix_specific_lint_issues.py
├── force_push_to_remotes.sh
├── github_mcp_fix_summary.sh
├── lint_all.py
├── lint_src.py
├── manage_docs.sh
├── manage_logs.sh
├── mcp_config_summary.sh
├── pexels_instructions.sh
├── post_commit_push.sh
├── remove_large_file.sh
├── remove_sensitive_file.sh
├── run_app.sh
├── run_mypy.sh
├── run_perplexity_mcp.sh
├── run_perplexity_mcp.sh.bak
├── setup_doc_watcher.sh
├── setup_env_template.sh
├── setup_mcp.sh
├── sync_mcp_config.sh
├── test_mcp
├── test_new_file.sh
├── truncate_md_files.sh
├── update_documentation.sh
├── update_documentation.sh.bak
├── update_perplexity_mcp.sh
├── verify_security.sh
```

## Contents Description

- `ai_commit_workflow.sh`: AI-assisted commit workflow script
- `check_ai_services.sh`: This script checks the connection to Context7 and Perplexity services
- `check_gitlab_connection.sh`: This script checks the connection to GitLab and provides troubleshooting information
- `check_perplexity_config.sh`: This script checks if the Perplexity API key exists in the global .env file
- `clean_run.py`: !/usr/bin/env python3
- `commit_with_docs_fix.sh`: Script to update documentation and commit changes without running into pre-commit loops
- `commit_with_docs.sh`: Script to commit changes with documentation updates
- `create_gitlab_branch.sh`: Script to create a new branch for GitLab when branch protection is enabled
- `deepseek_commit_message.py`: !/usr/bin/env python3
- `.doc_history`: ASCII text, with very long lines (816)
- `download_pexels_image.sh`: Script to download an image from Pexels using curl
- `fix_lint_issues.sh`: Quick script to fix common linting issues in the codebase
- `fix_specific_lint_issues.py`: !/usr/bin/env python
- `force_push_to_remotes.sh`: This script bypasses pre-commit hooks and pushes to both GitHub and GitLab
- `github_mcp_fix_summary.sh`: GitHub MCP Server Configuration Fix Summary
- `lint_all.py`: !/usr/bin/env python3
- `lint_src.py`: !/usr/bin/env python3
- `manage_docs.sh`: Documentation management script
- `manage_logs.sh`: Log management script with improved handling and documentation
- `mcp_config_summary.sh`: Summary of MCP Configuration Changes - 2025-05-31
- `pexels_instructions.sh`: Get image location from Pexels API
- `post_commit_push.sh`: This script runs after a successful commit
- `remove_large_file.sh`: Script to remove a large file from git history
- `remove_sensitive_file.sh`: Script to remove sensitive files from git repository history
- `run_app.sh`: Script to run the main application without showing virtual environment activation messages
- `run_mypy.sh`: This script is a wrapper for mypy that VS Code can use
- `run_perplexity_mcp.sh`: This script runs the Perplexity MCP server with environment variables from .env
- `run_perplexity_mcp.sh.bak`: Bourne-Again shell script, Unicode text, UTF-8 text executable
- `setup_doc_watcher.sh`: Setup script for documentation watcher service
- `setup_env_template.sh`: Script to create a clean .env template file with all required variables
- `setup_mcp.sh`: Setup MCP configuration
- `sync_mcp_config.sh`: Script to sync MCP configuration between VS Code and Cursor IDE
- `test_mcp/`: Directory containing 1 items
- `test_new_file.sh`: No description available
- `truncate_md_files.sh`: Script to immediately truncate all markdown files to 150 lines maximum
- `update_documentation.sh`: This script generates comprehensive documentation for the create_python_project package
- `update_documentation.sh.bak`: Bourne-Again shell script, Unicode text, UTF-8 text executable
- `update_perplexity_mcp.sh`: Script to update the run_perplexity_mcp.sh to use the global .env file
- `verify_security.sh`: Quick security verification script

## Change History

update_documentation.sh.bak
update_perplexity_mcp.sh
verify_security.sh
Wed 04 Jun 2025 13:39:16 IST: ADDED: ai_commit_workflow.sh check_ai_services.sh check_gitlab_connection.sh check_perplexity_config.sh clean_run.py commit_with_docs_fix.sh commit_with_docs.sh create_gitlab_branch.sh deepseek_commit_message.py download_pexels_image.sh fix_lint_issues.sh fix_specific_lint_issues.py force_push_to_remotes.sh github_mcp_fix_summary.sh lint_all.py lint_src.py manage_docs.sh manage_logs.sh mcp_config_summary.sh pexels_instructions.sh post_commit_push.sh remove_large_file.sh remove_sensitive_file.sh run_app.sh run_mypy.sh run_perplexity_mcp.sh run_perplexity_mcp.sh.bak setup_doc_watcher.sh setup_env_template.sh setup_mcp.sh sync_mcp_config.sh test_mcp test_new_file.sh truncate_md_files.sh update_documentation.sh update_documentation.sh.bak update_perplexity_mcp.sh verify_security.sh 
Wed 04 Jun 2025 13:39:16 IST: REMOVED:                                      00:12 01:03 01:40 03:59 07:49 10:04 12:47 14:39 16:44 2025: 2025: 2025: 2025: 2025: 2025: 2025: 2025: 2025: 20:32 20:43 21:58 25:14 25:17 26:36 27:14 28:57 29:01 30:04 30:30 30:49 32:45 34:49 36:18 37:40 39:59 40:37 42:34 43:09 45:04 45:06 48:15 49:48 50:06 51:13 52:04 53:12 59:41 FILES:ai_commit_workflow.sh IST IST IST IST IST IST IST IST IST IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: IST: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: REMOVED: 

## Last Updated

This documentation was automatically generated on: 2025-06-04 13:39:15
