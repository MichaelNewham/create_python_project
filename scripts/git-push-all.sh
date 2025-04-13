#!/bin/bash
# Script to set up git remote for pushing to multiple repositories

# Function to show usage
usage() {
  echo "Usage:"
  echo "  $0 add <remote_name> <remote_url>  - Add a new push URL to the origin remote"
  echo "  $0 list                           - List all configured push URLs"
  echo "  $0 remove <remote_url>            - Remove a push URL from the origin remote"
  echo "  $0 setup                          - Set up the initial configuration"
}

# Function to list all push URLs
list_urls() {
  echo "Currently configured push URLs:"
  git remote get-url --all --push origin 2>/dev/null | grep -v "^$" | grep -v "^git-push-all.sh$"
}

# Function to add a new push URL
add_url() {
  if [ -z "$1" ]; then
    echo "Error: No remote URL specified"
    usage
    exit 1
  fi
  
  echo "Adding push URL: $1"
  git remote set-url --add --push origin "$1"
  echo "Push URL added successfully"
}

# Function to remove a push URL
remove_url() {
  if [ -z "$1" ]; then
    echo "Error: No remote URL specified"
    usage
    exit 1
  fi
  
  echo "Removing push URL: $1"
  git remote set-url --delete --push origin "$1"
  echo "Push URL removed successfully"
}

# Function to set up initial configuration
setup() {
  # Get the current origin URL
  ORIGIN_URL=$(git remote get-url origin)
  
  # First, we need to ensure the remote has the original URL for pushing
  echo "Setting up multi-push configuration..."
  git remote set-url --push origin "$ORIGIN_URL"
  
  echo "Initial setup complete."
  echo ""
  echo "Your current push URL is set to: $ORIGIN_URL"
  echo ""
  echo "To add additional repositories, use:"
  echo "$0 add <repository_url>"
}

# Main script logic
case "$1" in
  "add")
    add_url "$2"
    ;;
  "list")
    list_urls
    ;;
  "remove")
    remove_url "$2"
    ;;
  "setup")
    setup
    ;;
  *)
    usage
    ;;
esac
