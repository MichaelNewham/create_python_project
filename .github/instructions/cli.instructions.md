---
applyTo: "**/create_python_project.py"
---
# CLI Development Guidelines

## Command Structure
- Use a consistent command structure: `create-python-project [options] <project_name>`
- Group related options logically
- Provide sensible defaults for all options
- Support both short (-h) and long (--help) option forms

## User Experience
- Provide clear, concise help text for all commands and options
- Include examples in help text for common use cases
- Use color in terminal output to highlight important information
- Show progress for long-running operations

## Error Handling
- Provide clear error messages that explain both what went wrong and how to fix it
- Handle common errors gracefully (e.g., missing dependencies, invalid inputs)
- Use appropriate exit codes for different error types
- Log detailed error information for debugging

## Input Validation
- Validate all user inputs before processing
- Confirm destructive operations before proceeding
- Provide clear feedback on invalid inputs
- Support interactive prompts for required information

## Output
- Make output concise by default
- Provide a verbose mode for detailed output
- Format output for both human readability and potential machine parsing
- Include timestamps for long-running operations

## Configuration
- Support configuration via environment variables
- Support configuration via config files
- Document all configuration options
- Validate configuration values at startup

## Testing
- Test all CLI command paths
- Test with various combinations of options
- Test error handling and edge cases
- Include integration tests that run the CLI as a subprocess
