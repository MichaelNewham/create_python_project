#!/usr/bin/env python3
"""
MCP Server Configuration Generator

Creates dynamic MCP server configurations based on project type and tech stack.
"""

from typing import Any


def get_mcp_servers_for_project(
    project_type: str, tech_stack: dict[str, str]
) -> dict[str, Any]:
    """Return MCP server configuration based on project requirements."""

    # Base servers for all projects
    base_servers = {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "src/"],
        },
        "github": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "-e",
                "GITHUB_PERSONAL_ACCESS_TOKEN",
                "ghcr.io/github/github-mcp-server",
            ],
            "env": {
                "GITHUB_PERSONAL_ACCESS_TOKEN": "${env:GITHUB_PERSONAL_ACCESS_TOKEN}"
            },
        },
        "context7": {"command": "npx", "args": ["-y", "@upstash/context7-mcp@latest"]},
    }

    # Add project-specific servers
    if project_type == "web":
        base_servers.update(_get_web_mcp_servers(tech_stack))
    elif project_type == "data":
        base_servers.update(_get_data_mcp_servers())
    elif project_type == "api":
        base_servers.update(_get_api_mcp_servers(tech_stack))

    return {"inputs": _get_mcp_inputs(), "servers": base_servers}


def _get_web_mcp_servers(tech_stack: dict[str, str]) -> dict[str, Any]:
    """Get web development specific MCP servers."""
    servers = {}

    # Database servers
    if tech_stack.get("Database") == "PostgreSQL":
        servers["postgres"] = {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-postgres"],
            "env": {"POSTGRES_CONNECTION_STRING": "${input:postgres_connection}"},
        }

    # Frontend servers
    if tech_stack.get("Frontend") == "React":
        servers["typescript"] = {
            "command": "npx",
            "args": ["-y", "typescript-mcp-server"],
            "workspaceFolder": "${workspaceFolder}/frontend",
        }

    return servers


def _get_data_mcp_servers() -> dict[str, Any]:
    """Get data science specific MCP servers."""
    return {
        "jupyter": {
            "command": "npx",
            "args": ["-y", "jupyter-mcp-server"],
            "env": {"JUPYTER_TOKEN": "${input:jupyter_token}"},
        }
    }


def _get_api_mcp_servers(tech_stack: dict[str, str]) -> dict[str, Any]:
    """Get API development specific MCP servers."""
    servers = {}

    if tech_stack.get("Database") == "PostgreSQL":
        servers["postgres"] = {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-postgres"],
            "env": {"POSTGRES_CONNECTION_STRING": "${input:postgres_connection}"},
        }

    return servers


def _get_mcp_inputs() -> list[dict[str, Any]]:
    """Get input definitions for MCP servers."""
    return [
        {
            "type": "promptString",
            "id": "github_token",
            "description": "GitHub Personal Access Token",
            "password": True,
        },
        {
            "type": "promptString",
            "id": "postgres_connection",
            "description": "PostgreSQL connection string",
            "password": True,
        },
        {
            "type": "promptString",
            "id": "jupyter_token",
            "description": "Jupyter server token",
            "password": True,
        },
    ]
