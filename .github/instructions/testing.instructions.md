---
applyTo: "**/test_*.py"
---
# Testing Standards for Python Code

## Test Structure
- All test files should be named `test_*.py`
- Tests should be organized to mirror the structure of the source code
- Use pytest as the testing framework
- Group related tests in classes prefixed with `Test`
- Use descriptive test names that explain what's being tested

## Test Functions
- Test function names should start with `test_` and describe what's being tested
- Follow the Arrange-Act-Assert pattern in tests:
  1. Set up the test data and conditions
  2. Perform the action being tested
  3. Assert the expected outcome
- Each test should ideally test one specific behavior

## Fixtures
- Use pytest fixtures for common setup and teardown
- Define fixtures at the appropriate scope (function, class, module, session)
- Use `conftest.py` for fixtures used across multiple test files
- Parameterize tests for multiple similar test cases

## Mocking
- Use `unittest.mock` or `pytest-mock` for mocking external dependencies
- Prefer `monkeypatch` for simple attribute/function replacements
- Mock at the lowest level possible (close to the external dependency)
- Reset all mocks in teardown

## Assertions
- Use pytest's built-in assertions rather than assert statements
- Use appropriate assertion functions for different types of checks
- Include clear failure messages in assertions
- For complex objects, assert specific attributes rather than entire objects

## Coverage
- Aim for at least 80% test coverage for all modules
- Focus on testing business logic and edge cases
- Don't write tests just to increase coverage
- Use `pytest-cov` to measure coverage

## Best Practices
- Tests should be deterministic (no random failures)
- Tests should be independent (can run in any order)
- No test should depend on external resources or services
- Clean up all resources and state changes after each test
