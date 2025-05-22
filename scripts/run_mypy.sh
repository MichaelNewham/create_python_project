#!/bin/bash
# This script is a wrapper for mypy that VS Code can use
# It ensures mypy runs through poetry with the correct configuration

# Get the absolute path to the project root directory (one level up from scripts)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Run mypy using poetry from the project root
cd "$PROJECT_DIR" && poetry run mypy --config-file=.config/mypy.ini "$@"
