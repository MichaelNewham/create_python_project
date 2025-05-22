#!/bin/bash
# This script checks the connection to Context7 and Perplexity services

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== AI Services Diagnostic Tool =====${NC}"

# Load environment variables
if [ -f ".env" ]; then
    echo -e "${BLUE}Loading environment variables from .env file...${NC}"
    export $(grep -v '^#' .env | xargs)
else
    echo -e "${YELLOW}⚠️ Warning: .env file not found. Using existing environment variables.${NC}"
fi

# Check Context7
echo -e "${BLUE}Testing Context7 service...${NC}"
if [ -z "$CONTEXT7_API_KEY" ]; then
    echo -e "${YELLOW}⚠️ Warning: CONTEXT7_API_KEY not found in environment variables.${NC}"
else
    echo -e "${GREEN}✅ CONTEXT7_API_KEY is set.${NC}"
    
    # Test a simple library ID resolution
    echo -e "${BLUE}Testing Context7 library resolution...${NC}"
    if command -v curl &> /dev/null; then
        response=$(curl -s -X POST "https://api.context7.ai/resolve-library-id" \
            -H "Authorization: Bearer $CONTEXT7_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{"query": "react"}' \
            --max-time 10)
        
        if [[ $response == *"id"* ]]; then
            echo -e "${GREEN}✅ Context7 service is responding correctly.${NC}"
        else
            echo -e "${RED}❌ Context7 service returned an unexpected response.${NC}"
            echo -e "${YELLOW}Response: ${response}${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️ curl command not found. Cannot test Context7 API.${NC}"
    fi
fi

# Check Perplexity
echo -e "${BLUE}Testing Perplexity service...${NC}"
if [ -z "$PERPLEXITY_API_KEY" ]; then
    echo -e "${YELLOW}⚠️ Warning: PERPLEXITY_API_KEY not found in environment variables.${NC}"
else
    echo -e "${GREEN}✅ PERPLEXITY_API_KEY is set.${NC}"
    
    # Test a simple query
    echo -e "${BLUE}Testing Perplexity API...${NC}"
    if command -v curl &> /dev/null; then
        response=$(curl -s -X POST "https://api.perplexity.ai/chat/completions" \
            -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{
                "model": "sonar",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello, are you working?"}
                ]
            }' \
            --max-time 10)
        
        if [[ $response == *"choices"* ]]; then
            echo -e "${GREEN}✅ Perplexity service is responding correctly.${NC}"
        else
            echo -e "${RED}❌ Perplexity service returned an unexpected response.${NC}"
            echo -e "${YELLOW}Response: ${response}${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️ curl command not found. Cannot test Perplexity API.${NC}"
    fi
fi

echo -e "${BLUE}===== Diagnostic Summary =====${NC}"
echo -e "${YELLOW}If you're experiencing issues with AI services:${NC}"
echo -e "1. Check your network connection and VPN status if applicable"
echo -e "2. Verify that your API keys are valid and not expired"
echo -e "3. Check service status pages for any outages"
echo -e "4. Try using alternative AI providers available in your project"

# List available AI providers
echo -e "${BLUE}Available AI providers in your environment:${NC}"
if command -v python &> /dev/null && command -v poetry &> /dev/null; then
    poetry run python -c "from create_python_project.utils.ai_integration import get_available_ai_providers; print('\n'.join([f'- {k}: {v}' for k, v in get_available_ai_providers().items()]))" 2>/dev/null || echo -e "${YELLOW}Could not retrieve AI providers from Python code.${NC}"
else
    echo -e "${YELLOW}Python or Poetry not available to check AI providers.${NC}"
fi