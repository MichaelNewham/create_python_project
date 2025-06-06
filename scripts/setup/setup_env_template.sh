#!/bin/bash
# Script to create a clean .env template file with all required variables
# This script does not include any actual API keys, only placeholders

set -e

# Color output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

ENV_FILE=".env.template"

echo -e "${YELLOW}Creating $ENV_FILE template file...${NC}"

cat > $ENV_FILE << EOL
# API Keys for AI Providers
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
PERPLEXITY_API_KEY=your_key_here
DEEPSEEK_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
BRIGHTDATA_API_KEY=your_key_here
PEXELS_API_KEY=your_key_here

# AI Model Names
OPENAI_MODEL=o4-mini-2025-04-16
ANTHROPIC_MODEL=claude-3-7-sonnet-20250219
PERPLEXITY_MODEL=sonar
DEEPSEEK_MODEL=deepseek-reasoner
GEMINI_MODEL=gemini-2.5-pro-preview-05-06

# GitHub MCP API Key
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_pat_here

# Bright Data Variables
WEB_UNLOCKER_ZONE=mcp_unlocker
BROWSER_AUTH=your_browser_auth_here

# Smithery CLI Variables
SMITHERY_CLI_KEY=your_key_here
SMITHERY_PROFILE=your_profile_here
SMITHERY_API_KEY=your_key_here
EOL

echo -e "${GREEN}Created $ENV_FILE with all required variables.${NC}"
echo -e "${YELLOW}To use this template:${NC}"
echo -e "1. Copy it to .env: cp $ENV_FILE .env"
echo -e "2. Edit .env and add your actual API keys"
echo -e "3. Keep .env secure and never commit it to version control"
