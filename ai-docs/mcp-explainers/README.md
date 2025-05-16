# MCP Explainers

This directory contains documentation and explanatory guides for Model Context Protocol (MCP) tools used in this project.

## Contents

- [Task Master Tools Guide](task_master_tools_guide.md) - A comprehensive guide to Task Master tools available through MCP, organized by function with example questions.
- [GitHub Copilot Tools Guide](github-copilot.md) - A guide to GitHub Copilot's capabilities for code generation, understanding, and task automation.
- [GitHub Versioning with MCP Tools Guide](github-versioning.md) - A focused guide on GitHub versioning and repository management tools available through the GitHub MCP Server.
- [Context7 Tools Guide](context7.md) - A guide to using Context7 for retrieving relevant documentation and code examples from libraries and frameworks.
- [Perplexity Tools Guide](perplexity.md) - A guide to using Perplexity as an AI research assistant to find accurate, up-to-date information.
- [PromptBoost Tools Guide](promptboost.md) - A guide to enhancing your prompts to get better AI-generated code and responses.

## MCP Server & Tool Count Overview

Each guide corresponds to a specific capability or MCP server in our configuration:

| Guide | MCP Server/Integration | Tools Count | Primary Purpose |
|-------|------------------------|-------------|-----------------|
| Task Master | AI-Task-Master | 24 tools | Task management and project organization |
| GitHub Copilot | VS Code Native | Native VS Code tools | Code generation and assistance |
| GitHub Versioning | github | 36 tools with `f1e_` prefix | GitHub repository and version control |
| Context7 | context7 | 2 tools | Library and framework documentation |
| Perplexity | Perplexity | 1 tool | AI research assistant |
| PromptBoost | VS Code Extension | 1 tool | Improving prompt quality and effectiveness |

## Tools Distribution

- **GitHub MCP Server** (36 tools): Repository management, branch operations, commits, PRs, issues, security scanning
- **Context7** (2 tools): `f1e_resolve-library-id` and `f1e_get-library-docs`
- **Perplexity** (1 tool): `f1e_perplexity_ask`
- **AI Task Master** (24 tools): Task initialization, management, dependencies, expansion, analysis
- **VS Code Native/GitHub Copilot**: File operations, searching, testing, terminal operations (not configured in mcp.json)
- **PromptBoost** (1 tool): `promptBoost` for enhancing prompts with better structure, specificity and technical context

## Purpose

The explainers in this directory help developers understand how to effectively use Model Context Protocol tools to manage, organize, and automate various aspects of the project development workflow.

Each guide provides:
- Clear examples of when to use each tool
- Sample questions that would trigger the use of a specific tool
- Tool names and their primary purposes
- Logical categorization of related tools

## Last Updated

This directory was last updated on: 2025-05-16
