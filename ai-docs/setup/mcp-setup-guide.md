# MCP Setup Guide

This document explains how the Model Context Protocol (MCP) is set up in this project and how to troubleshoot common issues.

## Overview

The project uses several AI services through the Model Context Protocol (MCP):

1. **GitHub MCP Server**: For repository management
2. **Context7**: For documentation lookup
3. **Perplexity**: For research and information retrieval
4. **AI Task Master**: For task management
5. **Bright Data**: For web scraping

## Configuration Files

The MCP configuration is spread across several files:

1. `.vscode/mcp.json`: Main configuration file for MCP servers
2. `.vscode/mcp-secrets.json`: Stores API keys and other secrets
3. `.env`: Environment variables for API keys and model names
4. `create_python_project.code-workspace`: VS Code workspace settings

## Perplexity MCP Setup

The Perplexity MCP server requires the `PERPLEXITY_API_KEY` environment variable to be available when running the server. This is configured in two ways:

1. **Via mcp-secrets.json**: The API key is stored in `.vscode/mcp-secrets.json` as `perplexity-key`
2. **Via environment variables**: The MCP configuration references `${input:perplexity-key}` which will use the value from mcp-secrets.json

## Troubleshooting

### Perplexity MCP Not Working

If the Perplexity MCP server isn't working:

1. **Check API Key**: Verify your Perplexity API key is correct in `.env` and `.vscode/mcp-secrets.json`
2. **Test Direct API Access**: Run `./scripts/check_ai_services.sh` to test direct API access
3. **Test MCP Server**: Run `./scripts/run_perplexity_mcp.sh` to test the MCP server with environment variables loaded
4. **Restart VS Code**: Sometimes restarting VS Code helps load the latest configuration
5. **Check VS Code Output**: Open the Output panel (View > Output) and select "MCP" to see error messages

### Manual Testing

You can manually test the Perplexity API with:

```bash
# Load environment variables and run the MCP server
./scripts/run_perplexity_mcp.sh

# Or directly with:
export $(grep -v '^#' .env | xargs) && npx -y server-perplexity-ask
```

## Last Updated

This documentation was created on: 2025-05-20
