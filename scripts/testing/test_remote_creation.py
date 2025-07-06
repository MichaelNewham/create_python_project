#!/usr/bin/env python3
"""
Test remote project creation functionality.
"""

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from create_python_project.utils.core_project_builder import (
    create_remote_directory,
    create_remote_file,
    execute_remote_command,
    is_remote_path,
    parse_remote_path,
)

# Test SFTP URL
test_url = "sftp://mail2mick@manjarodell-to-pi:8850/home/mail2mick/Projects/test_remote_project"

print("Testing Remote Project Creation")
print("=" * 60)
print(f"SFTP URL: {test_url}")
print(f"Is remote: {is_remote_path(test_url)}")

# Parse the URL
user, host, port, path = parse_remote_path(test_url)
print("\nParsed details:")
print(f"  User: {user}")
print(f"  Host: {host}")
print(f"  Port: {port}")
print(f"  Path: {path}")

# Test SSH connection
print("\nTesting SSH connection...")
success, output = execute_remote_command(test_url, "echo 'Connection successful!'")
if success:
    print(f"✅ SSH connection works: {output.strip()}")
else:
    print(f"❌ SSH connection failed: {output}")
    sys.exit(1)

# Create remote directory
print("\nCreating remote directory...")
success, msg = create_remote_directory(test_url)
if success:
    print("✅ Directory created successfully")
else:
    print(f"❌ Failed to create directory: {msg}")

# Create a test file
print("\nCreating test README.md...")
readme_content = """# Test Remote Project

This project was created remotely on the Raspberry Pi via Cloudflare tunnel.

## Connection Details
- Host: manjarodell-to-pi
- Port: 8850
- Path: /home/mail2mick/Projects/test_remote_project
"""

success, msg = create_remote_file(test_url, readme_content, "README.md")
if success:
    print(f"✅ {msg}")
else:
    print(f"❌ Failed to create file: {msg}")

# List the created files
print("\nListing remote directory contents...")
success, output = execute_remote_command(test_url, f"ls -la {path}")
if success:
    print("Directory contents:")
    print(output)
else:
    print(f"❌ Failed to list directory: {output}")

print("\n" + "=" * 60)
print("Test completed!")
