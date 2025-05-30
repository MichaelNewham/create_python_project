#!/bin/bash

# Log management script with improved handling and documentation
LOG_DIR="logs"
BACKUP_DIR="${LOG_DIR}/archive"
DOC_DIR="docs"
MAX_LOG_AGE_DAYS=7

# Ensure directories exist with proper permissions
mkdir -p "${LOG_DIR}" "${BACKUP_DIR}"
chmod 755 "${LOG_DIR}" "${BACKUP_DIR}"

# Function to safely create log file
create_log_file() {
    local log_file="$1"
    if [[ ! -f "$log_file" ]]; then
        touch "$log_file"
        chmod 644 "$log_file"
    fi
}

# Function to archive old logs
archive_old_logs() {
    local current_date=$(date +%Y%m%d)
    
    find "${LOG_DIR}" -type f -name "*.log" -mtime +${MAX_LOG_AGE_DAYS} | while read -r log_file; do
        local base_name=$(basename "$log_file")
        local archive_name="${BACKUP_DIR}/${base_name%.log}_${current_date}.log.gz"
        gzip -c "$log_file" > "$archive_name"
        rm "$log_file"
    done
}

# Function to update log documentation
update_log_documentation() {
    local doc_file="${DOC_DIR}/logs.md"
    
    # Create logs documentation directory if it doesn't exist
    mkdir -p "${DOC_DIR}"
    
    # Create or update the logs documentation
    cat > "$doc_file" << EOF
# Log Management Documentation

This document describes the logging system used in the project.

## Log Directory Structure

```
logs/
├── archive/          # Archived log files
└── current/          # Current log files
```

## Log Types

The following log files are maintained:

- linter_black_YYYYMMDD.log - Black linting results
- linter_ruff_YYYYMMDD.log - Ruff linting results
- linter_mypy_YYYYMMDD.log - Mypy type checking results

## Retention Policy

- Current logs are kept for ${MAX_LOG_AGE_DAYS} days
- Older logs are automatically archived with gzip compression
- Archives are stored in \`logs/archive\` directory

## Last Updated
$(date "+%Y-%m-%d %H:%M:%S")
EOF
}

# Create log files with proper permissions
for linter in black ruff mypy; do
    create_log_file "${LOG_DIR}/linter_${linter}_$(date +%Y%m%d).log"
done

# Archive old logs
archive_old_logs

# Update documentation
update_log_documentation

# Create symlinks for latest logs
for linter in black ruff mypy; do
    latest_log=$(ls -t "${LOG_DIR}/linter_${linter}_"*.log 2>/dev/null | head -n1)
    if [ -n "$latest_log" ]; then
        ln -sf "$latest_log" "${LOG_DIR}/linter_${linter}_latest.log"
    fi
done 