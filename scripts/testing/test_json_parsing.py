#!/usr/bin/env python3
"""
Test the improved JSON parsing logic for Create Python Project
"""

import json
import os
import re
import sys
from typing import Any

# Add the source directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_json_parsing():
    """Test the improved JSON parsing logic."""

    # Test cases - different JSON response formats
    test_cases: list[dict[str, Any]] = [
        {
            "name": "Pure JSON",
            "response": '{"categories": [{"name": "test", "options": []}]}',
            "should_parse": True,
        },
        {
            "name": "Markdown wrapped JSON",
            "response": '```json\n{"categories": [{"name": "test", "options": []}]}\n```',
            "should_parse": True,
        },
        {
            "name": "Simple markdown wrapped",
            "response": '```\n{"categories": [{"name": "test", "options": []}]}\n```',
            "should_parse": True,
        },
        {
            "name": "Perplexity style",
            "response": """```json
{
  "categories": [
    {
      "name": "Backend Framework",
      "description": "The web framework",
      "options": [
        {
          "name": "FastAPI",
          "description": "Modern framework",
          "recommended": true
        }
      ]
    }
  ]
}
```""",
            "should_parse": True,
        },
        {
            "name": "Invalid JSON",
            "response": "This is not JSON at all",
            "should_parse": False,
        },
        {
            "name": "Partial JSON in text",
            "response": 'Here is the JSON you requested: {"categories": [{"name": "test"}]} - hope this helps!',
            "should_parse": True,  # Should work with regex fallback
        },
    ]

    print("Testing improved JSON parsing logic...\n")

    for test_case in test_cases:
        print(f"Testing: {test_case['name']}")
        tech_response: str = test_case["response"]

        # Apply the improved parsing logic
        parsed_successfully = False

        # Clean the response first - handle markdown-wrapped JSON
        cleaned_response = tech_response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]  # Remove ```json
        if cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:]  # Remove ```
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]  # Remove trailing ```
        cleaned_response = cleaned_response.strip()

        # First try parsing the cleaned response
        try:
            json.loads(cleaned_response)  # Validate JSON parsing
            print("  ✅ Successfully parsed JSON after cleaning")
            parsed_successfully = True
        except json.JSONDecodeError:
            # If cleaning didn't work, try direct parsing of original
            try:
                json.loads(tech_response)  # Validate JSON parsing
                print("  ✅ Successfully parsed JSON directly")
                parsed_successfully = True
            except json.JSONDecodeError:
                # If direct parsing fails, try to extract JSON using regex
                json_match = re.search(
                    r"(\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\})", tech_response
                )

                if json_match:
                    json_str = json_match.group(1)
                    try:
                        json.loads(json_str)  # Validate JSON parsing
                        print("  ✅ Successfully parsed extracted JSON")
                        parsed_successfully = True
                    except json.JSONDecodeError:
                        print("  ❌ JSON parsing failed even after extraction")
                else:
                    print("  ❌ No JSON pattern found in response")

        # Check if result matches expectation
        if parsed_successfully == test_case["should_parse"]:
            print("  ✅ Test passed!")
        else:
            print(
                f"  ❌ Test failed! Expected {test_case['should_parse']}, got {parsed_successfully}"
            )

        print()


if __name__ == "__main__":
    test_json_parsing()
