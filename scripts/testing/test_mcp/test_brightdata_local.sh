#!/bin/bash
# Test BrightData MCP server locally to verify credentials

echo "Testing BrightData MCP server locally..."
echo "Loading environment from /home/michaelnewham/Projects/.env"

# Export environment variables
export API_TOKEN="949a2dab-c758-481b-8084-a27223aabf32"
export WEB_UNLOCKER_ZONE="mcp_unlocker"
export BROWSER_AUTH="brd-customer-hl_2864e594-zone-mcp_unlocker:i8xztmgmaiov"

echo "Environment variables set:"
echo "API_TOKEN: ${API_TOKEN:0:10}..."
echo "WEB_UNLOCKER_ZONE: $WEB_UNLOCKER_ZONE"
echo "BROWSER_AUTH: ${BROWSER_AUTH:0:20}..."

echo -e "\nStarting BrightData MCP server..."
echo "Press Ctrl+C to stop"
npx -y @brightdata/mcp
