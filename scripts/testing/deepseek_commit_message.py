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
    load_dotenv(override=True)

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
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 150,
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

            # Clean up the message - handle multi-line messages properly
            if commit_message:
                # Remove common prefixes
                prefixes = ["Here is", "The commit message", "Generated:", "Message:", "Commit message:"]
                for prefix in prefixes:
                    if commit_message.startswith(prefix):
                        commit_message = (
                            commit_message[len(prefix) :].strip().lstrip(":")
                        )
                
                # Handle multi-line messages (keep up to 3 lines)
                lines = commit_message.split("\n")
                if len(lines) > 3:
                    lines = lines[:3]
                
                # Clean and limit each line
                cleaned_lines = []
                for i, line in enumerate(lines):
                    line = line.strip()
                    if line:
                        if i == 0:  # First line (title) - limit to 80 chars
                            if len(line) > 80:
                                line = line[:80].strip()
                        cleaned_lines.append(line)
                
                if cleaned_lines:
                    final_message = "\n".join(cleaned_lines)
                    print(final_message)
                else:
                    print("Update project files")
            else:
                print("Update project files")
        else:
            print("Update project files")
    except Exception:
        print("Update project files")


if __name__ == "__main__":
    main()
