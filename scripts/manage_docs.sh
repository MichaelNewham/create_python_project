#!/bin/bash

# Documentation management script
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
LOG_FILE="${PROJECT_ROOT}/logs/doc_watcher.log"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Logging function
log_message() {
    local level="$1"
    local message="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message" | tee -a "$LOG_FILE"
}

# Check for required commands
check_requirements() {
    if ! command -v inotifywait >/dev/null 2>&1; then
        log_message "ERROR" "inotifywait not found. Please install inotify-tools package."
        exit 1
    fi
}

# Function to create/update aboutthisfolder.md for a directory
create_doc_content() {
    local dir="$1"
    local relative_path="${dir#$PROJECT_ROOT/}"
    local dir_name=$(basename "$dir")
    local contents
    
    contents=$(ls -la "$dir" | tail -n +4 | awk '{print $9}' | grep -v '^$' | grep -v 'aboutthisfolder.md' | sort)
    
    # Generate the documentation content
    cat << EOF
<!-- filepath: $dir/aboutthisfolder.md -->
# ${dir_name^} Folder

$(if [ -f "$dir/README.md" ]; then
    head -n 1 "$dir/README.md" | sed 's/^#* //'
else
    echo "Documentation for the $dir_name directory."
fi)

## Directory Structure

\`\`\`
$relative_path/
$(echo "$contents" | sed 's/^/├── /')
\`\`\`

## Contents Description

$(while read -r item; do
    if [ -f "$dir/$item" ]; then
        desc=$(head -n 1 "$dir/$item" 2>/dev/null | sed 's/^#* //' | sed 's/"""//' || echo "No description available")
        echo "- \`$item\`: $desc"
    elif [ -d "$dir/$item" ]; then
        count=$(ls -1 "$dir/$item" 2>/dev/null | wc -l)
        echo "- \`$item/\`: Directory containing $count items"
    fi
done <<< "$contents")

## Last Updated

This documentation was automatically generated on: $TIMESTAMP
EOF
}

# Function to update documentation for a directory
update_folder_doc() {
    local dir="$1"
    local doc_file="$dir/aboutthisfolder.md"
    
    # Check directory permissions
    if [ ! -w "$dir" ]; then
        log_message "ERROR" "No write permission for directory: $dir"
        return 1
    fi
    
    # Create the documentation
    create_doc_content "$dir" > "$doc_file"
    
    if [ $? -eq 0 ]; then
        log_message "INFO" "Updated documentation for: $dir"
        return 0
    else
        log_message "ERROR" "Failed to update documentation for: $dir"
        return 1
    fi
}

# Function to check if a directory should be documented
should_document_dir() {
    local dir="$1"
    local base_dir=$(basename "$dir")
    
    # Skip hidden directories and specific folders
    if [ "$base_dir" = "." ] || \
       [ "$base_dir" = ".." ] || \
       [ "$base_dir" = "venv" ] || \
       [ "$base_dir" = "__pycache__" ] || \
       [ "$base_dir" = "build" ] || \
       [ "$base_dir" = "dist" ] || \
       [ "$base_dir" = "node_modules" ] || \
       [ "$base_dir" = ".pytest_cache" ] || \
       [ "$base_dir" = ".mypy_cache" ] || \
       [ "$base_dir" = ".ruff_cache" ]; then
        return 1
    fi
    return 0
}

# Function to update documentation for a directory and its parents
update_directory_chain() {
    local dir="$1"
    local current_dir="$dir"
    
    while [[ "$current_dir" != "$PROJECT_ROOT" && "$current_dir" != "/" ]]; do
        if should_document_dir "$current_dir"; then
            update_folder_doc "$current_dir"
        fi
        current_dir="$(dirname "$current_dir")"
    done
    
    # Update project root as well
    if [ "$current_dir" == "$PROJECT_ROOT" ]; then
        update_folder_doc "$PROJECT_ROOT"
    fi
}

# Function to watch for changes and update docs
watch_and_update() {
    local dir="$1"
    
    inotifywait -m -e modify,create,delete,move "$dir" |
    while read -r directory events filename; do
        if [[ "$filename" != "aboutthisfolder.md" ]]; then
            log_message "INFO" "Change detected in $directory: $events on $filename"
            update_directory_chain "$directory"
        fi
    done
}

# Main execution
main() {
    # Check requirements first
    check_requirements
    
    log_message "INFO" "Starting documentation management script"
    
    # Only update documentation for specific project directories
    local project_dirs=(
        "$PROJECT_ROOT"
        "$PROJECT_ROOT/src"
        "$PROJECT_ROOT/tests"
        "$PROJECT_ROOT/scripts"
        "$PROJECT_ROOT/docs"
        "$PROJECT_ROOT/ai-docs"
    )
    
    for dir in "${project_dirs[@]}"; do
        if [ -d "$dir" ]; then
            update_folder_doc "$dir"
        fi
    done
    
    # Start watching directories for changes if --watch flag is provided
    if [[ "$1" == "--watch" ]]; then
        log_message "INFO" "Starting documentation watch mode..."
        for dir in "${project_dirs[@]}"; do
            if [ -d "$dir" ]; then
                watch_and_update "$dir" &
            fi
        done
        wait
    fi
}

# Make the script executable
chmod +x "$0"

# Run the main function with any provided arguments
main "$@" 