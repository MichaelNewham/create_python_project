#!/usr/bin/env python3
"""
AI Integration Module

This module handles integration with AI providers for project generation.
It supports multiple AI providers such as OpenAI, Anthropic, Perplexity, etc.
"""
import logging
import os
from typing import TYPE_CHECKING

import requests
from rich.console import Console
from rich.prompt import Prompt

# Handle conditional imports for type checking
if TYPE_CHECKING:
    import anthropic
    import google.generativeai as genai  # type: ignore # noqa
    import openai


console = Console()

# Try to import the AI provider modules
try:
    import openai  # noqa: F811
except ImportError:
    openai = None  # type: ignore

try:
    import anthropic  # noqa: F811
except ImportError:
    anthropic = None  # type: ignore

try:
    import google.generativeai as genai  # type: ignore # noqa: F811
except ImportError:
    genai = None  # type: ignore


class AIProvider:
    """Base class for AI providers."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        """Initialize the AI provider."""
        self.api_key = api_key or os.environ.get(self._get_api_key_env_var(), "")
        self.model = model or os.environ.get(self._get_model_env_var(), "")
        self.name = self.__class__.__name__
        self.display_name = self._get_display_name()

    def _get_api_key_env_var(self) -> str:
        """Get the environment variable name for the API key."""
        raise NotImplementedError

    def _get_model_env_var(self) -> str:
        """Get the environment variable name for the model."""
        raise NotImplementedError

    def _get_display_name(self) -> str:
        """Get a user-friendly display name for the model."""
        raise NotImplementedError

    def generate_response(self, prompt: str) -> tuple[bool, str]:
        """Generate a response from the AI provider."""
        raise NotImplementedError


class OpenAIProvider(AIProvider):
    """Provider for OpenAI API."""

    def _get_api_key_env_var(self) -> str:
        return "OPENAI_API_KEY"

    def _get_model_env_var(self) -> str:
        return "OPENAI_MODEL"

    def _get_display_name(self) -> str:
        """Get a user-friendly display name for the model."""
        model = self.model or "o4-mini-2025-04-16"
        if "o4-mini" in model.lower():
            return "GPT-4o-mini"
        elif "o4" in model.lower():
            return "GPT-4o"
        elif "gpt-4" in model.lower():
            return "GPT-4"
        elif "gpt-3.5" in model.lower():
            return "GPT-3.5 Turbo"
        else:
            return model

    def generate_response(self, prompt: str) -> tuple[bool, str]:
        """Generate a response using OpenAI API."""
        try:
            if openai is None:
                return False, "OpenAI package not installed. Run: pip install openai"

            openai.api_key = self.api_key

            response = openai.chat.completions.create(
                model=self.model or "o4-mini-2025-04-16",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides concise Python project guidance.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=1000,
            )

            # Ensure we're returning a string
            content = str(response.choices[0].message.content or "")
            return True, content
        except Exception as e:
            return False, f"OpenAI API error: {str(e)}"


class AnthropicProvider(AIProvider):
    """Provider for Anthropic API."""

    def _get_api_key_env_var(self) -> str:
        return "ANTHROPIC_API_KEY"

    def _get_model_env_var(self) -> str:
        return "ANTHROPIC_MODEL"

    def _get_display_name(self) -> str:
        """Get a user-friendly display name for the model."""
        model = self.model or "claude-3-7-sonnet-20250219"
        if "claude-3-haiku" in model.lower():
            return "Claude 3 Haiku"
        elif "claude-3-sonnet" in model.lower() or "claude-3.7-sonnet" in model.lower():
            return "Claude 3.7 Sonnet"
        elif "claude-3-opus" in model.lower() or "claude-3.5-opus" in model.lower():
            return "Claude 3.5 Opus"
        else:
            return model

    def generate_response(self, prompt: str) -> tuple[bool, str]:
        """Generate a response using Anthropic API."""
        try:
            if anthropic is None:
                return (
                    False,
                    "Anthropic package not installed. Run: pip install anthropic",
                )

            client = anthropic.Anthropic(api_key=self.api_key)

            system_prompt = (
                "You are a helpful assistant that provides concise Python "
                "project guidance."
            )

            message = client.messages.create(
                model=self.model or "claude-3-7-sonnet-20250219",
                max_tokens=1000,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}],
            )

            # Safely extract text to avoid union type errors
            content = message.content
            if (
                content
                and len(content) > 0
                and isinstance(content[0], dict)
                and "text" in content[0]
            ):
                return True, content[0]["text"]

            return True, str(content)
        except Exception as e:
            return False, f"Anthropic API error: {str(e)}"


class PerplexityProvider(AIProvider):
    """Provider for Perplexity API."""

    def _get_api_key_env_var(self) -> str:
        return "PERPLEXITY_API_KEY"

    def _get_model_env_var(self) -> str:
        return "PERPLEXITY_MODEL"

    def _get_display_name(self) -> str:
        """Get a user-friendly display name for the model."""
        model = self.model or "sonar"
        if "sonar-small" in model.lower():
            return "Sonar Small"
        elif "sonar-medium" in model.lower() or model.lower() == "sonar":
            return "Sonar"
        elif "sonar-large" in model.lower():
            return "Sonar Large"
        else:
            return model

    def generate_response(self, prompt: str) -> tuple[bool, str]:
        """Generate a response using Perplexity API."""
        try:
            if not self.api_key:
                return (
                    False,
                    "Perplexity API key not found. Please check your PERPLEXITY_API_KEY environment variable.",
                )

            url = "https://api.perplexity.ai/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": self.model or "sonar",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides concise Python project guidance.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": 1000,
            }

            # Log request details for debugging (without API key)
            logging.debug(
                f"Sending request to Perplexity API with model: {payload['model']}"
            )

            response = requests.post(url, headers=headers, json=payload, timeout=30)

            # Check for HTTP errors
            response.raise_for_status()

            result = response.json()
            logging.debug("Received response from Perplexity API: %s", result)

            if "choices" not in result or not result.get("choices"):
                return (
                    False,
                    "Perplexity API returned an empty response. Please try again.",
                )

            content = (
                result.get("choices", [{}])[0].get("message", {}).get("content", "")
            )
            if not content:
                return False, "Perplexity API returned no content. Please try again."

            return True, content
        except requests.exceptions.Timeout:
            return False, "Perplexity API request timed out. Please try again later."
        except requests.exceptions.RequestException as e:
            return False, f"Perplexity API request error: {str(e)}"
        except ValueError as e:
            return False, f"Perplexity API JSON parsing error: {str(e)}"
        except Exception as e:
            return False, f"Perplexity API error: {str(e)}"


class DeepSeekProvider(AIProvider):
    """Provider for DeepSeek API."""

    def _get_api_key_env_var(self) -> str:
        return "DEEPSEEK_API_KEY"

    def _get_model_env_var(self) -> str:
        return "DEEPSEEK_MODEL"

    def _get_display_name(self) -> str:
        """Get a user-friendly display name for the model."""
        model = self.model or "deepseek-chat"
        if "deepseek-coder" in model.lower():
            return "DeepSeek Coder"
        elif "deepseek-chat" in model.lower():
            return "DeepSeek Chat"
        elif "deepseek-math" in model.lower():
            return "DeepSeek Math"
        else:
            return model

    def generate_response(self, prompt: str) -> tuple[bool, str]:
        """Generate a response using DeepSeek API."""
        try:
            url = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": self.model or "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides concise Python project guidance.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": 1000,
            }

            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()

            result = response.json()
            return True, result.get("choices", [{}])[0].get("message", {}).get(
                "content", ""
            )
        except Exception as e:
            return False, f"DeepSeek API error: {str(e)}"


class GeminiProvider(AIProvider):
    """Provider for Google Gemini API."""

    def _get_api_key_env_var(self) -> str:
        return "GOOGLE_API_KEY"

    def _get_model_env_var(self) -> str:
        return "GEMINI_MODEL"

    def _get_display_name(self) -> str:
        """Get a user-friendly display name for the model."""
        model = self.model or "gemini-2.5-pro-preview-05-06"
        if "gemini-pro" in model.lower():
            return "Gemini Pro"
        elif "gemini-2.5-pro" in model.lower():
            return "Gemini 2.5 Pro"
        elif "gemini-1.5-pro" in model.lower():
            return "Gemini 1.5 Pro"
        else:
            return model

    def generate_response(self, prompt: str) -> tuple[bool, str]:
        """Generate a response using Google Gemini API."""
        try:
            if genai is None:
                return (
                    False,
                    "Google Generative AI package not installed. Run: pip install google-generativeai",
                )

            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model or "gemini-2.5-pro-preview-05-06")

            response = model.generate_content(
                contents=[{"role": "user", "parts": [prompt]}],
            )

            # Safely access text attribute
            if hasattr(response, "text"):
                return True, response.text
            else:
                parts = getattr(response, "parts", [])
                if parts and len(parts) > 0:
                    return True, str(parts[0])
                return True, str(response)
        except Exception as e:
            return False, f"Gemini API error: {str(e)}"


def get_available_ai_providers() -> dict[str, str]:
    """
    Get a list of available AI providers based on environment variables.

    Returns:
        Dict mapping provider names to model names
    """
    providers = {}

    # Check for OpenAI
    if os.environ.get("OPENAI_API_KEY"):
        model = os.environ.get("OPENAI_MODEL", "o4-mini-2025-04-16")
        providers["OpenAI"] = model

    # Check for Anthropic
    if os.environ.get("ANTHROPIC_API_KEY"):
        model = os.environ.get("ANTHROPIC_MODEL", "claude-3-7-sonnet-20250219")
        providers["Anthropic"] = model

    # Check for Perplexity
    if os.environ.get("PERPLEXITY_API_KEY"):
        model = os.environ.get("PERPLEXITY_MODEL", "sonar")
        providers["Perplexity"] = model

    # Check for DeepSeek
    if os.environ.get("DEEPSEEK_API_KEY"):
        model = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
        providers["DeepSeek"] = model

    # Check for Gemini (Google)
    if os.environ.get("GOOGLE_API_KEY"):
        model = os.environ.get("GEMINI_MODEL", "gemini-2.5-pro-preview-05-06")
        providers["Gemini"] = model

    return providers


def select_ai_provider(providers: dict[str, str]) -> tuple[bool, AIProvider | None]:
    """
    Select an AI provider from the available providers.

    Args:
        providers: Dictionary of available providers

    Returns:
        Tuple containing success status and selected provider
    """
    if not providers:
        return False, None

    console.print("\n[bold magenta]Step 2: AI Integration[/bold magenta]")
    console.print("Select an AI provider:")
    providers_list = list(providers.keys())
    for i, provider in enumerate(providers_list, 1):
        model = providers[provider]

        # Create the appropriate provider instance to get display name
        provider_instance: AIProvider | None = None
        if provider == "OpenAI":
            provider_instance = OpenAIProvider(model=model)
        elif provider == "Anthropic":
            provider_instance = AnthropicProvider(model=model)
        elif provider == "Perplexity":
            provider_instance = PerplexityProvider(model=model)
        elif provider == "DeepSeek":
            provider_instance = DeepSeekProvider(model=model)
        elif provider == "Gemini":
            provider_instance = GeminiProvider(model=model)

        display_name = model
        if provider_instance:
            display_name = provider_instance.display_name

        console.print(f"[cyan]{i}.[/cyan] {provider} ({display_name})")

    try:
        default = 1
        selection_str = Prompt.ask("Enter your choice", default=str(default))
        selection = int(selection_str) if selection_str else default

        if selection < 1 or selection > len(providers_list):
            console.print(
                f"Invalid selection: {selection}. Must be between 1 and {len(providers_list)}",
                style="bold red",
            )
            return False, None

        provider_name = providers_list[selection - 1]
        model = providers[provider_name]

        # Create the appropriate provider instance
        selected_provider: AIProvider | None = None

        if provider_name == "OpenAI":
            selected_provider = OpenAIProvider(model=model)
        elif provider_name == "Anthropic":
            selected_provider = AnthropicProvider(model=model)
        elif provider_name == "Perplexity":
            selected_provider = PerplexityProvider(model=model)
        elif provider_name == "DeepSeek":
            selected_provider = DeepSeekProvider(model=model)
        elif provider_name == "Gemini":
            selected_provider = GeminiProvider(model=model)

        if selected_provider:
            console.print(
                f"\nUsing {provider_name} with model {selected_provider.display_name}"
            )
            return True, selected_provider

        # Fallback for unimplemented providers
        console.print(
            f"Support for {provider_name} is not fully implemented yet.",
            style="bold red",
        )
        return False, None
    except Exception as e:
        console.print(f"Error selecting AI provider: {str(e)}", style="bold red")
        return False, None
