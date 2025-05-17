#!/bin/bash
# This script checks the connection to GitLab and provides troubleshooting information

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== GitLab Connection Diagnostic Tool =====${NC}"

# Check if the GitLab remote exists
if ! git remote | grep -q "gitlab"; then
    echo -e "${RED}❌ Error: GitLab remote does not exist.${NC}"
    echo -e "${YELLOW}Add GitLab remote with: git remote add gitlab https://gitlab.michaelnewham.me/python_projects/create_python_project.git${NC}"
    exit 1
fi

# Get GitLab URL
GITLAB_URL=$(git remote get-url gitlab)
echo -e "${BLUE}GitLab URL: ${GITLAB_URL}${NC}"

# Extract the domain from the URL
DOMAIN=$(echo "$GITLAB_URL" | sed -E 's|https?://([^/]+).*|\1|')
echo -e "${BLUE}Domain: ${DOMAIN}${NC}"

# Check if the domain is reachable
echo -e "${BLUE}Testing domain reachability...${NC}"
if ping -c 1 "$DOMAIN" &> /dev/null; then
    echo -e "${GREEN}✅ Domain is reachable.${NC}"
else
    echo -e "${YELLOW}⚠️ Warning: Cannot ping domain. This may be normal if ICMP is blocked.${NC}"
fi

# Check HTTPS connection
echo -e "${BLUE}Testing HTTPS connection...${NC}"
if curl -sS -I "https://$DOMAIN" &> /dev/null; then
    echo -e "${GREEN}✅ HTTPS connection successful.${NC}"
    echo -e "${BLUE}HTTP Status:${NC}"
    curl -sS -I "https://$DOMAIN" | head -n 1
else
    echo -e "${RED}❌ Error: Cannot establish HTTPS connection.${NC}"
    echo -e "${YELLOW}Possible reasons:${NC}"
    echo -e "  - Network connectivity issue"
    echo -e "  - SSL/TLS certificate problem"
    echo -e "  - Server is down or unreachable"
    echo -e "  - Firewall blocking HTTPS traffic"
fi

# Check Git authentication
echo -e "${BLUE}Testing Git credentials...${NC}"
echo -e "${YELLOW}Note: This will not push any changes, just check authentication.${NC}"
if git ls-remote --heads "$GITLAB_URL" &> /dev/null; then
    echo -e "${GREEN}✅ Git authentication successful.${NC}"
else
    echo -e "${RED}❌ Error: Git authentication failed.${NC}"
    echo -e "${YELLOW}Possible reasons:${NC}"
    echo -e "  - Invalid credentials"
    echo -e "  - Access token expired"
    echo -e "  - No access to repository"
    echo -e "  - Repository doesn't exist"
    echo -e "  - Server-side issue"
fi

# Try fetching with verbose output
echo -e "${BLUE}Attempting git fetch with verbose output...${NC}"
git fetch gitlab --verbose || echo -e "${RED}Fetch failed${NC}"

echo -e "${BLUE}===== Diagnostic Summary =====${NC}"
echo -e "${YELLOW}If you're experiencing issues with GitLab:${NC}"
echo -e "1. Check your network connection and VPN status if applicable"
echo -e "2. Verify that your GitLab instance is running correctly"
echo -e "3. Check that your credentials are valid (use git credential-manager list)"
echo -e "4. Consider using an access token instead of password"
echo -e "5. Try using SSH instead of HTTPS for connection"

echo -e "${BLUE}To force push without GitLab, use:${NC}"
echo -e "${GREEN}git push github \$(git branch --show-current)${NC}"
