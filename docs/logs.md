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
- linter_isort_YYYYMMDD.log - Isort linting results
- linter_ruff_YYYYMMDD.log - Ruff linting results
- linter_flake8_YYYYMMDD.log - Flake8 linting results
- linter_mypy_YYYYMMDD.log - Mypy linting results
- linter_pylint_YYYYMMDD.log - Pylint linting results

## Retention Policy

- Current logs are kept for 7 days
- Older logs are automatically archived with gzip compression
- Archives are stored in `logs/archive` directory

## Last Updated
2025-05-29 21:49:27
