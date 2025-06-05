#!/bin/bash
# This script checks the connection to all AI services used in Create Python Project

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

# Check Anthropic
echo -e "${BLUE}Testing Anthropic (Claude) service...${NC}"
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${YELLOW}⚠️ Warning: ANTHROPIC_API_KEY not found in environment variables.${NC}"
else
    echo -e "${GREEN}✅ ANTHROPIC_API_KEY is set.${NC}"
    
    # Get model from environment or use default
    ANTHROPIC_MODEL_NAME=${ANTHROPIC_MODEL:-"claude-sonnet-4-20250514"}
    echo -e "${BLUE}Using model: ${ANTHROPIC_MODEL_NAME}${NC}"
    
    # Test a simple query
    echo -e "${BLUE}Testing Anthropic API...${NC}"
    if command -v curl &> /dev/null; then
        response=$(curl -s -X POST "https://api.anthropic.com/v1/messages" \
            -H "x-api-key: $ANTHROPIC_API_KEY" \
            -H "Content-Type: application/json" \
            -H "anthropic-version: 2023-06-01" \
            -d "{
                \"model\": \"$ANTHROPIC_MODEL_NAME\",
                \"max_tokens\": 100,
                \"messages\": [
                    {\"role\": \"user\", \"content\": \"Hello, please respond with just 'API test successful' to confirm you are working.\"}
                ]
            }" \
            --max-time 15)
        
        if [[ $response == *"content"* ]] && [[ $response == *"text"* ]]; then
            echo -e "${GREEN}✅ Anthropic service is responding correctly.${NC}"
            # Extract and display the response content
            if command -v python3 &> /dev/null; then
                content=$(echo "$response" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['content'][0]['text'].strip())" 2>/dev/null || echo "Could not parse response")
                echo -e "${GREEN}Response: ${content}${NC}"
            fi
        else
            echo -e "${RED}❌ Anthropic service returned an unexpected response.${NC}"
            echo -e "${YELLOW}Response: ${response}${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️ curl command not found. Cannot test Anthropic API.${NC}"
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

# Check OpenAI
echo -e "${BLUE}Testing OpenAI service...${NC}"
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}⚠️ Warning: OPENAI_API_KEY not found in environment variables.${NC}"
else
    echo -e "${GREEN}✅ OPENAI_API_KEY is set.${NC}"
    
    # Get model from environment or use default
    OPENAI_MODEL_NAME=${OPENAI_MODEL:-"gpt-4o-mini"}
    echo -e "${BLUE}Using model: ${OPENAI_MODEL_NAME}${NC}"
    
    # Test a simple query
    echo -e "${BLUE}Testing OpenAI API...${NC}"
    if command -v curl &> /dev/null; then
        response=$(curl -s -X POST "https://api.openai.com/v1/chat/completions" \
            -H "Authorization: Bearer $OPENAI_API_KEY" \
            -H "Content-Type: application/json" \
            -d "{
                \"model\": \"$OPENAI_MODEL_NAME\",
                \"messages\": [
                    {\"role\": \"user\", \"content\": \"Hello, please respond with just 'API test successful' to confirm you are working.\"}
                ],
                \"max_completion_tokens\": 100
            }" \
            --max-time 15)
        
        if [[ $response == *"choices"* ]] && [[ $response == *"content"* ]]; then
            echo -e "${GREEN}✅ OpenAI service is responding correctly.${NC}"
            # Extract and display the response content
            if command -v python3 &> /dev/null; then
                content=$(echo "$response" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['choices'][0]['message']['content'].strip())" 2>/dev/null || echo "Could not parse response")
                echo -e "${GREEN}Response: ${content}${NC}"
            fi
        else
            echo -e "${RED}❌ OpenAI service returned an unexpected response.${NC}"
            echo -e "${YELLOW}Response: ${response}${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️ curl command not found. Cannot test OpenAI API.${NC}"
    fi
fi

# Check DeepSeek
echo -e "${BLUE}Testing DeepSeek service...${NC}"
if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo -e "${YELLOW}⚠️ Warning: DEEPSEEK_API_KEY not found in environment variables.${NC}"
else
    echo -e "${GREEN}✅ DEEPSEEK_API_KEY is set.${NC}"
    
    # Get model from environment or use default
    DEEPSEEK_MODEL_NAME=${DEEPSEEK_MODEL:-"deepseek-reasoner"}
    echo -e "${BLUE}Using model: ${DEEPSEEK_MODEL_NAME}${NC}"
    
    # Test a simple query
    echo -e "${BLUE}Testing DeepSeek API...${NC}"
    if command -v curl &> /dev/null; then
        response=$(curl -s -X POST "https://api.deepseek.com/v1/chat/completions" \
            -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
            -H "Content-Type: application/json" \
            -d "{
                \"model\": \"$DEEPSEEK_MODEL_NAME\",
                \"messages\": [
                    {\"role\": \"user\", \"content\": \"Hello, please respond with just 'API test successful' to confirm you are working.\"}
                ],
                \"max_tokens\": 100
            }" \
            --max-time 15)
        
        if [[ $response == *"choices"* ]] && [[ $response == *"content"* ]]; then
            echo -e "${GREEN}✅ DeepSeek service is responding correctly.${NC}"
            # Extract and display the response content
            if command -v python3 &> /dev/null; then
                content=$(echo "$response" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['choices'][0]['message']['content'].strip())" 2>/dev/null || echo "Could not parse response")
                echo -e "${GREEN}Response: ${content}${NC}"
            fi
        else
            echo -e "${RED}❌ DeepSeek service returned an unexpected response.${NC}"
            echo -e "${YELLOW}Response: ${response}${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️ curl command not found. Cannot test DeepSeek API.${NC}"
    fi
fi

# Check Gemini
echo -e "${BLUE}Testing Gemini service...${NC}"
if [ -z "$GOOGLE_API_KEY" ]; then
    echo -e "${YELLOW}⚠️ Warning: GOOGLE_API_KEY not found in environment variables.${NC}"
else
    echo -e "${GREEN}✅ GOOGLE_API_KEY is set.${NC}"
    
    # Get model from environment or use default
    GEMINI_MODEL_NAME=${GEMINI_MODEL:-"gemini-2.5-flash-preview-05-20"}
    echo -e "${BLUE}Using model: ${GEMINI_MODEL_NAME}${NC}"
    
    # Test a simple query
    echo -e "${BLUE}Testing Gemini API...${NC}"
    if command -v curl &> /dev/null; then
        response=$(curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL_NAME}:generateContent?key=${GOOGLE_API_KEY}" \
            -H "Content-Type: application/json" \
            -d '{
                "contents": [{
                    "parts": [{
                        "text": "Hello, please respond with just API test successful to confirm you are working."
                    }]
                }],
                "generationConfig": {
                    "maxOutputTokens": 100
                }
            }' \
            --max-time 15)
        
        if [[ $response == *"candidates"* ]] && [[ $response == *"content"* ]]; then
            echo -e "${GREEN}✅ Gemini service is responding correctly.${NC}"
            # Extract and display the response content
            if command -v python3 &> /dev/null; then
                content=$(echo "$response" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['candidates'][0]['content']['parts'][0]['text'].strip())" 2>/dev/null || echo "Could not parse response")
                echo -e "${GREEN}Response: ${content}${NC}"
            fi
        else
            echo -e "${RED}❌ Gemini service returned an unexpected response.${NC}"
            echo -e "${YELLOW}Response: ${response}${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️ curl command not found. Cannot test Gemini API.${NC}"
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