#!/bin/bash
# This script runs the Perplexity MCP server with environment variables from .env

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== Perplexity MCP Server Launcher =====${NC}"

# Load environment variables
if [ -f ".env" ]; then
    echo -e "${BLUE}Loading environment variables from .env file...${NC}"
    export $(grep -v '^#' .env | xargs)
    
    # Verify Perplexity API key is loaded
    if [ -z "$PERPLEXITY_API_KEY" ]; then
        echo -e "${RED}❌ Error: PERPLEXITY_API_KEY not found in environment variables.${NC}"
        exit 1
    else
        echo -e "${GREEN}✅ PERPLEXITY_API_KEY is set.${NC}"
        echo -e "${GREEN}✅ Using model: ${PERPLEXITY_MODEL:-sonar}${NC}"
    fi
else
    echo -e "${RED}❌ Error: .env file not found.${NC}"
    exit 1
fi

# Run the Perplexity MCP server
echo -e "${BLUE}Starting Perplexity MCP server...${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
npx -y server-perplexity-ask
