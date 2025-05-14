"""
Tests for the ai_integration module.
"""

from typing import Any, Dict

import pytest

from create_python_project.utils.ai_integration import (
    AIProvider,
    get_available_ai_providers,
    select_ai_provider,
)


class TestAIProvider:
    """Tests for the AIProvider class."""

    def test_ai_provider_initialization(self) -> None:
        """Test initializing an AI provider."""
        # This test will fail until AIProvider is properly implemented
        with pytest.raises(NotImplementedError):
            provider = AIProvider()
            provider._get_api_key_env_var()

        with pytest.raises(NotImplementedError):
            provider = AIProvider()
            provider._get_model_env_var()

        with pytest.raises(NotImplementedError):
            provider = AIProvider()
            provider.generate_response("test prompt")


class TestGetAvailableAIProviders:
    """Tests for the get_available_ai_providers function."""

    def test_get_available_providers(self, mock_env_vars: Dict[str, str]) -> None:
        """Test getting available AI providers."""
        # Execute
        providers = get_available_ai_providers()

        # Assert
        assert isinstance(providers, dict), "Result should be a dictionary"
        assert len(providers) > 0, "No providers found"

        # Check for specific providers
        expected_providers = ["OpenAI", "Anthropic", "Perplexity", "DeepSeek", "Gemini"]
        for provider in expected_providers:
            assert any(
                provider.lower() in key.lower() for key in providers
            ), f"{provider} not found in providers"


class TestSelectAIProvider:
    """Tests for the select_ai_provider function."""

    def test_select_ai_provider(
        self, mock_env_vars: Dict[str, str], monkeypatch: Any
    ) -> None:
        """Test selecting an AI provider."""
        # Setup
        providers = {
            "OpenAI": "test_openai_model",
            "Anthropic": "test_anthropic_model",
            "Perplexity": "test_perplexity_model",
            "DeepSeek": "test_deepseek_model",
            "Gemini": "test_gemini_model",
        }

        # Mock user input to select the first provider
        monkeypatch.setattr("builtins.input", lambda _: "1")

        # Execute
        success, provider = select_ai_provider(providers)

        # Assert
        assert success, "Provider selection failed"
        assert provider is not None, "No provider selected"
        assert success, "Provider selection failed"
        assert provider is not None, "No provider selected"
