# Log Management Documentation

This document describes the logging system used in the project.

## Log Directory Structure



## Log Types

The following log files are maintained:

- linter_black_YYYYMMDD.log - Black linting results
- linter_ruff_YYYYMMDD.log - Ruff linting results
- linter_mypy_YYYYMMDD.log - Mypy type checking results

## Retention Policy

- Current logs are kept for 7 days
- Older logs are automatically archived with gzip compression
- Archives are stored in `logs/archive` directory

## Last Updated
2025-05-30 02:04:32
