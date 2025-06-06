#!/bin/bash
# Script to update the run_perplexity_mcp.sh to use the global .env file

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== Updating Perplexity MCP Runner =====${NC}"

# Define global .env path
GLOBAL_ENV_PATH="/home/michaelnewham/Projects/.env"
PERPLEXITY_SCRIPT_PATH="/home/michaelnewham/Projects/create_python_project/scripts/setup/run_perplexity_mcp.sh"

# Check if global .env exists
if [ ! -f "$GLOBAL_ENV_PATH" ]; then
    echo -e "${RED}❌ Error: Global .env file not found at $GLOBAL_ENV_PATH${NC}"
    exit 1
fi

# Check if the perplexity script exists
if [ ! -f "$PERPLEXITY_SCRIPT_PATH" ]; then
    echo -e "${RED}❌ Error: Perplexity MCP script not found at $PERPLEXITY_SCRIPT_PATH${NC}"
    exit 1
fi

# Backup the original script
cp "$PERPLEXITY_SCRIPT_PATH" "${PERPLEXITY_SCRIPT_PATH}.bak"
echo -e "${GREEN}✅ Created backup of original script at ${PERPLEXITY_SCRIPT_PATH}.bak${NC}"

# Update the script to use the global .env file
sed -i "s|if \[ -f \".env\" \]; then|if \[ -f \"$GLOBAL_ENV_PATH\" \]; then|" "$PERPLEXITY_SCRIPT_PATH"
sed -i "s|export \$(grep -v \'^#\' .env | xargs)|export \$(grep -v \'^#\' $GLOBAL_ENV_PATH | xargs)|" "$PERPLEXITY_SCRIPT_PATH"
sed -i "s|❌ Error: .env file not found.|❌ Error: Global .env file not found at $GLOBAL_ENV_PATH|" "$PERPLEXITY_SCRIPT_PATH"

echo -e "${GREEN}✅ Updated Perplexity MCP script to use the global .env file at $GLOBAL_ENV_PATH${NC}"
echo -e "${YELLOW}Note: You may need to restart VS Code for changes to take effect.${NC}"
