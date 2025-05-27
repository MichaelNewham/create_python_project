#!/bin/bash

# Script to manage log files according to Cursor rules
# - Enforces 250 line limit
# - Rotates logs
# - Maintains consistent structure

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOGS_DIR="${PROJECT_DIR}/logs"
MAX_LINES=250
DATE=$(date '+%Y%m%d')

# Create logs directory if it doesn't exist
mkdir -p "$LOGS_DIR"

# Function to truncate a log file to MAX_LINES
truncate_log() {
    local file=$1
    local lines=$(wc -l < "$file")
    
    if [ "$lines" -gt "$MAX_LINES" ]; then
        echo "Truncating $file (current lines: $lines)"
        # Add truncation notice if not already present
        if ! grep -q "=== LOG TRUNCATED ===" "$file"; then
            local temp_file="${file}.tmp"
            echo "=== LOG TRUNCATED === Keeping last $MAX_LINES lines (truncated on $(date '+%Y-%m-%d %H:%M:%S')) ===" > "$temp_file"
            tail -n "$MAX_LINES" "$file" >> "$temp_file"
            mv "$temp_file" "$file"
        else
            # If notice exists, just keep last MAX_LINES
            local temp_file="${file}.tmp"
            head -n 1 "$file" > "$temp_file"  # Keep the truncation notice
            tail -n "$MAX_LINES" "$file" >> "$temp_file"
            mv "$temp_file" "$file"
        fi
    fi
}

# Function to ensure log file has proper format
ensure_log_format() {
    local file=$1
    local component=$2
    
    # Add header if file is empty
    if [ ! -s "$file" ]; then
        echo "=== $component Log ===" > "$file"
        echo "Started: $(date '+%Y-%m-%d %H:%M:%S')" >> "$file"
        echo "====================\n" >> "$file"
    fi
}

# Move and rename temporary logs to proper location
move_temp_logs() {
    # Move linter logs
    for temp_log in /tmp/linter_*_*.log; do
        if [ -f "$temp_log" ]; then
            local base_name=$(basename "$temp_log")
            local linter_name=$(echo "$base_name" | cut -d'_' -f2)
            local new_name="linter_${linter_name}_${DATE}.log"
            mv "$temp_log" "${LOGS_DIR}/${new_name}"
            ensure_log_format "${LOGS_DIR}/${new_name}" "${linter_name}"
            truncate_log "${LOGS_DIR}/${new_name}"
        fi
    done

    # Move commit logs
    for temp_log in /tmp/commit_*.txt; do
        if [ -f "$temp_log" ]; then
            local new_name="commit_debug_${DATE}.log"
            mv "$temp_log" "${LOGS_DIR}/${new_name}"
            ensure_log_format "${LOGS_DIR}/${new_name}" "Commit"
            truncate_log "${LOGS_DIR}/${new_name}"
        fi
    done

    # Move MyPy report
    if [ -f "/tmp/mypy_report.txt" ]; then
        mv "/tmp/mypy_report.txt" "${LOGS_DIR}/linter_mypy_${DATE}.log"
        ensure_log_format "${LOGS_DIR}/linter_mypy_${DATE}.log" "MyPy"
        truncate_log "${LOGS_DIR}/linter_mypy_${DATE}.log"
    fi

    # Move Pylint report
    if [ -f "/tmp/pylint_report.txt" ]; then
        mv "/tmp/pylint_report.txt" "${LOGS_DIR}/linter_pylint_${DATE}.log"
        ensure_log_format "${LOGS_DIR}/linter_pylint_${DATE}.log" "Pylint"
        truncate_log "${LOGS_DIR}/linter_pylint_${DATE}.log"
    fi

    # Move security check results
    if [ -f "${PROJECT_DIR}/ai-docs/sensitive_check_results.txt" ]; then
        mv "${PROJECT_DIR}/ai-docs/sensitive_check_results.txt" "${LOGS_DIR}/security_scan_${DATE}.log"
        ensure_log_format "${LOGS_DIR}/security_scan_${DATE}.log" "Security"
        truncate_log "${LOGS_DIR}/security_scan_${DATE}.log"
    fi

    # Move documentation update log
    if [ -f "${PROJECT_DIR}/ai-docs/updated_files.txt" ]; then
        mv "${PROJECT_DIR}/ai-docs/updated_files.txt" "${LOGS_DIR}/documentation_updates_${DATE}.log"
        ensure_log_format "${LOGS_DIR}/documentation_updates_${DATE}.log" "Documentation"
        truncate_log "${LOGS_DIR}/documentation_updates_${DATE}.log"
    fi
}

# Clean up old logs (keep last 7 days)
cleanup_old_logs() {
    find "$LOGS_DIR" -name "*.log" -type f -mtime +7 -delete
}

# Main execution
move_temp_logs
cleanup_old_logs

# Make the script executable
chmod +x "$0" 