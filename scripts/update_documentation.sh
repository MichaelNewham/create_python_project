#!/bin/bash
# This script generates comprehensive documentation for the create_python_project package
# It generates:
# 1. API documentation in ai-docs/api using pdoc
# 2. aboutthisfolder.md files in each main directory (including hidden folders that are tracked by git)
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

# Function to check if a path is ignored by git
is_git_ignored() {
    local path="$1"
    local dirname=$(basename "$path")
    
    # Check if git is available
    if command -v git >/dev/null 2>&1; then
        # Use git to check if the path is ignored
        if git -C "${PROJECT_DIR}" check-ignore -q "$(realpath --relative-to="${PROJECT_DIR}" "$path")"; then
            return 0  # Path is ignored
        fi
    fi
    
    # Fallback to manual check in .gitignore
    if grep -q "^$dirname\$\|^$dirname/\|/$dirname/\|/$dirname\$" "${PROJECT_DIR}/.gitignore"; then
        return 0  # Path is in .gitignore
    fi
    
    return 1  # Path is not ignored
}

echo "📚 Updating project documentation..."

# Function to dynamically scan and document the project structure
generate_api_documentation() {
    echo "  • API documentation..."

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

    echo "   ✅"

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

# Function to generate a tree representation of a directory with specified depth
generate_directory_tree() {
    local dir=$1
    local max_depth=$2

    # Default max_depth if not provided
    max_depth=${max_depth:-2}

    # Get the basename of the directory for the root node
    local dir_name=$(basename "$dir")

    # Check if tree command is available
    if command -v tree >/dev/null 2>&1; then
        # Use tree command with proper formatting
        tree_output=$(cd "$dir" && tree -L "$max_depth" -I "__pycache__|*.pyc" --noreport | sed "1s/.*/$(basename "$dir")\//")
        echo "$tree_output"
    else
        # Fallback to a simple listing if tree is not available
        local tree_output="$dir_name/\n"

        # List files and directories in the current directory
        for item in "$dir"/*; do
            if [[ -f "$item" ]]; then
                local filename=$(basename "$item")
                if [[ "$filename" != "__pycache__" && "$filename" != "*.pyc" ]]; then
                    tree_output+="├── $filename\n"
                fi
            elif [[ -d "$item" ]]; then
                local dirname=$(basename "$item")
                if [[ "$dirname" != "__pycache__" ]]; then
                    tree_output+="└── $dirname/\n"
                fi
            fi
        done

        echo -e "$tree_output"
    fi
}

# Function to get semantic file description
get_semantic_description() {
    local file="$1"
    local filename=$(basename "$file")
    local dir_name="$2"
    
    # Check if file exists
    if [[ ! -f "$file" ]]; then
        echo "File not found"
        return
    fi
    
    case "$filename" in
        *.py)
            # Extract docstring or first comment
            local desc=$(head -20 "$file" 2>/dev/null | grep -E '^""".*"""$|^""".*|^#[^!].*' | head -1 | sed 's/^[#"]*\s*//' | sed 's/"""$//')
            if [[ -z "$desc" ]]; then
                # Try to extract class or function name
                local class_func=$(head -10 "$file" 2>/dev/null | grep -E '^(class|def) ' | head -1 | cut -d' ' -f2 | cut -d'(' -f1)
                if [[ -n "$class_func" ]]; then
                    desc="Python module containing $class_func"
                else
                    desc="Python source file"
                fi
            fi
            echo "$desc"
            ;;
        *.sh)
            # Extract comment after shebang
            local desc=$(head -10 "$file" 2>/dev/null | grep '^#' | grep -v '^#!/' | head -1 | sed 's/^#\s*//')
            [[ -z "$desc" ]] && desc="Shell script for automation"
            echo "$desc"
            ;;
        *.md)
            # Extract first heading or line
            local desc=$(head -5 "$file" 2>/dev/null | grep '^#' | head -1 | sed 's/^#*\s*//')
            [[ -z "$desc" ]] && desc="Markdown documentation"
            echo "$desc"
            ;;
        *.json)
            case "$filename" in
                "package.json") echo "Node.js package configuration" ;;
                "pyproject.toml"|"poetry.lock") echo "Python package configuration" ;;
                *) echo "JSON configuration file" ;;
            esac
            ;;
        *.toml)
            case "$filename" in
                "pyproject.toml") echo "Python project configuration and dependencies" ;;
                *) echo "TOML configuration file" ;;
            esac
            ;;
        *.txt|*.log)
            case "$filename" in
                "errors.txt") echo "Error logs and debugging information" ;;
                "requirements.txt") echo "Python package dependencies" ;;
                *.log) echo "Application log file" ;;
                *) echo "Text file" ;;
            esac
            ;;
        "LICENSE"|"LICENCE") echo "Project license information" ;;
        "README"|"README.md") echo "Project overview and documentation" ;;
        "aboutthisfolder.md") echo "Auto-generated folder documentation" ;;
        ".gitignore") echo "Git ignore patterns" ;;
        ".env"|".env.example") echo "Environment variables configuration" ;;
        *)
            # Generic description based on extension
            local ext="${filename##*.}"
            case "$ext" in
                "html") echo "HTML web page" ;;
                "css") echo "CSS stylesheet" ;;
                "js") echo "JavaScript source file" ;;
                "yml"|"yaml") echo "YAML configuration file" ;;
                "xml") echo "XML data file" ;;
                *) echo "Project file" ;;
            esac
            ;;
    esac
}

# Function to analyze folder content and generate overview
generate_folder_overview() {
    local dir="$1"
    local folder_name="$2"
    local overview=""
    
    # Count different file types (including hidden files in all subdirectories)
    local py_count=$(find "$dir" -maxdepth 3 -name "*.py" 2>/dev/null | wc -l)
    local md_count=$(find "$dir" -maxdepth 3 -name "*.md" 2>/dev/null | wc -l)
    local sh_count=$(find "$dir" -maxdepth 3 -name "*.sh" 2>/dev/null | wc -l)
    local config_count=$(find "$dir" -maxdepth 3 \( -name "*.json" -o -name "*.toml" -o -name "*.yml" -o -name "*.yaml" \) 2>/dev/null | wc -l)
    # Count all immediate subdirectories (including hidden ones)
    local subdirs=$(find "$dir" -maxdepth 1 -type d ! -path "$dir" 2>/dev/null | wc -l)
    
    # Generate content-based overview
    case "$folder_name" in
        "ai-docs")
            overview="This folder serves as the central hub for all AI-related documentation, including:\n\n"
            if [[ $subdirs -gt 0 ]]; then
                local subdir_list=$(find "$dir" -maxdepth 1 -type d ! -path "$dir" -exec basename {} \; 2>/dev/null | sort | tr '\n' ', ' | sed 's/, $//')
                overview+="- **Organized documentation** across $subdirs categories: $subdir_list\n"
            fi
            if [[ $md_count -gt 0 ]]; then
                overview+="- **Documentation files** ($md_count files) covering project setup, API references, and guides\n"
            fi
            overview+="- **Development notes** and conversation logs for AI-assisted development\n"
            overview+="- **API documentation** with auto-generated references\n"
            overview+="- **Setup guides** for various tools and environments"
            ;;
        "src")
            overview="This folder contains the core implementation of the Create Python Project package:\n\n"
            if [[ $py_count -gt 0 ]]; then
                overview+="- **Python modules** ($py_count files) implementing the main functionality\n"
            fi
            overview+="- **Package structure** organized by feature areas\n"
            overview+="- **Utility modules** for common operations\n"
            overview+="- **Main application logic** and entry points"
            ;;
        "tests")
            overview="This folder contains the test suite for ensuring code quality and reliability:\n\n"
            if [[ $py_count -gt 0 ]]; then
                overview+="- **Test files** ($py_count files) covering unit and integration tests\n"
            fi
            overview+="- **Test fixtures** and helper utilities\n"
            overview+="- **Coverage reports** and test configuration\n"
            overview+="- **Automated testing** for continuous integration"
            ;;
        "scripts")
            overview="This folder contains automation scripts for development workflow:\n\n"
            if [[ $sh_count -gt 0 ]]; then
                overview+="- **Shell scripts** ($sh_count files) for build and deployment automation\n"
            fi
            if [[ $py_count -gt 0 ]]; then
                overview+="- **Python scripts** ($py_count files) for specialized tasks\n"
            fi
            overview+="- **Development tools** for code quality and formatting\n"
            overview+="- **CI/CD automation** and deployment scripts"
            ;;
        *)
            # Generic overview based on content analysis
            overview="This folder contains:\n\n"
            if [[ $py_count -gt 0 ]]; then
                overview+="- **Python files** ($py_count files) for implementation\n"
            fi
            if [[ $md_count -gt 0 ]]; then
                overview+="- **Documentation** ($md_count files) with guides and references\n"
            fi
            if [[ $sh_count -gt 0 ]]; then
                overview+="- **Scripts** ($sh_count files) for automation\n"
            fi
            if [[ $config_count -gt 0 ]]; then
                overview+="- **Configuration** ($config_count files) for tools and settings\n"
            fi
            if [[ $subdirs -gt 0 ]]; then
                overview+="- **Subdirectories** ($subdirs folders) for organized content"
            fi
            ;;
    esac
    
    echo -e "$overview"
}

# Function to create/update aboutthisfolder.md files
create_folder_documentation() {
    echo "Updating folder documentation files..."

    # Get all directories in the project root (including hidden directories that are tracked by git)
    local all_dirs=()
    local hidden_dirs=()
    local gitignored_dirs=()
    local tracked_hidden_dirs=()
    
    # Find all immediate directories in the project root ONLY (first level)
    while IFS= read -r dir; do
        dir_name=$(basename "$dir")
        
        # Check if directory is git-ignored
        if is_git_ignored "$dir"; then
            gitignored_dirs+=("$dir")
            continue
        fi
        
        # Skip system and development directories that don't need documentation
        if [[ "$dir_name" == ".git" || "$dir_name" == ".vscode" || "$dir_name" == "__pycache__" || "$dir_name" == "node_modules" ]]; then
            continue
        fi
        
        # Track hidden directories separately (only meaningful ones)
        if [[ "$dir_name" == .* ]]; then
            # Only include specific hidden directories that are meaningful for documentation
            if [[ "$dir_name" == ".config" || "$dir_name" == ".github" || "$dir_name" == ".claude" ]]; then
                tracked_hidden_dirs+=("$dir")
            fi
            continue
        fi
        
        all_dirs+=("$dir")
    done < <(find "${PROJECT_DIR}" -maxdepth 1 -type d | grep -v "^${PROJECT_DIR}\$")
    
    # Add tracked hidden directories to all_dirs
    for dir in "${tracked_hidden_dirs[@]}"; do
        all_dirs+=("$dir")
    done
    
    # Log what we're doing
    if [[ "$VERBOSE" == "true" ]]; then
        echo "Found ${#all_dirs[@]} root-level directories to document"
        echo "Including ${#tracked_hidden_dirs[@]} tracked hidden directories"
        
        if [[ ${#tracked_hidden_dirs[@]} -gt 0 && "$VERBOSE" == "true" ]]; then
            for tracked_hidden_dir in "${tracked_hidden_dirs[@]}"; do
                echo "  - $(basename "$tracked_hidden_dir") (hidden but tracked)"
            done
        fi
        
        echo "Skipping ${#gitignored_dirs[@]} gitignored directories"
        
        if [[ ${#gitignored_dirs[@]} -gt 0 && "$VERBOSE" == "true" ]]; then
            for gitignored_dir in "${gitignored_dirs[@]}"; do
                echo "  - $(basename "$gitignored_dir") (gitignored)"
            done
        fi
    fi

    # Process each directory
    for dir in "${all_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            local folder_name=$(basename "$dir")
            local doc_file="$dir/aboutthisfolder.md"
            local folder_description=""
            local folder_purpose=""
            local max_depth=2  # Default depth for most folders

            # Enhanced folder purpose and description
            case "$folder_name" in
                "src")
                    folder_description="Source code for the Create Python Project package"
                    folder_purpose="Contains the main application code, utilities, and implementation of all features for the Python project creation tool."
                    max_depth=3
                    ;;
                "tests")
                    folder_description="Test suite for the Create Python Project package"
                    folder_purpose="Contains comprehensive test files that verify functionality, ensure code quality, and enable continuous integration."
                    ;;
                "scripts")
                    folder_description="Development and automation scripts"
                    folder_purpose="Contains helper scripts for development workflow, build automation, documentation generation, and deployment tasks."
                    ;;
                "ai-docs")
                    folder_description="AI-assisted development documentation hub"
                    folder_purpose="Central repository for all AI-related documentation, including API references, setup guides, conversation logs, and development notes."
                    max_depth=2
                    ;;
                "logs")
                    folder_description="Application and build log files"
                    folder_purpose="Contains log output from application runs, build processes, and debugging sessions."
                    ;;
                "imagesandvids")
                    folder_description="Media assets and visual resources"
                    folder_purpose="Contains images, videos, and other media files used in documentation, UI, or project demonstrations."
                    ;;
                "TaskMasterTasks")
                    folder_description="Task management and workflow organization"
                    folder_purpose="Contains task definitions, workflow configurations, and project management resources."
                    ;;
                ".config")
                    folder_description="Development tool configurations"
                    folder_purpose="Contains configuration files for linters, formatters, type checkers, and other development tools."
                    ;;
                ".vscode")
                    folder_description="Visual Studio Code workspace configuration"
                    folder_purpose="Contains VS Code specific settings, tasks, launch configurations, and extension recommendations."
                    ;;
                *)
                    # Generic handling for unknown folders
                    if [[ "$folder_name" == .* ]]; then
                        folder_description="Configuration directory"
                        folder_purpose="Contains configuration and system files for $folder_name."
                    else
                        folder_description="Project directory"
                        folder_purpose="Contains project files and resources related to $folder_name functionality."
                    fi
                    ;;
            esac

            # Check if the folder contents have changed since the last aboutthisfolder.md update
            local should_update=true
            if [[ -f "$doc_file" ]]; then
                local doc_timestamp=$(stat -c %Y "$doc_file" 2>/dev/null || echo 0)
                
                # Comprehensive change detection for files, hidden files, and directories
                # Check for newer files (including hidden files) - additions and modifications
                local newer_files=$(find "$dir" -not -path "$doc_file" -newer "$doc_file" 2>/dev/null | wc -l)
                
                # Count all files (including hidden files) in all subdirectories
                local current_file_count=$(find "$dir" -type f -not -path "$doc_file" 2>/dev/null | wc -l)
                
                # Count all directories (including hidden directories) in all subdirectories
                local current_dir_count=$(find "$dir" -type d -not -path "$dir" 2>/dev/null | wc -l)
                
                # Combined count for comprehensive tracking
                local current_total_count=$((current_file_count + current_dir_count))
                
                # Get previous counts from documentation
                local previous_file_count=0
                local previous_dir_count=0
                local previous_total_count=0
                
                if [[ -f "$doc_file" ]]; then
                    # Extract file count from the existing documentation (files listed with backticks, no trailing /)
                    previous_file_count=$(grep -c "^- \*\*\`[^/]*\`\*\* -" "$doc_file" 2>/dev/null || echo "0")
                    # Extract directory count from the existing documentation (directories with trailing /)
                    previous_dir_count=$(grep -c "^- \*\*\`[^/]*/\`\*\* -" "$doc_file" 2>/dev/null || echo "0")
                    
                    # Ensure we have valid numbers
                    [[ -z "$previous_file_count" || ! "$previous_file_count" =~ ^[0-9]+$ ]] && previous_file_count=0
                    [[ -z "$previous_dir_count" || ! "$previous_dir_count" =~ ^[0-9]+$ ]] && previous_dir_count=0
                    
                    previous_total_count=$((previous_file_count + previous_dir_count))
                fi
                
                # Store current counts in a history file for tracking
                local doc_history_file="$dir/.doc_history"
                echo "files:$current_file_count" > "$doc_history_file"
                echo "dirs:$current_dir_count" >> "$doc_history_file"
                echo "total:$current_total_count" >> "$doc_history_file"
                echo "timestamp:$(date +%s)" >> "$doc_history_file"
                
                # Update if there are newer items OR if counts changed (files, directories, or total)
                if [[ $newer_files -eq 0 && $current_total_count -eq $previous_total_count ]]; then
                    should_update=false
                    if [[ "$VERBOSE" == "true" ]]; then
                        echo "Skipping $folder_name folder - contents unchanged (files: $current_file_count, dirs: $current_dir_count, total: $current_total_count, newer: $newer_files)"
                    fi
                else
                    if [[ "$VERBOSE" == "true" ]]; then
                        echo "Updating $folder_name folder - detected changes:"
                        echo "  Files: $current_file_count (was: $previous_file_count)"
                        echo "  Directories: $current_dir_count (was: $previous_dir_count)" 
                        echo "  Total items: $current_total_count (was: $previous_total_count)"
                        echo "  Newer items: $newer_files"
                    fi
                fi
            fi

            # Only update the file if the folder contents have changed or the file doesn't exist
            if [[ "$should_update" == true ]]; then
                echo "Creating/updating documentation for $folder_name folder..."
                
                # Generate the aboutthisfolder.md file with enhanced content
                cat > "$doc_file" << EOF
<!-- filepath: $doc_file -->
# ${folder_name^} Folder

$folder_description

## Purpose

$folder_purpose

## Overview

$(generate_folder_overview "$dir" "$folder_name")

## Files and Directories

EOF

                # Add detailed file and directory descriptions (including hidden items)
                # Use find to get all immediate items including hidden files and directories
                local all_items=()
                
                # Get all files and directories in the immediate directory, including hidden ones
                while IFS= read -r -d '' item; do
                    local item_name=$(basename "$item")
                    # Skip the aboutthisfolder.md file itself and .doc_history
                    if [[ "$item_name" != "aboutthisfolder.md" && "$item_name" != ".doc_history" ]]; then
                        all_items+=("$item_name")
                    fi
                done < <(find "$dir" -maxdepth 1 -not -path "$dir" -print0 2>/dev/null | sort -z)
                
                if [[ ${#all_items[@]} -gt 0 ]]; then
                    for item in "${all_items[@]}"; do
                        local item_path="$dir/$item"
                        if [[ -f "$item_path" ]]; then
                            local desc=$(get_semantic_description "$item_path" "$folder_name")
                            echo "- **\`$item\`** - $desc" >> "$doc_file"
                        elif [[ -d "$item_path" ]]; then
                            # Count all items in subdirectory (including hidden files and nested directories)
                            local count=$(find "$item_path" -type f -o -type d 2>/dev/null | wc -l)
                            # Subtract 1 to exclude the directory itself from the count
                            count=$((count - 1))
                            local dir_desc=""
                            case "$item" in
                                "utils") dir_desc="Utility modules and helper functions" ;;
                                "api") dir_desc="API documentation and references" ;;
                                "setup") dir_desc="Installation and configuration guides" ;;
                                "security") dir_desc="Security documentation and best practices" ;;
                                "workflows") dir_desc="Development workflow documentation" ;;
                                "mcp-explainers") dir_desc="Model Context Protocol service documentation" ;;
                                "tests") dir_desc="Test files and test utilities" ;;
                                "scripts") dir_desc="Automation and utility scripts" ;;
                                "development") dir_desc="Development notes and documentation" ;;
                                "historical") dir_desc="Historical documentation and archived files" ;;
                                "templates") dir_desc="Template files and boilerplate code" ;;
                                "__pycache__") dir_desc="Python bytecode cache (auto-generated)" ;;
                                ".git") dir_desc="Git version control data" ;;
                                ".github") dir_desc="GitHub Actions and repository configuration" ;;
                                ".config") dir_desc="Development tool configurations" ;;
                                ".vscode") dir_desc="VS Code workspace settings" ;;
                                "node_modules") dir_desc="Node.js dependencies" ;;
                                *) 
                                    if [[ "$item" == .* ]]; then
                                        dir_desc="Hidden directory containing $count items"
                                    else
                                        dir_desc="Directory containing $count items"
                                    fi
                                    ;;
                            esac
                            echo "- **\`$item/\`** - $dir_desc" >> "$doc_file"
                        fi
                    done
                else
                    echo "*(Empty directory)*" >> "$doc_file"
                fi

                # Add navigation section for complex folders
                if [[ "$folder_name" == "ai-docs" ]]; then
                    cat >> "$doc_file" << EOF

## Quick Navigation

### Getting Started
- **\`README.md\`** - Start here for an overview of all documentation
- **\`setup/MCP_SETUP.md\`** - Essential setup guide for new users

### Development Resources
- **\`api/\`** - Auto-generated API documentation
- **\`workflows/\`** - Development workflow guides
- **\`security/\`** - Security configuration guides

### Reference Materials
- **\`mcp-explainers/\`** - Service-specific documentation
- **\`handover.md\`** - Detailed project status and recent changes
EOF
                elif [[ "$folder_name" == "scripts" ]]; then
                    cat >> "$doc_file" << EOF

## Common Tasks

### Documentation
- **\`update_documentation.sh\`** - Regenerate all project documentation
- **\`manage_docs.sh\`** - Watch for changes and auto-update docs

### Development Workflow
- **\`ai_commit_workflow.sh\`** - AI-assisted commit message generation
- **\`lint_all.py\`** - Run all linting and formatting tools

### Build and Deploy
- **\`clean_run.py\`** - Clean build and run the application
- **\`force_push_to_remotes.sh\`** - Deploy to multiple git remotes
EOF
                fi

                # Add footer
                cat >> "$doc_file" << EOF

## Last Updated

This documentation was automatically generated on: $TIMESTAMP

---
*This file is auto-generated. Do not edit manually - changes will be overwritten.*
EOF

                echo "✅ Created/updated documentation for $folder_name folder"
            fi
        fi
    done
}

# Function to clean up aboutthisfolder.md files from unwanted directories
cleanup_unwanted_documentation() {
    echo "Cleaning up unwanted aboutthisfolder.md files..."
    
    # List of directories where we DON'T want aboutthisfolder.md files
    local unwanted_dirs=(
        ".git"
        ".vscode" 
        ".mypy_cache"
        ".pytest_cache"
        ".ruff_cache"
        ".venv"
        ".cursor"
        "__pycache__"
        "node_modules"
    )
    
    # Remove aboutthisfolder.md from unwanted directories
    for unwanted_dir in "${unwanted_dirs[@]}"; do
        local unwanted_file="${PROJECT_DIR}/${unwanted_dir}/aboutthisfolder.md"
        if [[ -f "$unwanted_file" ]]; then
            rm "$unwanted_file"
            echo "✅ Removed unwanted documentation from $unwanted_dir"
        fi
    done
    
    # Also check for any aboutthisfolder.md files deeper than first level and remove them
    while IFS= read -r deep_file; do
        # Calculate depth relative to project root
        local relative_path="${deep_file#${PROJECT_DIR}/}"
        local depth=$(echo "$relative_path" | grep -o "/" | wc -l)
        
        # If depth > 1, it's deeper than first level, so remove it
        if [[ $depth -gt 1 ]]; then
            local dir_path=$(dirname "$deep_file")
            local relative_dir="${dir_path#${PROJECT_DIR}/}"
            rm "$deep_file"
            echo "✅ Removed deep documentation from $relative_dir (depth: $depth)"
        fi
    done < <(find "${PROJECT_DIR}" -name "aboutthisfolder.md" -type f 2>/dev/null)
}

# Function to update the main README.md file
update_readme() {
    echo "Updating README.md with project overview..."

    local readme_file="${PROJECT_DIR}/README.md"

    # Auto-detect recent changes for changelog
    local recent_changes=""
    if git log --oneline --since="7 days ago" | head -5 | grep -qE "(add|feat|fix|update)"; then
        recent_changes="$(git log --oneline --since="7 days ago" --pretty=format:"- %s" | head -3)"
    fi

    # Get the list of all tracked directories
    local all_dirs=()
    local tracked_hidden_dirs=()
    
    # Find all immediate directories in the project root
    while IFS= read -r dir; do
        dir_name=$(basename "$dir")
        
        # Skip directories that are git-ignored
        if is_git_ignored "$dir"; then
            continue
        fi
        
        # Handle hidden directories separately
        if [[ "$dir_name" == .* ]]; then
            tracked_hidden_dirs+=("$dir_name")
        else
            all_dirs+=("$dir_name")
        fi
    done < <(find "${PROJECT_DIR}" -maxdepth 1 -type d | grep -v "^${PROJECT_DIR}\$")
    
    # Sort the directory arrays
    IFS=$'\n' all_dirs=($(sort <<< "${all_dirs[*]}"))
    IFS=$'\n' tracked_hidden_dirs=($(sort <<< "${tracked_hidden_dirs[*]}"))
    unset IFS

    # Generate a project structure section if it doesn't exist
    if ! grep -q "## Project Structure" "$readme_file"; then
        # Create a structured section
        local structure_content="\n## Project Structure\n\nThe project is organized as follows:\n\n"
        
        # Add visible directories first
        for dir in "${all_dirs[@]}"; do
            structure_content+="- **$dir/**: "
            
            # Add a brief description based on folder name
            case "$dir" in
                "src")
                    structure_content+="Main implementation code\n"
                    ;;
                "tests")
                    structure_content+="Test files for the project\n"
                    ;;
                "scripts")
                    structure_content+="Automation scripts for development workflow\n"
                    ;;
                "ai-docs")
                    structure_content+="AI-related documentation and conversation logs\n"
                    ;;
                "logs")
                    structure_content+="Log output files\n"
                    ;;
                *)
                    structure_content+="Project files\n"
                    ;;
            esac
        done
        
        # Add tracked hidden directories
        if [[ ${#tracked_hidden_dirs[@]} -gt 0 ]]; then
            structure_content+="\n### Configuration Directories\n\n"
            for dir in "${tracked_hidden_dirs[@]}"; do
                structure_content+="- **$dir/**: "
                
                # Add a brief description based on folder name
                case "$dir" in
                    ".config")
                        structure_content+="Configuration files for linters and tools\n"
                        ;;
                    ".vscode")
                        structure_content+="VS Code specific settings and tasks\n"
                        ;;
                    ".github")
                        structure_content+="GitHub workflows and configuration\n"
                        ;;
                    *)
                        structure_content+="Configuration files\n"
                        ;;
                esac
            done
        fi
        
        # Append to README.md
        echo -e "$structure_content" >> "$readme_file"
    fi

    # Only update the last updated section without changing the core content
    if grep -q "## Last Updated" "$readme_file"; then
        # Update the "Last Updated" section
        sed -i "/## Last Updated/,/^$/c\\## Last Updated\\n\\nThis project was last updated on: $TIMESTAMP\\n\\nRun \`./scripts/update_documentation.sh\` to update documentation.\\n" "$readme_file"
    else
        # Add the "Last Updated" section if it doesn't exist
        echo -e "\n## Last Updated\n\nThis project was last updated on: $TIMESTAMP\n\nRun \`./scripts/update_documentation.sh\` to update documentation.\n" >> "$readme_file"
    fi

    echo "README.md updated successfully"
}

# Function to update the convo.md file with more detailed changelog
update_convo_md() {
    echo "Updating convo.md with documentation changes..."

    local convo_file="${PROJECT_DIR}/ai-docs/convo.md"
    local temp_file="${PROJECT_DIR}/ai-docs/convo.md.tmp"
    local update_hash="doc_update_$(date '+%Y%m%d')"
    local update_marker="<!-- $update_hash -->"

    # Check if the file exists
    if [[ -f "$convo_file" ]]; then
        # Create a backup of the original file
        cp "$convo_file" "${convo_file}.bak"

        # Check if we've already updated today (using a hidden marker)
        if grep -q "$update_marker" "$convo_file"; then
            return 0
        fi

        # Check if there's an existing Updates section for today
        if grep -q "## Latest Updates ($DATE_ONLY)" "$convo_file"; then
            # Updates section exists, need to update it
            # Extract the file up to the "### Changes Made" line
            sed -n '1,/### Changes Made/p' "$convo_file" > "$temp_file"

            # Add our update marker as a hidden HTML comment
            echo "$update_marker" >> "$temp_file"

            # Add documentation update entry
            echo "1. **Documentation System Enhancement**" >> "$temp_file"
            echo "   - Improved documentation generation script with automatic folder scanning" >> "$temp_file"
            echo "   - Added/updated aboutthisfolder.md files in all main directories" >> "$temp_file"
            echo "   - Enhanced API documentation with comprehensive module detection" >> "$temp_file"
            echo "   - Updated README.md and convo.md with latest changes" >> "$temp_file"
            echo "   - Added timestamp tracking for all documentation updates" >> "$temp_file"
            echo "" >> "$temp_file"

            # Find the next section after "### Changes Made"
            local next_section_line=$(grep -n -A 1 "^##" "$convo_file" | grep -v "Latest Updates ($DATE_ONLY)" | head -1 | cut -d'-' -f1)

            if [[ -n "$next_section_line" ]]; then
                # If there's another section, append everything from that line to the end
                tail -n +"$next_section_line" "$convo_file" >> "$temp_file"
            else
                # If there's no other section, just add the Project Structure section
                echo "## Project Structure" >> "$temp_file"
                echo "" >> "$temp_file"
                echo "The project is organized as follows:" >> "$temp_file"
                echo "" >> "$temp_file"
                echo "- **src/create_python_project/**: Main implementation code" >> "$temp_file"
                echo "  - **utils/**: Utility modules and helper functions" >> "$temp_file"
                echo "- **tests/**: Test files for the project" >> "$temp_file"
                echo "- **scripts/**: Automation scripts for development workflow" >> "$temp_file"
                echo "- **ai-docs/**: AI-related documentation and conversation logs" >> "$temp_file"
                echo "- **.config/**: Configuration files for linters and tools" >> "$temp_file"
                echo "- **.vscode/**: VS Code specific settings and tasks" >> "$temp_file"
            fi

            # Replace the original file with our updated version
            mv "$temp_file" "$convo_file"
        else
            mv "$temp_file" "$convo_file"
        fi

        echo "convo.md updated successfully"
    else
        # Create a new file if it doesn't exist
        echo "<!-- filepath: $convo_file -->" > "$temp_file"
        echo "# Engineering Assessment for Create Python Project" >> "$temp_file"
        echo "" >> "$temp_file"
        echo "## Latest Updates ($DATE_ONLY)" >> "$temp_file"
        echo "" >> "$temp_file"
        echo "### Changes Made" >> "$temp_file"

        # Add our update marker as a hidden HTML comment
        echo "$update_marker" >> "$temp_file"

        echo "1. **Documentation System Enhancement**" >> "$temp_file"
        echo "   - Improved documentation generation script with automatic folder scanning" >> "$temp_file"
        echo "   - Added/updated aboutthisfolder.md files in all main directories" >> "$temp_file"
        echo "   - Enhanced API documentation with comprehensive module detection" >> "$temp_file"
        echo "   - Updated README.md and convo.md with latest changes" >> "$temp_file"
        echo "   - Added timestamp tracking for all documentation updates" >> "$temp_file"
        echo "" >> "$temp_file"

        # Add project structure information
        echo "## Project Structure" >> "$temp_file"
        echo "" >> "$temp_file"
        echo "The project is organized as follows:" >> "$temp_file"
        echo "" >> "$temp_file"
        echo "- **src/create_python_project/**: Main implementation code" >> "$temp_file"
        echo "  - **utils/**: Utility modules and helper functions" >> "$temp_file"
        echo "- **tests/**: Test files for the project" >> "$temp_file"
        echo "- **scripts/**: Automation scripts for development workflow" >> "$temp_file"
        echo "- **ai-docs/**: AI-related documentation and conversation logs" >> "$temp_file"
        echo "- **.config/**: Configuration files for linters and tools" >> "$temp_file"
        echo "- **.vscode/**: VS Code specific settings and tasks" >> "$temp_file"

        # Replace the original file with our updated version
        mv "$temp_file" "$convo_file"

        echo "convo.md created successfully"
    fi

    # Note: We don't need to limit the file size here as the limit_markdown_files function
    # will handle that for all markdown files including convo.md
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

# Function to limit markdown files to 500 lines
limit_markdown_files() {
    echo "Limiting all markdown files to 500 lines maximum..."

    # Find all markdown files in the project
    find "${PROJECT_DIR}" -type f -name "*.md" | while read -r md_file; do
        # Skip files in .git directory
        if [[ "$md_file" == *".git/"* ]]; then
            continue
        fi

        # Count lines in the file
        local line_count=$(wc -l < "$md_file")

        # If the file has more than 500 lines, truncate it
        if [[ $line_count -gt 500 ]]; then
            local temp_file="${md_file}.tmp"
            
            # Create truncated version with first 250 lines and last 250 lines
            head -n 250 "$md_file" > "$temp_file"
            echo "" >> "$temp_file"
            echo "... (truncated for brevity) ..." >> "$temp_file"
            echo "" >> "$temp_file"
            tail -n 250 "$md_file" >> "$temp_file"
            
            # Replace original with truncated version
            mv "$temp_file" "$md_file"
            echo "Truncated $md_file from $line_count lines to 500 lines"
        fi
    done

    echo "All markdown files limited to 500 lines maximum"
}

# Function to track and report all updated files
track_updated_files() {
    echo "Tracking all updated files..."

    # Create a temporary file to store the list of modified files
    local track_file="${PROJECT_DIR}/ai-docs/updated_files.txt"

    # Store the current timestamp
    echo "Documentation update on $TIMESTAMP" > "$track_file"
    echo "----------------------------------------" >> "$track_file"

    # Find all non-hidden, non-gitignored root-level directories
    local check_dirs=()
    
    # Always include these important directories
    check_dirs+=("${PROJECT_DIR}/ai-docs")
    
    # Add all immediate directories in the project root (excluding hidden and gitignored)
    while IFS= read -r dir; do
        dir_name=$(basename "$dir")
        
        # Skip hidden directories except .config and .vscode (which may contain important files)
        if [[ "$dir_name" == .* && "$dir_name" != ".config" && "$dir_name" != ".vscode" ]]; then
            continue
        fi
        
        # Skip git-ignored directories
        if is_git_ignored "$dir"; then
            continue
        fi
        
        check_dirs+=("$dir")
    done < <(find "${PROJECT_DIR}" -maxdepth 1 -type d | grep -v "^${PROJECT_DIR}\$")
    
    if [[ "$VERBOSE" == "true" ]]; then
        echo "Checking ${#check_dirs[@]} directories for updates:"
        for dir in "${check_dirs[@]}"; do
            echo "  - $dir"
        done
    fi

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
echo "Starting documentation update process - $(date '+%Y-%m-%d %H:%M:%S')"

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
    
    # Find all non-hidden, non-gitignored root-level directories
    visible_dirs=()
    
    while IFS= read -r dir; do
        dir_name=$(basename "$dir")
        
        # Skip hidden directories
        if [[ "$dir_name" == .* ]]; then
            continue
        fi
        
        # Skip git-ignored directories
        if is_git_ignored "$dir"; then
            continue
        fi
        
        visible_dirs+=("$dir")
    done < <(find "${PROJECT_DIR}" -maxdepth 1 -type d | grep -v "^${PROJECT_DIR}\$")
    
    for dir in "${visible_dirs[@]}"; do
        echo "   - $(basename "$dir")/aboutthisfolder.md"
    done
    echo ""
    echo "3. Other Files:"
    echo "   - ${PROJECT_DIR}/README.md"
    echo "   - ${PROJECT_DIR}/ai-docs/convo.md"
    echo "   - ${PROJECT_DIR}/ai-docs/api/doc_updates.log"
    echo "   - ${PROJECT_DIR}/ai-docs/updated_files.txt"
    echo ""
    echo "4. File Size Limitation:"
    echo "   - All markdown files will be limited to 500 lines maximum"
    echo ""
    echo "To perform the actual update, run without the --list-only option."
else
    # Run all documentation functions
    generate_api_documentation
    create_folder_documentation
    update_readme
    update_convo_md
    check_sensitive_info
    # Limit all markdown files to 500 lines
    limit_markdown_files
    track_updated_files
fi

echo "Documentation process completed - $(date '+%Y-%m-%d %H:%M:%S')"
