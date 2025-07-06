# Filesystem Tools Guide

This document provides an overview of Filesystem's capabilities through the Model Context Protocol (MCP) in VS Code. The Filesystem MCP server provides secure file and directory operations within authorized paths.

## File Operations

### 1. Read File
**Question:** "Can you read the contents of my package.json file?"  
**Tool:** `read_file`  
**Description:** Reads the entire contents of a file from the specified path. Returns the file content as text.

### 2. Read Multiple Files
**Question:** "Can you read all the JavaScript files in my components directory?"  
**Tool:** `read_multiple_files`  
**Description:** Reads multiple files in a single operation. Accepts an array of file paths and returns their contents.

### 3. Write File
**Question:** "Create a new configuration file with these settings."  
**Tool:** `write_file`  
**Description:** Creates or overwrites a file at the specified path with the provided content.

### 4. Edit File
**Question:** "Update the version number in my package.json from 1.0.0 to 1.1.0."  
**Tool:** `edit_file`  
**Description:** Makes specific edits to an existing file by replacing old content with new content.

### 5. Create File
**Question:** "Create a new README.md file for my project."  
**Tool:** `create_file`  
**Description:** Creates a new file at the specified path. Fails if the file already exists.

### 6. Delete File
**Question:** "Remove the temporary log file from my project."  
**Tool:** `delete_file`  
**Description:** Permanently deletes a file from the filesystem.

## Directory Operations

### 1. List Directory
**Question:** "What files are in my src directory?"  
**Tool:** `list_directory`  
**Description:** Lists all files and directories within a specified directory path.

### 2. Create Directory
**Question:** "Create a new components folder in my src directory."  
**Tool:** `create_directory`  
**Description:** Creates a new directory at the specified path, including parent directories if needed.

### 3. Move/Rename File
**Question:** "Rename my old-config.json to config.json."  
**Tool:** `move_file`  
**Description:** Moves or renames a file from one location to another.

### 4. Search Files
**Question:** "Find all files containing 'TODO' in my project."  
**Tool:** `search_files`  
**Description:** Searches for files containing specific text patterns within the authorized paths.

### 5. Get File Info
**Question:** "What are the details of this image file?"  
**Tool:** `get_file_info`  
**Description:** Retrieves metadata about a file including size, modification date, and permissions.

## Use Cases

### Project Setup

**Question:** "Set up a basic Express.js project structure."  
**Workflow:**
1. Use `create_directory` to create project folders (src, public, config)
2. Use `create_file` to generate package.json, app.js, and configuration files
3. Use `write_file` to add boilerplate code

### Code Refactoring

**Question:** "Move all utility functions to a separate utils directory."  
**Workflow:**
1. Use `create_directory` to create utils folder
2. Use `search_files` to find utility functions
3. Use `move_file` to relocate files
4. Use `edit_file` to update import statements

### Documentation Management

**Question:** "Update all markdown files to include a table of contents."  
**Workflow:**
1. Use `list_directory` to find all .md files
2. Use `read_multiple_files` to read their contents
3. Use `edit_file` to add table of contents to each file

### Configuration Updates

**Question:** "Update all environment configuration files with new API endpoints."  
**Workflow:**
1. Use `search_files` to find .env files
2. Use `read_file` to check current values
3. Use `edit_file` to update API endpoints

## Best Practices for Using Filesystem

### 1. Always Use Absolute Paths
The filesystem server requires absolute paths. Ensure your paths start from the authorized root directory.

### 2. Check Before Writing
Before creating or overwriting files, use `get_file_info` or `read_file` to check if the file exists and verify its contents.

### 3. Batch Operations
When working with multiple files, use `read_multiple_files` instead of multiple `read_file` calls for better performance.

### 4. Safe Edits
Use `edit_file` for modifying existing files rather than reading and rewriting the entire file content.

### 5. Backup Important Files
Before making significant changes, consider creating backup copies of important files.

### 6. Respect Path Boundaries
The filesystem server only allows operations within authorized paths. Attempting to access files outside these boundaries will result in errors.

## Security Considerations

### Path Restrictions
The filesystem server is configured with specific allowed paths. In your case, it has access to `/home/michaelnewham`. Operations outside this path will be denied.

### Permission Checks
All operations respect system file permissions. Ensure you have appropriate read/write permissions for the files you're working with.

### Safe Operations
Destructive operations like `delete_file` are irreversible. Always double-check paths before executing these commands.

## Integration with Other Tools

### With Memory MCP
Store frequently accessed file paths or configuration templates in memory for quick retrieval.

### With GitHub MCP
After making file changes, use GitHub tools to commit and push your modifications.

### With Context7
When working with library files, use Context7 to get documentation about the libraries you're modifying.

## Last Updated

This guide was last updated on: 2025-06-09