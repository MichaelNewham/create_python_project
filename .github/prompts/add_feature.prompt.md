---
mode: 'agent'
tools: ['codebase', 'file_search']
description: 'Add new feature to the project'
---
# Add New Feature to Create Python Project

Your goal is to implement a new feature in the Create Python Project CLI tool.

If not provided, ask for the feature name and description. Search #codebase to understand the current project structure and implementation patterns.

Follow these steps:
1. Analyze the current codebase to understand the architecture
2. Design the new feature to integrate seamlessly with existing code
3. Implement the feature following all project standards
4. Add appropriate tests for the new functionality
5. Update documentation to reflect the new feature

Requirements:
- Follow the [Python style guidelines](../instructions/python_style.instructions.md)
- For CLI components, follow the [CLI guidelines](../instructions/cli.instructions.md)
- Include detailed docstrings for all new functions and classes
- Ensure all new code has corresponding tests
- Maintain backward compatibility with existing functionality
- Add appropriate error handling for the new feature

After implementing, run tests to ensure the feature works as expected and doesn't break existing functionality.
