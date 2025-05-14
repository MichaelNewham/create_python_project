#!/bin/bash
# This script generates comprehensive documentation for the create_python_project package
# It generates:
# 1. API documentation in ai-docs/api using pdoc
# 2. aboutthisfolder.md files in each main directory
# 3. Updates to README.md and convo.md
# Recommended to run this after significant code changes

# Parse command-line arguments
VERBOSE=false
LIST_ONLY=false

# Process command line arguments
for arg in "$@"; do
  case $arg in
    --verbose|-v)
      VERBOSE=true
      shift
      ;;
    --list-only|-l)
      LIST_ONLY=true
      shift
      ;;
    --help|-h)
      echo "Usage: $0 [options]"
      echo ""
      echo "Options:"
      echo "  --verbose, -v     Show verbose output including all modified files"
      echo "  --list-only, -l   Only list files that would be updated (no actual updates)"
      echo "  --help, -h        Show this help message"
      exit 0
      ;;
  esac
done

# Get the absolute path to the project root directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Timestamp for documentation
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
DATE_ONLY=$(date '+%Y-%m-%d')

# Create necessary directories
mkdir -p "${PROJECT_DIR}/ai-docs/api"

echo "=== Create Python Project Documentation Generator ==="
echo "Started: $TIMESTAMP"
echo "=========================================="

