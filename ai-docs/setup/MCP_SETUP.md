# MCP Configuration Setup Guide

This document provides instructions for setting up the Model Context Protocol (MCP) configuration for this project.

## Setting Up `.vscode/mcp.json`

For security reasons, the `.vscode/mcp.json` file is not tracked in Git. Instead, use the template provided in this repository:

1. Copy the template file to create your local configuration:

   ```bash
   cp .vscode/mcp.json.template .vscode/mcp.json
   ```

2. Create your `.env` file with API keys (use our helper script):

   ```bash
   ./scripts/setup_env_template.sh     # Creates .env.template
   cp .env.template .env               # Copy to your actual .env file
   ```

3. Edit the `.env` file to add your actual API keys:

   ```properties
   # API Keys for AI Providers
   OPENAI_API_KEY=your_key_here
   ANTHROPIC_API_KEY=your_key_here
   PERPLEXITY_API_KEY=your_key_here
   # ... other keys
   ```

4. The MCP configuration automatically reads from your `.env` file when VS Code is started.

## Security Considerations

- **NEVER commit API keys directly in any file**
- All API keys and sensitive values should be stored in your local `.env` file
- The `.env` file is included in `.gitignore` to prevent accidental exposure
- Your `.vscode/mcp.json` file will also be ignored by Git

### Keeping Secrets Safe

We have implemented several measures to prevent accidental exposure of API keys:

1. **Environment Variables**: All secrets are stored in `.env` files which are ignored by Git
2. **Template Files**: Configuration templates are provided without actual keys
3. **Git Ignore Rules**: Both `.env` and `.vscode/mcp.json` are in `.gitignore`
4. **Secret Scanning**: We use `detect-secrets` to scan for accidentally committed secrets

### What To Do If You Accidentally Commit Secrets

If you accidentally commit secrets to this repository:

1. **Immediately revoke and rotate the exposed keys**
2. **Remove the secrets from Git history**:

   ```bash
   ./scripts/remove_sensitive_file.sh path/to/file/with/secrets
   ```

3. **Force push to all remotes**:

   ```bash
   git push github --force
   git push gitlab --force
   ```

4. **Notify relevant team members**

## Required API Keys and Configuration Values

The following keys are used by various MCP servers in the project:

| Variable | Purpose | Where to Get It |
|----------|---------|-----------------|
| `OPENAI_API_KEY` | OpenAI API access | [OpenAI Platform](https://platform.openai.com/) |
| `ANTHROPIC_API_KEY` | Anthropic Claude models | [Anthropic Console](https://console.anthropic.com/) |
| `PERPLEXITY_API_KEY` | Perplexity AI | [Perplexity Labs](https://www.perplexity.ai/settings/api) |
| `DEEPSEEK_API_KEY` | DeepSeek models | [DeepSeek Platform](https://platform.deepseek.com/) |
| `GOOGLE_API_KEY` | Google AI services | [Google AI Studio](https://aistudio.google.com/) |
| `BRIGHTDATA_API_KEY` | Web scraping | [Bright Data](https://brightdata.com/) |
| `SMITHERY_CLI_KEY` | Smithery CLI access | [Smithery Dashboard](https://smithery.dev/) |

## Troubleshooting

If you encounter issues with MCP servers not connecting:

1. Verify your `.env` file contains all required keys
2. Check that your API keys are valid and not expired
3. Ensure VS Code has properly loaded the environment variables
4. Restart VS Code if you've recently updated your `.env` file

For more help, please contact the project maintainer.
