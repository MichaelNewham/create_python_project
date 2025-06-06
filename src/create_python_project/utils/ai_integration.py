#!/usr/bin/env python3
"""
AI Integration Module

This module handles integration with AI providers for project generation.
It supports multiple AI providers such as OpenAI, Anthropic, Perplexity, etc.
"""

import importlib.util
import logging
import os
from typing import TYPE_CHECKING, Any

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
        model = self.model or "gpt-4o-2025-05-13"
        if "gpt-4o-2025" in model.lower():
            return "GPT-4o (May 2025)"
        elif "o4-mini" in model.lower():
            return "GPT-4o-mini"
        elif "o4" in model.lower() or "gpt-4o" in model.lower():
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
            # Check if the module is available at runtime
            if importlib.util.find_spec("openai") is None:
                return False, "OpenAI package not installed. Run: pip install openai"

            # Import openai locally
            import openai

            openai.api_key = self.api_key

            # Use max_completion_tokens for newer models, max_tokens for older ones
            completion_params: dict[str, Any] = {
                "model": self.model or "gpt-4o-2025-05-13",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides concise Python project guidance.",
                    },
                    {"role": "user", "content": prompt},
                ],
            }

            # Only add temperature for models that support it
            if "o4-mini" not in (self.model or "").lower():
                completion_params["temperature"] = 0.7

            # Use appropriate token parameter based on model
            if "o4-mini" in (self.model or "").lower():
                completion_params["max_completion_tokens"] = 2500
            else:
                completion_params["max_tokens"] = 2500

            response = openai.chat.completions.create(**completion_params)

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
        model = self.model
        if not model:
            return "Claude (no model specified)"

        if "claude-3-haiku" in model.lower():
            return "Claude 3 Haiku"
        elif "claude-sonnet-4" in model.lower():
            return "Claude Sonnet 4"
        elif "claude-3-sonnet" in model.lower() or "claude-3.7-sonnet" in model.lower():
            return "Claude 3.7 Sonnet"
        elif "claude-3-opus" in model.lower() or "claude-3.5-opus" in model.lower():
            return "Claude 3.5 Opus"
        else:
            return model

    def generate_response(self, prompt: str) -> tuple[bool, str]:
        """Generate a response using Anthropic API."""
        try:
            # Check if the module is available at runtime
            if importlib.util.find_spec("anthropic") is None:
                return (
                    False,
                    "Anthropic package not installed. Run: pip install anthropic",
                )

            # Import anthropic locally
            import anthropic

            client = anthropic.Anthropic(api_key=self.api_key)

            system_prompt = (
                "You are a helpful assistant that provides concise Python "
                "project guidance."
            )

            if not self.model:
                return (
                    False,
                    "No Anthropic model specified. Please set ANTHROPIC_MODEL in your .env file",
                )

            message = client.messages.create(
                model=self.model,
                max_tokens=2500,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}],
            )

            # Extract text content from Anthropic response
            if hasattr(message.content, "__iter__") and len(message.content) > 0:
                # Handle list of TextBlock objects
                content_text = (
                    message.content[0].text
                    if hasattr(message.content[0], "text")
                    else str(message.content[0])
                )
            else:
                # Fallback to string conversion
                content_text = str(message.content)

            return True, content_text
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
                "max_tokens": 2500,
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
        model = self.model or "deepseek-reasoner"
        if "deepseek-coder" in model.lower():
            return "DeepSeek Coder"
        elif "deepseek-reasoner" in model.lower():
            return "DeepSeek Reasoner"
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
                "model": self.model or "deepseek-reasoner",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides concise Python project guidance.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": 2500,
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
        model = self.model or "gemini-3.5-pro-latest"
        if "gemini-3.5-pro" in model.lower():
            return "Gemini 3.5 Pro"
        elif "gemini-pro" in model.lower():
            return "Gemini Pro"
        elif "gemini-2.5-pro" in model.lower():
            return "Gemini 2.5 Pro"
        elif "gemini-1.5-pro" in model.lower():
            return "Gemini 1.5 Pro"
        else:
            return model

    def generate_response(self, prompt: str) -> tuple[bool, str]:
        """Generate a response using Gemini API."""
        try:
            # Check if the module is available at runtime
            if importlib.util.find_spec("google.generativeai") is None:
                return (
                    False,
                    "Google Generative AI package not installed. Run: pip install google-generativeai",
                )

            # Import google.generativeai locally
            import google.generativeai as genai
            from google.generativeai.types import HarmBlockThreshold, HarmCategory

            genai.configure(api_key=self.api_key)

            # Set up the model
            model = genai.GenerativeModel(self.model or "gemini-3.5-pro-latest")

            # Generate the response
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 2500,
                },
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                },
            )

            # Check if the response is valid
            if not response.text:
                return False, "Gemini API returned no content. Please try again."

            return True, response.text
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
        model = os.environ.get("OPENAI_MODEL", "gpt-4o-2025-05-13")
        providers["OpenAI"] = model

    # Check for Anthropic
    if os.environ.get("ANTHROPIC_API_KEY"):
        model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-0")
        providers["Anthropic"] = model

    # Check for Perplexity
    if os.environ.get("PERPLEXITY_API_KEY"):
        model = os.environ.get("PERPLEXITY_MODEL", "sonar")
        providers["Perplexity"] = model

    # Check for DeepSeek
    if os.environ.get("DEEPSEEK_API_KEY"):
        model = os.environ.get("DEEPSEEK_MODEL", "deepseek-reasoner")
        providers["DeepSeek"] = model

    # Check for Gemini (Google)
    if os.environ.get("GOOGLE_API_KEY"):
        model = os.environ.get("GEMINI_MODEL", "gemini-3.5-pro-latest")
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

    # Add the selection text
    console.print("\n[bold yellow]AI Selection:[/bold yellow]")
    console.print("  [dim]• Enter a number (1-5) to select an AI provider[/dim]")
    console.print("  [dim]• Press Enter to use the default (1)[/dim]")

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
