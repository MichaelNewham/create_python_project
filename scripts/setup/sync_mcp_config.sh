#!/bin/bash
# Script to sync MCP configuration between VS Code and Cursor IDE
# Handles external .env file location and creates symbolic links

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== MCP Configuration Sync Tool =====${NC}"

# Define global .env path
GLOBAL_ENV_PATH="/home/michaelnewham/Projects/.env"

# Check if global .env exists
if [ ! -f "$GLOBAL_ENV_PATH" ]; then
    echo -e "${RED}❌ Error: Global .env file not found at $GLOBAL_ENV_PATH${NC}"
    exit 1
fi

# Create .vscode directory if it doesn't exist
if [ ! -d ".vscode" ]; then
    echo -e "${BLUE}Creating .vscode directory...${NC}"
    mkdir -p .vscode
fi

# Create .cursor directory if it doesn't exist
if [ ! -d ".cursor" ]; then
    echo -e "${BLUE}Creating .cursor directory...${NC}"
    mkdir -p .cursor
fi

# 1. Create symbolic link for .env in the project root
if [ -L ".env" ] && [ "$(readlink .env)" == "$GLOBAL_ENV_PATH" ]; then
    echo -e "${GREEN}✅ Symbolic link to global .env already exists.${NC}"
else
    echo -e "${BLUE}Creating symbolic link to global .env file...${NC}"
    ln -sf "$GLOBAL_ENV_PATH" ./.env
    echo -e "${GREEN}✅ Created symbolic link to global .env file.${NC}"
fi

# 2. Sync VS Code MCP config to Cursor
if [ -f ".vscode/mcp.json" ]; then
    echo -e "${BLUE}Syncing VS Code MCP configuration to Cursor...${NC}"
    cp -f .vscode/mcp.json .cursor/mcp.json
    echo -e "${GREEN}✅ Copied .vscode/mcp.json to .cursor/mcp.json${NC}"
elif [ -f ".cursor/mcp.json" ]; then
    echo -e "${BLUE}Syncing Cursor MCP configuration to VS Code...${NC}"
    cp -f .cursor/mcp.json .vscode/mcp.json
    echo -e "${GREEN}✅ Copied .cursor/mcp.json to .vscode/mcp.json${NC}"
else
    echo -e "${YELLOW}⚠️ No MCP configuration found in either .vscode or .cursor directories.${NC}"
fi

# 3. Sync VS Code MCP secrets to Cursor
if [ -f ".vscode/mcp-secrets.json" ]; then
    echo -e "${BLUE}Syncing VS Code MCP secrets to Cursor...${NC}"
    cp -f .vscode/mcp-secrets.json .cursor/mcp-secrets.json
    echo -e "${GREEN}✅ Copied .vscode/mcp-secrets.json to .cursor/mcp-secrets.json${NC}"
elif [ -f ".cursor/mcp-secrets.json" ]; then
    echo -e "${BLUE}Syncing Cursor MCP secrets to VS Code...${NC}"
    cp -f .cursor/mcp-secrets.json .vscode/mcp-secrets.json
    echo -e "${GREEN}✅ Copied .cursor/mcp-secrets.json to .vscode/mcp-secrets.json${NC}"
fi

echo -e "${GREEN}✅ MCP configuration sync complete.${NC}"
echo -e "${YELLOW}Note: You may need to restart VS Code and Cursor for changes to take effect.${NC}"
