#!/usr/bin/env python3
"""
Generate a commit message using the DeepSeek API.
"""

import json
import os
import sys

import requests
from dotenv import load_dotenv


def main():
    """Main function to generate a commit message."""
    if len(sys.argv) < 2:
        print("Update project files")
        return

    prompt = sys.argv[1]
    load_dotenv()

    api_key = os.environ.get("DEEPSEEK_API_KEY")
    model = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")

    if not api_key:
        print("Update project files")
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
                    "content": (
                        "You are a git commit message generator. Output ONLY the commit message text with no explanations, "
                        "no formatting, no markdown, and no additional text. Do not start with phrases like 'Here is a commit message' "
                        "or explain your reasoning. Just output the exact text that should be used for the git commit."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 300,
        }

        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(data),
        )

        if response.status_code == 200:
            result = response.json()
            commit_message = result["choices"][0]["message"]["content"].strip()
            print(commit_message)
        else:
            print("Update project files")
    except Exception:
        print("Update project files")


if __name__ == "__main__":
    main()
