#!/bin/bash
# This script checks if the Perplexity API key exists in the global .env file
# and ensures that MCP server configurations are properly set up.

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== Perplexity MCP Configuration Check =====${NC}"

# Define global .env path
GLOBAL_ENV_PATH="/home/michaelnewham/Projects/.env"

# Check if global .env exists
if [ ! -f "$GLOBAL_ENV_PATH" ]; then
    echo -e "${RED}❌ Error: Global .env file not found at $GLOBAL_ENV_PATH${NC}"
    exit 1
fi

# Load environment variables from global .env
echo -e "${BLUE}Loading environment variables from global .env file...${NC}"
export "$(grep -v '^#' "$GLOBAL_ENV_PATH" | xargs)"

# Check if PERPLEXITY_API_KEY exists in the environment
if [ -z "$PERPLEXITY_API_KEY" ]; then
    echo -e "${RED}❌ Error: PERPLEXITY_API_KEY not found in global .env file.${NC}"
    echo -e "${YELLOW}Please add your Perplexity API key to $GLOBAL_ENV_PATH:${NC}"
    echo -e "PERPLEXITY_API_KEY=your_key_here"
    exit 1
else
    echo -e "${GREEN}✅ PERPLEXITY_API_KEY is set in global .env file.${NC}"
fi

# Check for MCP configuration directories
echo -e "${BLUE}Checking MCP configuration directories...${NC}"

# VS Code MCP config
VSCODE_MCP_DIR=".vscode"
if [ -d "$VSCODE_MCP_DIR" ]; then
    echo -e "${GREEN}✅ VS Code configuration directory exists.${NC}"
    
    # Check for mcp.json
    if [ -f "$VSCODE_MCP_DIR/mcp.json" ]; then
        echo -e "${GREEN}✅ VS Code MCP configuration file exists.${NC}"
        
        # Check if Perplexity is configured in mcp.json
        if grep -q "perplexity" "$VSCODE_MCP_DIR/mcp.json"; then
            echo -e "${GREEN}✅ Perplexity configuration found in VS Code MCP config.${NC}"
        else
            echo -e "${YELLOW}⚠️ Warning: Perplexity configuration not found in VS Code MCP config.${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️ Warning: VS Code MCP configuration file not found.${NC}"
    fi
else
    echo -e "${YELLOW}⚠️ Warning: VS Code configuration directory not found.${NC}"
fi

# Cursor MCP config
CURSOR_MCP_DIR=".cursor"
if [ -d "$CURSOR_MCP_DIR" ]; then
    echo -e "${GREEN}✅ Cursor configuration directory exists.${NC}"
    
    # Check for mcp.json
    if [ -f "$CURSOR_MCP_DIR/mcp.json" ]; then
        echo -e "${GREEN}✅ Cursor MCP configuration file exists.${NC}"
        
        # Check if Perplexity is configured in mcp.json
        if grep -q "perplexity" "$CURSOR_MCP_DIR/mcp.json"; then
            echo -e "${GREEN}✅ Perplexity configuration found in Cursor MCP config.${NC}"
        else
            echo -e "${YELLOW}⚠️ Warning: Perplexity configuration not found in Cursor MCP config.${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️ Warning: Cursor MCP configuration file not found.${NC}"
    fi
else
    echo -e "${YELLOW}⚠️ Warning: Cursor configuration directory not found.${NC}"
fi

echo -e "${BLUE}===== Configuration Check Complete =====${NC}"
echo -e "${YELLOW}Note: If any warnings were shown, run the sync_mcp_config.sh script to fix configuration issues.${NC}"
echo -e "${YELLOW}To test the Perplexity MCP server, run: ./scripts/run_perplexity_mcp.sh${NC}"
