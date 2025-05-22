#!/bin/bash
# Script to run the main application without showing virtual environment activation messages

# Use poetry directly to run the application
# This avoids the need to manually activate the virtual environment
clear
poetry run python -m create_python_project.create_python_project
