#!/usr/bin/env python3
"""
Test ALL AI provider integrations for Create Python Project workflow.
Tests each provider without running the full application.
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Load environment variables
try:
    from dotenv import load_dotenv

    load_dotenv()
    print("✅ Loaded .env file")
except ImportError:
    print("⚠️  python-dotenv not available, using existing env vars")


def test_provider(provider_name, provider_class):
    """Test a specific AI provider."""
    print(f"\n🧪 Testing {provider_name} Provider...")

    try:
        # Create provider instance
        provider = provider_class()
        print(f"✅ Created {provider_name} provider")
        print(f"   Display name: {provider.display_name}")
        print(f"   Model: {provider.model}")
        print(f"   API key set: {'Yes' if provider.api_key else 'No'}")

        if not provider.model:
            print(f"❌ No model specified in {provider._get_model_env_var()} env var")
            return False

        if not provider.api_key:
            print(f"❌ No API key found in {provider._get_api_key_env_var()} env var")
            return False

        # Test API call
        test_prompt = (
            "Respond with exactly 'API test successful' to confirm you are working."
        )
        print(f"🚀 Making API call to {provider_name}...")

        success, response = provider.generate_response(test_prompt)

        if success:
            print("✅ API call successful!")
            print(f"📤 Response: {response[:100]}...")
            return True
        else:
            print(f"❌ API call failed: {response}")
            return False

    except Exception as e:
        print(f"❌ Exception during {provider_name} test: {str(e)}")
        return False


def test_all_providers():
    """Test all available AI providers."""
    from create_python_project.utils import ai_integration

    # Get available providers
    available = ai_integration.get_available_ai_providers()
    print(f"Available providers: {list(available.keys())}")

    # Provider classes to test
    test_providers = {
        "DeepSeek": ai_integration.DeepSeekProvider,
        "Anthropic": ai_integration.AnthropicProvider,
        "Perplexity": ai_integration.PerplexityProvider,
        "OpenAI": ai_integration.OpenAIProvider,
        "Gemini": ai_integration.GeminiProvider,
    }

    results = {}

    for name, provider_class in test_providers.items():
        if name in available:
            results[name] = test_provider(name, provider_class)
        else:
            print(f"\n⚠️  {name} not available (missing API key)")
            results[name] = False

    return results


if __name__ == "__main__":
    print("🧪 Testing ALL AI Provider Integrations")
    print("=" * 60)

    results = test_all_providers()

    print("\n" + "=" * 60)
    print("📊 RESULTS SUMMARY:")

    for provider, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {provider}: {status}")

    total_pass = sum(results.values())
    total_tests = len(results)
    print(f"\nOverall: {total_pass}/{total_tests} providers working")