# Function to dynamically scan and document the project structure
generate_api_documentation() {
    echo "Generating API documentation..."

    # Create a summary of the project structure to help with documentation
    SRC_DIR="${PROJECT_DIR}/src/create_python_project"
    STRUCTURE_FILE="${PROJECT_DIR}/ai-docs/api/project_structure.md"

    # Generate markdown file with project structure
    echo "# Project Structure" > "$STRUCTURE_FILE"
    echo "" >> "$STRUCTURE_FILE"
    echo "Last updated: $TIMESTAMP" >> "$STRUCTURE_FILE"
    echo "" >> "$STRUCTURE_FILE"
    echo "## Modules and Packages" >> "$STRUCTURE_FILE"
    echo "" >> "$STRUCTURE_FILE"

    # Run pdoc through poetry to generate the HTML documentation
    cd "$PROJECT_DIR" && poetry run pdoc --html --output-dir "${PROJECT_DIR}/ai-docs/api" src/create_python_project/

    # Update the API documentation README with discovered modules
    README_FILE="${PROJECT_DIR}/ai-docs/api_documentation.md"

    # Create the API documentation readme if it doesn't exist
    if [[ ! -f "$README_FILE" ]]; then
        echo "<!-- filepath: $README_FILE -->" > "$README_FILE"
        echo "# API Documentation" >> "$README_FILE"
        echo "" >> "$README_FILE"
        echo "This folder contains auto-generated API documentation for the create_python_project package." >> "$README_FILE"
        echo "" >> "$README_FILE"
        echo "## How to Update" >> "$README_FILE"
        echo "" >> "$README_FILE"
        echo "The documentation is automatically generated using the [pdoc](https://pdoc.dev/) tool which extracts documentation from Python docstrings." >> "$README_FILE"
        echo "" >> "$README_FILE"
        echo "To update this documentation:" >> "$README_FILE"
        echo "" >> "$README_FILE"
        echo "1. Run the VS Code task \"Generate Documentation\" from the Command Palette (Ctrl+Shift+P)" >> "$README_FILE"
        echo "2. Or manually execute the script: \`./scripts/update_documentation.sh\`" >> "$README_FILE"
        echo "" >> "$README_FILE"
    fi

    # First, keep the top part of the file
    if [[ -f "$README_FILE" ]]; then
        head -n 15 "$README_FILE" > "${README_FILE}.tmp"
    else
        touch "${README_FILE}.tmp"
    fi

    # Now add the dynamically discovered modules section
    echo "## Contents" >> "${README_FILE}.tmp"
    echo "" >> "${README_FILE}.tmp"
    echo "The documentation is organized following the package structure:" >> "${README_FILE}.tmp"
    echo "" >> "${README_FILE}.tmp"

    # Find all Python files in the project and list them in the README
    echo "- \`create_python_project/\` - Main package documentation" >> "${README_FILE}.tmp"

    find "$SRC_DIR" -type f -name "*.py" | sort | while read -r file; do
        relative_path=${file#$SRC_DIR/}
        if [[ "$relative_path" != "__pycache__"* && "$relative_path" != "__init__.py" ]]; then
            module_path=${relative_path%.py}
            indent=""
            depth=$(echo "$module_path" | grep -o "/" | wc -l)

            # Calculate proper indentation based on directory depth
            for (( i=0; i<depth; i++ )); do
                indent="$indent  "
            done

            # Add the module to the README
            echo "$indent- \`${module_path}.html\` - Documentation for $(basename "$module_path" | sed 's/_/ /g' | sed 's/\b\(.\)/\u\1/g')" >> "${README_FILE}.tmp"
        fi
    done

    # Add the best practices and last updated sections
    cat >> "${README_FILE}.tmp" << EOL

## Best Practices

To ensure high-quality documentation:

1. Always include docstrings for all public functions, classes, and modules
2. Use type annotations for function parameters and return values
3. Include examples in docstrings for complex functionality
4. Update documentation when making significant code changes

## Last Updated

This documentation was last updated on: $TIMESTAMP
EOL

    # Replace the original file with the updated one
    mv "${README_FILE}.tmp" "$README_FILE"

    echo "API documentation generated successfully in ai-docs/api/"

    # Append timestamp to a record file to track documentation updates
    echo "Documentation updated on $TIMESTAMP" >> "${PROJECT_DIR}/ai-docs/api/doc_updates.log"
}

# Function to generate a tree representation of a directory
generate_tree() {
    local dir=$1
    local max_depth=$2
    local cur_depth=${3:-0}
    local prefix=${4:-""}
    local last_prefix=${5:-""}

    # Get list of files and directories, excluding certain patterns
    local items=($(ls -A "$dir" 2>/dev/null | grep -v "__pycache__" | grep -v ".pyc" | grep -v ".git" | sort))
    local total=${#items[@]}
    local count=0
    local output=""

    for item in "${items[@]}"; do
        count=$((count + 1))
        local path="$dir/$item"
        local is_last=$([[ $count -eq $total ]] && echo true || echo false)
        local cur_prefix="$prefix"
        local next_prefix="$last_prefix"

        if [[ $is_last == true ]]; then
            cur_prefix="${prefix}└── "
            next_prefix="${last_prefix}    "
        else
            cur_prefix="${prefix}├── "
            next_prefix="${last_prefix}│   "
        fi

        if [[ -d "$path" ]]; then
            # It's a directory
            echo "${cur_prefix}${item}/"

            # Only recurse if we haven't reached max depth
            if [[ $cur_depth -lt $max_depth ]]; then
                generate_tree "$path" "$max_depth" $((cur_depth + 1)) "$next_prefix" "$next_prefix"
            fi
        else
            # It's a file
            echo "${cur_prefix}${item}"
        fi
    done
}

# Function to create/update aboutthisfolder.md files
create_folder_documentation() {
    echo "Updating folder documentation files..."

    # Main directories to document - based on git tracked folders
    local main_dirs=(
        "${PROJECT_DIR}/src"
        "${PROJECT_DIR}/tests"
        "${PROJECT_DIR}/scripts"
        "${PROJECT_DIR}/.config"
        "${PROJECT_DIR}/.vscode"
        "${PROJECT_DIR}/ai-docs"
        "${PROJECT_DIR}/sketches"
    )

    for dir in "${main_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            local folder_name=$(basename "$dir")
            local doc_file="$dir/aboutthisfolder.md"
            local folder_description=""
            local folder_purpose=""

            # Determine folder purpose based on folder name
            case "$folder_name" in
                "src")
                    folder_description="Source code for the Create Python Project package."
                    folder_purpose="Contains the main application code, utilities, and implementation of all features."
                    ;;
                "tests")
                    folder_description="Tests for the Create Python Project package."
                    folder_purpose="Contains test files that verify the functionality of the project components."
                    ;;
                "scripts")
                    folder_description="Utility scripts for the Create Python Project."
                    folder_purpose="Contains helper scripts for development, documentation, and automation tasks."
                    ;;
                ".config")
                    folder_description="Configuration files for the Create Python Project."
                    folder_purpose="Contains configuration files for development tools like mypy, pylint, etc."
                    ;;
                ".vscode")
                    folder_description="Visual Studio Code configuration for the project."
                    folder_purpose="Contains VS Code task definitions, settings, and launch configurations."
                    ;;
                "ai-docs")
                    folder_description="AI documentation for the Create Python Project."
                    folder_purpose="Contains AI-related documentation, API documentation, and development notes."
                    ;;
                "sketches")
                    folder_description="Design sketches and visual assets for the Create Python Project."
                    folder_purpose="Contains visual design elements, mockups, and reference images for the project."
                    ;;
            esac

            # Create tree visualization for the folder structure
            local tree_output=""
            tree_output+="$folder_name/\n"

            # List files in the directory (excluding __pycache__)
            for item in "$dir"/*; do
                if [[ -f "$item" ]]; then
                    local filename=$(basename "$item")
                    if [[ "$filename" != "__pycache__" ]]; then
                        tree_output+="├── $filename\n"
                    fi
                elif [[ -d "$item" && "$(basename "$item")" != "__pycache__" ]]; then
                    local dirname=$(basename "$item")
                    tree_output+="└── $dirname/\n"
                fi
            done

            # Create/update the aboutthisfolder.md file
            echo "<!-- filepath: $doc_file -->" > "$doc_file"
            # TODO: Fix duplicate header issue - currently this may cause doubling of the header in some cases

            echo "# ${folder_name^} Folder" >> "$doc_file"
            echo "" >> "$doc_file"
            echo "$folder_description" >> "$doc_file"
            echo "" >> "$doc_file"
            echo "## Purpose" >> "$doc_file"
            echo "" >> "$doc_file"
            echo "$folder_purpose" >> "$doc_file"
            echo "" >> "$doc_file"
            echo "## Structure" >> "$doc_file"
            echo "" >> "$doc_file"
            echo "\`\`\`" >> "$doc_file"
            echo -e "$tree_output" >> "$doc_file"
            echo "\`\`\`" >> "$doc_file"
            echo "" >> "$doc_file"
            echo "## Last Updated" >> "$doc_file"
            echo "" >> "$doc_file"
            echo "This documentation was automatically generated on: $TIMESTAMP" >> "$doc_file"

            echo "Created/updated documentation for $folder_name folder"
        fi
    done
}

# Function to update the main README.md file
update_readme() {
    echo "Updating README.md with project overview..."

    local readme_file="${PROJECT_DIR}/README.md"

    # Only update the last updated section without changing the core content
    if grep -q "## Last Updated" "$readme_file"; then
        # If the section already exists, update it
        sed -i "/## Last Updated/,/^$/c\\## Last Updated\\n\\nThis project was last updated on: $TIMESTAMP\\n\\nRun \`./scripts/update_documentation.sh\` to update documentation.\\n" "$readme_file"
    else
        # If the section doesn't exist, add it to the end
        echo "" >> "$readme_file"
        echo "## Last Updated" >> "$readme_file"
        echo "" >> "$readme_file"
        echo "This project was last updated on: $TIMESTAMP" >> "$readme_file"
        echo "" >> "$readme_file"
        echo "Run \`./scripts/update_documentation.sh\` to update documentation." >> "$readme_file"
    fi

    echo "README.md updated successfully"
}

# Function to update the convo.md file with more detailed changelog
update_convo_md() {
    echo "Updating convo.md with documentation changes..."

    local convo_file="${PROJECT_DIR}/ai-docs/convo.md"
    local temp_file="${PROJECT_DIR}/ai-docs/convo.md.tmp"

    # Check if the file exists
    if [[ -f "$convo_file" ]]; then
        # Create a backup of the original file
        cp "$convo_file" "${convo_file}.bak"

        # Check if there's an existing Updates section for today
        if grep -q "## Latest Updates ($DATE_ONLY)" "$convo_file"; then
            # Updates section exists, need to update it
            # Extract the file up to the "### Changes Made" line
            sed -n '1,/### Changes Made/p' "$convo_file" > "$temp_file"

            # Add documentation update entry
            echo "1. **Documentation System Enhancement**" >> "$temp_file"
            echo "   - Improved documentation generation script with automatic folder scanning" >> "$temp_file"
            echo "   - Added/updated aboutthisfolder.md files in all main directories" >> "$temp_file"
            echo "   - Enhanced API documentation with comprehensive module detection" >> "$temp_file"
            echo "   - Updated README.md and convo.md with latest changes" >> "$temp_file"
            echo "   - Added timestamp tracking for all documentation updates" >> "$temp_file"
            echo "" >> "$temp_file"

            # Get the rest of the file after the "### Changes Made" line
            # but skip the first update since we just added our own
            sed -n '/### Changes Made/,/^$/p' "$convo_file" | tail -n +2 >> "$temp_file"

            # Append the remainder of the file
            sed -n '/^$/,$p' "$convo_file" | tail -n +2 >> "$temp_file"

            # Replace the original file with our updated version
            mv "$temp_file" "$convo_file"
        else
            # No updates section for today, need to add one
            # Create a new temp file with updated content
            echo "<!-- filepath: $convo_file -->" > "$temp_file"
            echo "# Engineering Assessment for Create Python Project" >> "$temp_file"
            echo "" >> "$temp_file"
            echo "## Latest Updates ($DATE_ONLY)" >> "$temp_file"
            echo "" >> "$temp_file"
            echo "### Changes Made" >> "$temp_file"
            echo "1. **Documentation System Enhancement**" >> "$temp_file"
            echo "   - Improved documentation generation script with automatic folder scanning" >> "$temp_file"
            echo "   - Added/updated aboutthisfolder.md files in all main directories" >> "$temp_file"
            echo "   - Enhanced API documentation with comprehensive module detection" >> "$temp_file"
            echo "   - Updated README.md and convo.md with latest changes" >> "$temp_file"
            echo "   - Added timestamp tracking for all documentation updates" >> "$temp_file"
            echo "" >> "$temp_file"

            # Add the rest of the original file, skipping the first line which is the filepath comment
            tail -n +2 "$convo_file" >> "$temp_file"

            # Replace the original file with our updated version
            mv "$temp_file" "$convo_file"
        fi

        echo "convo.md updated successfully"
    else
        echo "Warning: convo.md file not found at $convo_file"
    fi
}

# Function to check for sensitive information in the ai-docs folder
check_sensitive_info() {
    echo "Checking for sensitive information in ai-docs..."

    local ai_docs_dir="${PROJECT_DIR}/ai-docs"

    # Define regex patterns for actual API keys, not just the names
    local sensitive_patterns=(
        # API key-like patterns (alphanumeric with dashes, 20+ chars)
        "[a-zA-Z0-9_-]{20,}"
        # OpenAI API key pattern
        "sk-[a-zA-Z0-9]{24,}"
        # Common secret patterns
        "[a-zA-Z0-9]{30,}"
    )

    local sensitive_found=false
    local results_file="${PROJECT_DIR}/ai-docs/sensitive_check_results.txt"

    # Create a temporary file for results
    > "$results_file"

    for pattern in "${sensitive_patterns[@]}"; do
        # Use grep -r to recursively search for the pattern
        if grep -r --include="*.md" --include="*.html" --include="*.txt" -E "$pattern" "$ai_docs_dir" > "$results_file" 2>&1; then
            # Check if the results contain actual API keys by filtering out false positives
            if grep -v -E "(API_KEY|SECRET|TOKEN|PASSWORD|CREDENTIAL|example|placeholder|your-key-here)" "$results_file" > /dev/null; then
                sensitive_found=true
                echo "⚠️ Warning: Potentially sensitive information matching API key pattern found in ai_docs folder."
            fi
        fi
    done

    # Clean up the results file
    rm "$results_file"

    if [[ "$sensitive_found" == true ]]; then
        echo "⚠️ Some potentially sensitive information was found in the ai-docs folder."
        echo "⚠️ Please review the content before committing to GitHub."
        echo "⚠️ You may need to add ai-docs to .gitignore to prevent sensitive data from being tracked."
    else
        echo "✅ No sensitive information detected in ai-docs folder."

        # Check if ai-docs is in .gitignore and suggest removing it
        if grep -q "ai-docs" "${PROJECT_DIR}/.gitignore"; then
            echo "🔄 The ai-docs folder is currently in .gitignore. Since no sensitive information was found,"
            echo "   you may want to remove it from .gitignore to track documentation changes with Git."
            echo "   Command to remove: sed -i '/ai-docs/d' ${PROJECT_DIR}/.gitignore"
        else
            echo "✅ The ai-docs folder is not in .gitignore. Documentation changes will be tracked by Git."
        fi
    fi
}

# Function to track and report all updated files
track_updated_files() {
    echo "Tracking all updated files..."

    # Create a temporary file to store the list of modified files
    local track_file="${PROJECT_DIR}/ai-docs/updated_files.txt"

    # Store the current timestamp
    echo "Documentation update on $TIMESTAMP" > "$track_file"
    echo "----------------------------------------" >> "$track_file"

    # List of directories to check for updated files
    local check_dirs=(
        "${PROJECT_DIR}/ai-docs"
        "${PROJECT_DIR}/src"
        "${PROJECT_DIR}/tests"
        "${PROJECT_DIR}/scripts"
        "${PROJECT_DIR}/.config"
        "${PROJECT_DIR}/.vscode"
        "${PROJECT_DIR}/sketches"
    )

    # Find all files modified in the last 5 minutes (should catch all our updates)
    echo "Files modified during this documentation update:" >> "$track_file"
    local found_files=()
    for dir in "${check_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            while IFS= read -r file; do
                found_files+=("$file")
                echo "$file" >> "$track_file"
            done < <(find "$dir" -type f -mmin -5 | grep -v "\.tmp$" | grep -v "\.bak$" | sort)
        fi
    done

    # Add README.md if it was updated
    if [[ $(find "${PROJECT_DIR}/README.md" -type f -mmin -5 2>/dev/null) ]]; then
        found_files+=("${PROJECT_DIR}/README.md")
        echo "${PROJECT_DIR}/README.md" >> "$track_file"
    fi

    # Count the number of updated files
    local file_count=${#found_files[@]}
    echo "----------------------------------------" >> "$track_file"
    echo "Total files updated: $file_count" >> "$track_file"

    # Print the update summary
    echo ""
    echo "📋 Update Summary:"
    echo "----------------------------------------"
    echo "Documentation updated on: $TIMESTAMP"
    echo "Total files updated: $file_count"

    # Print detailed file list if verbose mode is on
    if [[ "$VERBOSE" == "true" ]]; then
        echo ""
        echo "📄 Updated Files:"
        echo "----------------------------------------"
        for file in "${found_files[@]}"; do
            echo "- $file"
        done
    fi

    echo ""
    echo "Full list saved to: $track_file"
    echo ""
    if [[ "$VERBOSE" != "true" ]]; then
        echo "To see all updated files, run:"
        echo "cat ${track_file}"
        echo ""
        echo "Or run with --verbose next time:"
        echo "./scripts/update_documentation.sh --verbose"
    fi
}

# Main execution
echo "================================================================"
echo "Starting documentation update process - $(date '+%Y-%m-%d %H:%M:%S')"
echo "================================================================"

if [[ "$LIST_ONLY" == "true" ]]; then
    echo "Running in list-only mode (no changes will be made)"
    echo "The following files would be updated:"
    echo ""
    echo "1. API Documentation:"
    echo "   - ${PROJECT_DIR}/ai-docs/api_documentation.md"
    echo "   - ${PROJECT_DIR}/ai-docs/api/project_structure.md"
    echo "   - All HTML files in ${PROJECT_DIR}/ai-docs/api/"
    echo ""
    echo "2. Folder Documentation:"
    for dir in src tests scripts .config .vscode ai-docs sketches; do
        echo "   - ${PROJECT_DIR}/${dir}/aboutthisfolder.md"
    done
    echo ""
    echo "3. Other Files:"
    echo "   - ${PROJECT_DIR}/README.md"
    echo "   - ${PROJECT_DIR}/ai-docs/convo.md"
    echo "   - ${PROJECT_DIR}/ai-docs/api/doc_updates.log"
    echo "   - ${PROJECT_DIR}/ai-docs/updated_files.txt"
    echo ""
    echo "To perform the actual update, run without the --list-only option."
else
    # Run all documentation functions
    generate_api_documentation
    create_folder_documentation
    update_readme
    update_convo_md
    check_sensitive_info
    track_updated_files
fi

echo "================================================================"
echo "Documentation process completed - $(date '+%Y-%m-%d %H:%M:%S')"
echo "================================================================"
