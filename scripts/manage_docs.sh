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

Documentation for the $dir_name directory.

## Directory Structure

\`\`\`
$relative_path/
$(echo "$contents" | sed 's/^/├── /')
\`\`\`

## Contents Description

$(while read -r item; do
    if [ -f "$dir/$item" ]; then
        # Get better file description
        if [[ "$item" == *.py ]]; then
            desc=$(head -5 "$dir/$item" 2>/dev/null | grep -E '^""".*"""$|^""".*|^#.*' | head -1 | sed 's/^[#"]*\s*//' | sed 's/"""$//')
        elif [[ "$item" == *.sh ]]; then
            desc=$(head -5 "$dir/$item" 2>/dev/null | grep '^#' | grep -v '^#!/' | head -1 | sed 's/^#\s*//')
        elif [[ "$item" == *.md ]]; then
            desc=$(head -1 "$dir/$item" 2>/dev/null | sed 's/^#*\s*//')
        else
            desc=$(file "$dir/$item" 2>/dev/null | cut -d: -f2- | sed 's/^\s*//')
        fi
        [ -z "$desc" ] && desc="No description available"
        echo "- \`$item\`: $desc"
    elif [ -d "$dir/$item" ]; then
        count=$(ls -1 "$dir/$item" 2>/dev/null | wc -l)
        echo "- \`$item/\`: Directory containing $count items"
    fi
done <<< "$contents")

## Change History

$(if [ -f "$dir/.doc_history" ]; then
    tail -5 "$dir/.doc_history"
else
    echo "No change history available"
fi)

## Last Updated

This documentation was automatically generated on: $TIMESTAMP
EOF
}

# Function to update documentation for a directory
update_folder_doc() {
    local dir="$1"
    local doc_file="$dir/aboutthisfolder.md"
    local history_file="$dir/.doc_history"
    
    if [ ! -w "$dir" ]; then
        log_message "ERROR" "No write permission for directory: $dir"
        return 1
    fi
    
    # Track changes
    local current_files=$(ls -1 "$dir" 2>/dev/null | grep -v aboutthisfolder.md | sort)
    local previous_files=""
    
    if [ -f "$history_file" ]; then
        previous_files=$(grep "FILES:" "$history_file" | tail -1 | cut -d: -f2-)
    fi
    
    if [ "$current_files" != "$previous_files" ]; then
        echo "$(date): FILES:$current_files" >> "$history_file"
        
        # Log specific changes
        if [ -n "$previous_files" ]; then
            local added=$(comm -13 <(echo "$previous_files" | tr ' ' '\n' | sort) <(echo "$current_files" | tr ' ' '\n' | sort) | tr '\n' ' ')
            local removed=$(comm -23 <(echo "$previous_files" | tr ' ' '\n' | sort) <(echo "$current_files" | tr ' ' '\n' | sort) | tr '\n' ' ')
            
            [ -n "$added" ] && echo "$(date): ADDED: $added" >> "$history_file"
            [ -n "$removed" ] && echo "$(date): REMOVED: $removed" >> "$history_file"
        fi
    fi
    
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
    
    # Skip hidden directories, venv, and build folders
    if [[ "$dir" == *"/.venv"* ]] || \
       [[ "$dir" == *"/venv"* ]] || \
       [ "$base_dir" = "." ] || \
       [ "$base_dir" = ".." ] || \
       [ "$base_dir" = "__pycache__" ] || \
       [ "$base_dir" = "build" ] || \
       [ "$base_dir" = "dist" ] || \
       [ "$base_dir" = "node_modules" ] || \
       [[ "$base_dir" == .* ]]; then
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
    
    # Only document first-level directories under project root
    local project_dirs=()
    for dir in "$PROJECT_ROOT"/*; do
        if [ -d "$dir" ] && should_document_dir "$dir"; then
            project_dirs+=("$dir")
        fi
    done
    
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