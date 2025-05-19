"""
Test fixtures and configuration for the Create Python Project tests.
"""

import shutil
import tempfile
from collections.abc import Generator
from typing import Any

import pytest


@pytest.fixture
def temp_dir() -> Generator[str, None, None]:
    """
    Create a temporary directory for testing.

    Yields:
        Path to the temporary directory
    """
    tmp_dir = tempfile.mkdtemp()
    yield tmp_dir
    shutil.rmtree(tmp_dir, ignore_errors=True)


@pytest.fixture
def mock_env_vars(monkeypatch: Any) -> dict[str, str]:
    """
    Create mock environment variables for testing.

    Args:
        monkeypatch: pytest's monkeypatch fixture

    Returns:
        Dictionary of mocked environment variables
    """
    env_vars = {
        "OPENAI_API_KEY": "test_openai_key",
        "OPENAI_MODEL": "test_openai_model",
        "ANTHROPIC_API_KEY": "test_anthropic_key",
        "ANTHROPIC_MODEL": "test_anthropic_model",
        "PERPLEXITY_API_KEY": "test_perplexity_key",
        "PERPLEXITY_MODEL": "test_perplexity_model",
        "DEEPSEEK_API_KEY": "test_deepseek_key",
        "DEEPSEEK_MODEL": "test_deepseek_model",
        "GOOGLE_API_KEY": "test_gemini_key",
        "GEMINI_MODEL": "test_gemini_model",
    }

    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)

    return env_vars
    return env_vars
