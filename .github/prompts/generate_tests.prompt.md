---
mode: 'agent'
tools: ['codebase', 'file_search']
description: 'Generate a complete test file for a Python module'
---
# Generate Comprehensive Unit Tests

Your goal is to create a complete test file for a Python module using pytest.

If not provided, ask for the module name to test. Look for the module in #codebase to understand its functionality.

Requirements:
- Follow the [testing standards](../instructions/testing.instructions.md)
- Create test cases for all public functions and classes
- Include tests for edge cases and error conditions
- Organize tests in classes that mirror the module structure
- Use appropriate fixtures for test setup
- Include docstrings for test classes and complex test functions
- Aim for high test coverage of the module
- Use mocks for external dependencies to ensure tests are isolated

Once you've identified all the functionality to test, generate a complete test file that follows our project standards.
