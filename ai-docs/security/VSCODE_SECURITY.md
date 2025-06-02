# VS Code Settings Security Guide

This document outlines best practices for handling sensitive information in VS Code settings.

## Sensitive Information in VS Code Settings

VS Code settings files can contain sensitive information like API keys and tokens. To ensure security:

1. **Never commit sensitive information to git repositories**
2. **Always use environment variables for secrets**

## Settings Files Setup

### Using `.vscode/settings.json.template`

We provide a template file that shows how to set up VS Code settings without hardcoded secrets:

```bash
# Copy the template to create your local settings
cp .vscode/settings.json.template .vscode/settings.json
```

### Environment Variables for Secrets

All secrets should be stored in your `.env` file:

```
# API Keys for various services
BRIGHTDATA_API_KEY=your_brightdata_api_key_here
# Other API keys...
```

### Accessing Environment Variables in VS Code Settings

If you need to reference secrets in VS Code settings, use environment variable references:

```jsonc
{
    // Example: Reference environment variable
    "myExtension.apiKey": "${env:BRIGHTDATA_API_KEY}"
}
```

## Removed Secrets

The following secrets have been removed from tracked files and should be stored in `.env`:

1. `BRIGHTDATA_API_KEY` - Previously hardcoded in settings.json as `mcp-secrets.brightdata.API_TOKEN`

## Git Security

The following files are ignored in Git to prevent accidental exposure of secrets:

- `.env`
- `.vscode/settings.json`
- `.vscode/mcp.json`

## What to Do If Secrets Are Exposed

If you accidentally commit sensitive information to a repository:

1. **Immediately revoke the exposed credentials**
2. **Generate new credentials**
3. **Use the `scripts/remove_sensitive_file.sh` script to remove the file from git history**
4. **Force push to remote repositories**
