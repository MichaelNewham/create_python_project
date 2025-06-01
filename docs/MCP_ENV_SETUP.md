# MCP Environment Setup for Multiple IDEs

This document provides instructions for setting up and maintaining Model Context Protocol (MCP) configurations across multiple IDEs, specifically VS Code and Cursor.

## Overview

Since you're using both VS Code and Cursor IDEs with a global `.env` file located at `/home/michaelnewham/Projects/.env`, this setup ensures consistent MCP server configurations across both development environments.

## The Problem

The error logs show that the Perplexity MCP server is failing to initialize with the error:

```plaintext
Error: PERPLEXITY_API_KEY environment variable is required
```

This happens because:

1. The `.env` file is being loaded from the project directory, not from the global location
2. VS Code and Cursor have separate MCP configurations that need to be synchronized

## Solution

We've created three scripts to address these issues:

### 1. Sync MCP Configurations Between IDEs

The `sync_mcp_config.sh` script:

- Creates a symbolic link from your project's `.env` to the global `.env` file
- Syncs MCP configurations between VS Code and Cursor
- Ensures both IDEs use the same configuration files

```bash
./scripts/sync_mcp_config.sh
```

### 2. Update Perplexity MCP Runner

The `update_perplexity_mcp.sh` script:

- Updates the `run_perplexity_mcp.sh` script to use the global `.env` file location
- Backs up the original script before making changes

```bash
./scripts/update_perplexity_mcp.sh
```

### 3. Check Perplexity MCP Configuration

The `check_perplexity_config.sh` script:

- Verifies that the `PERPLEXITY_API_KEY` exists in the global `.env` file
- Checks that MCP configuration files are properly set up
- Provides guidance on next steps if issues are found

```bash
./scripts/check_perplexity_config.sh
```

## Setup Instructions

Follow these steps in order:

1. First, check your Perplexity configuration:

```bash
./scripts/check_perplexity_config.sh
```

1. If issues are found, sync your MCP configurations:

```bash
./scripts/sync_mcp_config.sh
```

1. Update the Perplexity MCP runner:

```bash
./scripts/update_perplexity_mcp.sh
```

1. Test the Perplexity MCP server:

```bash
./scripts/run_perplexity_mcp.sh
```

## MCP Server Configuration Best Practices

For environments with multiple IDEs and a global `.env` file:

1. **Use symbolic links** to reference the global `.env` file
2. **Keep configurations in sync** between IDEs
3. **Use absolute paths** in scripts and configurations
4. **Check environment variables** at startup
5. **Provide clear error messages** when required variables are missing

## Troubleshooting

If issues persist:

1. **Check the API key** in the global `.env` file
2. **Restart the IDEs** after making configuration changes
3. **Verify permissions** on the symbolic link and configuration files
4. **Check IDE logs** for additional error information
5. **Run the check script** to diagnose configuration issues

## Notes for Adding New MCP Servers

When adding new MCP servers:

1. Update the global `.env` file with any required API keys
2. Run the `sync_mcp_config.sh` script to ensure both IDEs have the latest configuration
3. Test the server in both IDEs to confirm proper initialization

## Further Reading

- [MCP Setup Guide](./MCP_SETUP.md)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/docs)
