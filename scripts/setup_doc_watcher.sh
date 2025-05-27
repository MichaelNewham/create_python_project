#!/bin/bash

# Setup script for documentation watcher service

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Function to print colored messages
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Check for required packages
check_dependencies() {
    local missing_deps=()
    
    # Check for inotify-tools
    if ! command -v inotifywait >/dev/null 2>&1; then
        missing_deps+=("inotify-tools")
    fi
    
    # If any dependencies are missing, try to install them
    if [ ${#missing_deps[@]} -gt 0 ]; then
        print_message "$YELLOW" "Missing required packages: ${missing_deps[*]}"
        
        # Detect package manager and install
        if command -v pacman >/dev/null 2>&1; then
            print_message "$YELLOW" "Installing with pacman..."
            sudo pacman -S --noconfirm "${missing_deps[@]}"
        elif command -v apt-get >/dev/null 2>&1; then
            print_message "$YELLOW" "Installing with apt..."
            sudo apt-get update && sudo apt-get install -y "${missing_deps[@]}"
        elif command -v dnf >/dev/null 2>&1; then
            print_message "$YELLOW" "Installing with dnf..."
            sudo dnf install -y "${missing_deps[@]}"
        else
            print_message "$RED" "Could not detect package manager. Please install manually: ${missing_deps[*]}"
            exit 1
        fi
    fi
}

# Create required directories
setup_directories() {
    print_message "$YELLOW" "Setting up directories..."
    
    # Create systemd user directory
    mkdir -p ~/.config/systemd/user/
    
    # Create log directory
    mkdir -p ~/Projects/create_python_project/logs
    chmod 755 ~/Projects/create_python_project/logs
}

# Setup service
setup_service() {
    print_message "$YELLOW" "Setting up systemd service..."
    
    # Copy the service file
    cp .config/systemd/user/doc-watcher.service ~/.config/systemd/user/
    
    # Reload systemd user daemon
    systemctl --user daemon-reload
    
    # Enable and start the service
    if systemctl --user enable doc-watcher.service; then
        print_message "$GREEN" "Service enabled successfully"
    else
        print_message "$RED" "Failed to enable service"
        exit 1
    fi
    
    if systemctl --user start doc-watcher.service; then
        print_message "$GREEN" "Service started successfully"
    else
        print_message "$RED" "Failed to start service"
        exit 1
    fi
}

# Check service status
check_service() {
    print_message "$YELLOW" "Checking service status..."
    
    if systemctl --user status doc-watcher.service; then
        print_message "$GREEN" "Service is running"
    else
        print_message "$RED" "Service failed to start"
        print_message "$YELLOW" "Check logs with: journalctl --user -u doc-watcher.service"
        exit 1
    fi
}

# Main execution
main() {
    print_message "$GREEN" "Setting up documentation watcher service..."
    
    # Check and install dependencies
    check_dependencies
    
    # Setup directories
    setup_directories
    
    # Setup and start service
    setup_service
    
    # Check service status
    check_service
    
    print_message "$GREEN" "Documentation watcher service has been set up and started."
    print_message "$GREEN" "To check logs, use:"
    print_message "$GREEN" "  - Service logs: journalctl --user -u doc-watcher.service"
    print_message "$GREEN" "  - Documentation logs: tail -f ~/Projects/create_python_project/logs/doc_watcher.log"
}

# Run main function
main 