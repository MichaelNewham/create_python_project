#!/usr/bin/env python3
"""Test ALL AI providers for Create Python Project workflow."""

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
    print("⚠️  Using existing env vars")


def test_provider(provider_name, provider_class):
    """Test a specific AI provider."""
    print(f"\n🧪 Testing {provider_name}...")

    try:
        provider = provider_class()
        print(f"   Model: {provider.model}")
        print(f"   API key: {'✅' if provider.api_key else '❌'}")

        if not provider.model or not provider.api_key:
            return False

        # Test project type determination with same prompt as main app
        from create_python_project.utils import ai_prompts

        prompt = ai_prompts.get_project_type_prompt(
            "test-cli-tool",
            "A command-line automation tool for file management",
            {"problem": "automate tasks", "users": "developers"},
        )

        success, response = provider.generate_response(prompt)

        if success:
            # Check if response contains valid project type
            for line in response.strip().split("\n"):
                if ":" in line:
                    proj_type = line.split(":", 1)[0].strip().lower()
                    valid_types = [
                        "cli",
                        "web",
                        "api",
                        "data",
                        "ai",
                        "library",
                        "automation",
                    ]
                    if proj_type in valid_types:
                        print(f"   ✅ Detected: '{proj_type}'")
                        return True
            print("   ⚠️  No valid type extracted")
            return False
        else:
            print(f"   ❌ API failed: {response[:50]}...")
            return False

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False


if __name__ == "__main__":
    print("🧪 Testing AI Providers")
    print("=" * 40)

    from create_python_project.utils import ai_integration

    # Test providers 1, 3, 4, 5 (DeepSeek, Perplexity, OpenAI, Gemini)
    test_providers = {
        "1. DeepSeek": ai_integration.DeepSeekProvider,
        "3. Perplexity": ai_integration.PerplexityProvider,
        "4. OpenAI": ai_integration.OpenAIProvider,
        "5. Gemini": ai_integration.GeminiProvider,
    }

    results = {}
    for name, provider_class in test_providers.items():
        results[name] = test_provider(name, provider_class)

    print("\n" + "=" * 40)
    print("📊 RESULTS:")
    for provider, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {provider}: {status}")

    working = sum(results.values())
    total = len(results)
    print(f"\nWorking: {working}/{total} providers")
