#!/bin/bash
# Setup MCP configuration

set -e

# Define paths
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE_FILE="${PROJECT_DIR}/.vscode/mcp.json.template"
TARGET_FILE="${PROJECT_DIR}/.vscode/mcp.json"

# Check if template exists
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "❌ Template file not found at $TEMPLATE_FILE"
    exit 1
fi

# Check if .env file exists
if [ ! -f "${PROJECT_DIR}/.env" ]; then
    echo "❌ .env file not found in $PROJECT_DIR"
    echo "Please create a .env file based on .env.example"
    exit 1
fi

# Copy template to target file if it doesn't exist
if [ ! -f "$TARGET_FILE" ]; then
    cp "$TEMPLATE_FILE" "$TARGET_FILE"
    echo "✅ Created MCP configuration file from template"
else
    echo "⚠️ MCP configuration file already exists at $TARGET_FILE"
    read -p "Do you want to overwrite it? (y/n): " overwrite
    if [[ "$overwrite" == "y" || "$overwrite" == "Y" ]]; then
        cp "$TEMPLATE_FILE" "$TARGET_FILE"
        echo "✅ Updated MCP configuration file from template"
    else
        echo "⚠️ MCP configuration file not updated"
    fi
fi

echo "✅ MCP setup complete"