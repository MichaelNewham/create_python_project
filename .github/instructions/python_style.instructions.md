---
applyTo: "**/*.py"
---
# Python Code Style Guidelines

## Formatting
- Follow PEP 8 conventions strictly
- Format code with Black using 88-character line length
- Use 4 spaces for indentation (not tabs)
- Use single quotes for strings unless the string contains single quotes
- Add a blank line at the end of each file
- Use trailing commas in multi-line data structures

## Variables and Functions
- Use descriptive names that convey intent
- Use snake_case for all variable and function names
- Use ALL_CAPS for constants and module-level variables that shouldn't change
- Avoid abbreviations unless they are standard in the domain

## Type Annotations
- Always include type hints for:
  - Function parameters
  - Return values
  - Class attributes when their type isn't obvious
- Use typing module for complex types (List, Dict, Optional, Union, etc.)
- Use collections.abc for container types in Python 3.9+

## Comments and Docstrings
- Every public function, class, and module should have a docstring
- Follow Google-style docstring format consistently
- Include Args, Returns, Raises, and Examples sections as appropriate
- Comment complex logic or non-obvious decisions, not obvious code

## Imports
- Organize imports in three groups:
  1. Standard library imports
  2. Third-party imports
  3. Local application/library imports
- Sort each group alphabetically
- One import per line
- Use absolute imports, not relative imports

## Best Practices
- Prefer dict.get() with a default value over checking if a key exists
- Use context managers (with statements) for resource management
- Use list/dict comprehensions for simple transformations instead of loops
- For complex list processing operations, prefer generator expressions to save memory
