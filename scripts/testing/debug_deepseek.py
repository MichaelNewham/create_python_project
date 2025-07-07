#!/usr/bin/env python3
"""
Debug version of DeepSeek commit message generator.
"""

import json
import os
import sys

import requests
from dotenv import load_dotenv


def main():
    """Main function to generate a commit message."""
    if len(sys.argv) < 2:
        print("No prompt provided")
        return

    prompt = sys.argv[1]
    print(f"Prompt: {prompt}")

    load_dotenv()

    api_key = os.environ.get("DEEPSEEK_API_KEY")
    model = os.environ.get("DEEPSEEK_MODEL", "deepseek-reasoner")

    print(f"API Key found: {bool(api_key)}")
    print(f"Model: {model}")

    if not api_key:
        print("No API key found")
        return

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "Generate concise git commit message. Output ONLY the message.",
                },
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 50,
            "temperature": 0.3,
        }

        print("Making API request...")
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(data),
            timeout=30,
        )

        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text[:500]}")

        if response.status_code == 200:
            result = response.json()
            commit_message = result["choices"][0]["message"]["content"].strip()
            print(f"Generated message: {commit_message}")
        else:
            print("API request failed")
    except Exception as e:
        print(f"Exception occurred: {e}")


if __name__ == "__main__":
    main()
