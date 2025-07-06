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
                {"role": "user", "content": f"Create git commit message: {prompt}"},
            ],
            "max_tokens": 30,
            "temperature": 0.1,
        }

        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(data),
        )

        if response.status_code == 200:
            result = response.json()
            message = result["choices"][0]["message"]
            commit_message = message.get("content", "").strip()

            # Clean up the message - take only the first line and limit length
            if commit_message:
                commit_message = commit_message.split("\n")[0].strip()
                # Remove common prefixes
                prefixes = ["Here is", "The commit message", "Generated:", "Message:"]
                for prefix in prefixes:
                    if commit_message.startswith(prefix):
                        commit_message = (
                            commit_message[len(prefix) :].strip().lstrip(":")
                        )
                # Limit to reasonable length
                if len(commit_message) > 80:
                    commit_message = commit_message[:80].strip()
                print(commit_message)
            else:
                print("Update project files")
        else:
            print("Update project files")
    except Exception:
        print("Update project files")


if __name__ == "__main__":
    main()
