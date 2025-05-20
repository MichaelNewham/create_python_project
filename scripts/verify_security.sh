#!/bin/bash
# Quick security verification script
# This checks that our security measures are properly in place

set -e

# Color output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Performing Security Verification Checks...${NC}"
echo

# Check 1: .env and mcp.json are in .gitignore
echo -n "Checking .gitignore file: "
if grep -q "\.env" .gitignore && grep -q "\.vscode/mcp\.json" .gitignore; then
    echo -e "${GREEN}PASSED${NC} - .env and mcp.json are properly ignored"
else
    echo -e "${RED}FAILED${NC} - .env or mcp.json missing from .gitignore"
fi

# Check 2: Template files exist
echo -n "Checking template files: "
if [ -f ".vscode/mcp.json.template" ] && [ -f ".env.template" ]; then
    echo -e "${GREEN}PASSED${NC} - Template files exist"
else
    echo -e "${RED}FAILED${NC} - Template files missing"
fi

# Check 3: No hardcoded API keys in mcp.json
echo -n "Checking for hardcoded API keys: "
if [ -f ".vscode/mcp.json" ]; then
    if grep -q "d50516c4-5ac8-478a-97e2-8e1448dfd374" .vscode/mcp.json; then
        echo -e "${RED}FAILED${NC} - Found hardcoded Smithery key in mcp.json"
    else
        API_KEY_COUNT=$(grep -c "api_key\|API_KEY\|api-key" .vscode/mcp.json || true)
        if [ "$API_KEY_COUNT" -gt 0 ]; then
            echo -e "${YELLOW}WARNING${NC} - Found $API_KEY_COUNT references to API keys, please verify they're using environment variables"
        else
            echo -e "${GREEN}PASSED${NC} - No hardcoded API keys found"
        fi
    fi
else
    echo -e "${YELLOW}SKIPPED${NC} - mcp.json doesn't exist in this environment"
fi

# Check 4: Security scripts exist
echo -n "Checking security scripts: "
if [ -f "scripts/remove_sensitive_file.sh" ] && [ -f "scripts/setup_env_template.sh" ]; then
    echo -e "${GREEN}PASSED${NC} - Security scripts exist"
else
    echo -e "${RED}FAILED${NC} - Security scripts missing"
fi

# Check 5: Documentation exists
echo -n "Checking security documentation: "
if [ -f "docs/MCP_SETUP.md" ]; then
    echo -e "${GREEN}PASSED${NC} - Security documentation exists"
else
    echo -e "${RED}FAILED${NC} - Security documentation missing"
fi

echo
echo -e "${YELLOW}Security verification complete.${NC}"
