#!/usr/bin/env python3
# create_python_project.py - All-in-one Python project creator
# This is a self-contained script that creates Python projects with intelligent setup

import os
import sys
import tempfile
import subprocess
import argparse
import json
import re
import shutil
import logging
import random
import string
import time
import base64
import platform
from io import BytesIO
from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime, timedelta
from setuptools import setup, find_packages
from dotenv import load_dotenv

# Ensure project root is in sys.path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set up logging first before using it anywhere
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("project_creator")

def safely_parse_json(json_string, default=None):
    """Safely parse JSON with error handling."""
    if not json_string:
        return default
    
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        # Try to extract JSON if parsing fails
        json_pattern = r'\{[\s\S]*\}'
        match = re.search(json_pattern, json_string)
        if match:
            json_str = match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                logger.warning(f"Failed to extract valid JSON")
                return default
        else:
            logger.warning(f"No JSON found in response")
            return default

# Load environment variables from .env file
load_dotenv()

# Try to import the dump_environment module
try:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from dump_environment import create_environment_dump
    HAS_ENV_DUMP = True
except ImportError:
    HAS_ENV_DUMP = False

# Try to import optional dependencies
try:
    from flask import Blueprint, request, session, redirect, url_for, flash, render_template, g
    from flask_wtf import FlaskForm
    from wtforms import StringField, PasswordField, BooleanField, SubmitField
    from wtforms.validators import DataRequired, Email, Length
    from werkzeug.security import generate_password_hash, check_password_hash
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False

try:
    from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
    from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
    from jose import JWTError, jwt
    from passlib.context import CryptContext
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

# Color codes for terminal output
GREEN = '\033[0;32m'
BLUE = '\033[0;34m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color

# Logger is already set up at the beginning of the file

# AI integration support - dynamically imported if needed
HAS_ANTHROPIC = False
HAS_OPENAI = False
HAS_DEEPSEEK = False

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    import requests  # We use requests for DeepSeek API
    HAS_DEEPSEEK = True
except ImportError:
    HAS_DEEPSEEK = False

def print_banner():
    """Display the ASCII art banner."""
    print(f"{BLUE}")
    print("╔═══════════════════════════════════════════════╗")
    print("║           Python Project Initializer          ║")
    print("║           -------------------------           ║")
    print("║     Automated project structure creation      ║")
    print("╚═══════════════════════════════════════════════╝")
    print(f"{NC}")

def check_dependencies():
    """Check if required dependencies are installed."""
    print(f"{BLUE}Checking dependencies...{NC}")
    
    missing_deps = []
    
    # Check for python3
    if not shutil.which("python3"):
        missing_deps.append("python3")
    
    # Check for pip
    if not shutil.which("pip3"):
        missing_deps.append("pip3")
    
    # Check for git
    if not shutil.which("git"):
        missing_deps.append("git")
    
    # Check for code (VS Code)
    if not shutil.which("code"):
        print(f"{YELLOW}Warning: Visual Studio Code not found in PATH. You won't be able to automatically open projects in VS Code.{NC}")
    
    if missing_deps:
        print(f"{RED}The following dependencies are missing:{NC}")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nPlease install them before continuing.")
        sys.exit(1)
    
    print(f"{GREEN}All required dependencies are installed.{NC}")

def cli_entry(title, text, default=""):
    """CLI version of zenity entry dialog."""
    print(f"\n{BLUE}=== {title} ==={NC}")
    print(f"{text}")
    if default:
        print(f"(Default: {default})")
    try:
        result = input("> ").strip()
        # Use default if empty input
        if not result and default:
            return default
        return result
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)

def cli_file_selection(title, directory=True, filename=""):
    """CLI version of zenity file selection."""
    print(f"\n{BLUE}=== {title} ==={NC}")
    if directory:
        print("Enter directory path:")
    else:
        print("Enter file path:")
    
    try:
        result = input("> ").strip()
        # Expand user directory (~)
        result = os.path.expanduser(result)
        # Validate path
        if directory:
            if not os.path.isdir(result):
                print(f"{YELLOW}Warning: Directory does not exist or is not accessible.{NC}")
                while True:
                    choice = input("Create directory? (y/n) > ").strip().lower()
                    if choice == 'y':
                        os.makedirs(result, exist_ok=True)
                        break
                    elif choice == 'n':
                        print("Please enter a valid directory path.")
                        return cli_file_selection(title, directory, filename)
        return result
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)

def cli_text_info(title, text, editable=True, width=600, height=400):
    """CLI version of zenity text info dialog."""
    print(f"\n{BLUE}=== {title} ==={NC}")
    print(f"{text}")
    if editable:
        print("\nEnter text (end with Ctrl+D on a new line):")
        lines = []
        try:
            # Read multiple lines until EOF (Ctrl+D)
            while True:
                try:
                    line = input()
                    lines.append(line)
                except EOFError:
                    break
            return "\n".join(lines)
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            sys.exit(0)
    return ""

def cli_info(title, text, width=500, height=300):
    """CLI version of zenity info dialog."""
    print(f"\n{BLUE}=== {title} ==={NC}")
    print(f"{text}")
    input("Press Enter to continue...")

def cli_question(title, text, width=500):
    """CLI version of zenity question dialog."""
    print(f"\n{BLUE}=== {title} ==={NC}")
    print(f"{text}")
    try:
        while True:
            response = input("(y/n) > ").strip().lower()
            if response in ('y', 'yes'):
                return True
            elif response in ('n', 'no'):
                return False
            print("Please enter 'y' or 'n'")
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return False

def cli_list(title, text, columns, data, list_type="radiolist", width=700, height=500):
    """CLI version of zenity list dialog."""
    print(f"\n{BLUE}=== {title} ==={NC}")
    print(f"{text}")
    
    # For radiolist or checklist, data is formatted differently
    if list_type in ["radiolist", "checklist"]:
        options = []
        selected = []
        
        # Parse the data into options
        i = 0
        while i < len(data):
            is_selected = data[i] == "TRUE"
            option = data[i+1]
            options.append(option)
            if is_selected:
                selected.append(option)
            i += 2
        
        # Display options
        for i, option in enumerate(options):
            selected_marker = "*" if option in selected else " "
            print(f"{i+1}. [{selected_marker}] {option}")
        
        try:
            if list_type == "radiolist":
                # Single selection
                while True:
                    choice = input("Enter number (1-" + str(len(options)) + "): ").strip()
                    try:
                        idx = int(choice) - 1
                        if 0 <= idx < len(options):
                            return options[idx]
                        print(f"Please enter a number between 1 and {len(options)}")
                    except ValueError:
                        print("Please enter a valid number")
            else:
                # Multiple selection
                while True:
                    choice = input("Enter numbers separated by commas (1-" + str(len(options)) + "): ").strip()
                    try:
                        if not choice:  # Empty input
                            return ""
                            
                        indices = [int(x.strip()) - 1 for x in choice.split(",")]
                        if all(0 <= idx < len(options) for idx in indices):
                            return "|".join(options[idx] for idx in indices)
                        print(f"Please enter numbers between 1 and {len(options)}")
                    except ValueError:
                        print("Please enter valid numbers separated by commas")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return ""
    else:
        # Simple list
        for i, item in enumerate(data):
            print(f"{i+1}. {item}")
        
        try:
            while True:
                choice = input("Enter number: ").strip()
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(data):
                        return data[idx]
                    print(f"Please enter a number between 1 and {len(data)}")
                except ValueError:
                    print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return ""

def check_available_ai_models():
    """Check available AI models from supported providers."""
    available_models = {
        "anthropic": [],
        "openai": [],
        "deepseek": []
    }
    
    # Check Anthropic models
    if HAS_ANTHROPIC and os.environ.get("ANTHROPIC_API_KEY"):
        try:
            client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
            # Since Anthropic doesn't have a direct list_models endpoint, we'll hardcode current models
            available_models["anthropic"] = [
                {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus", "description": "Most powerful model for complex tasks"},
                {"id": "claude-3-sonnet-20240229", "name": "Claude 3 Sonnet", "description": "Balanced performance and cost"},
                {"id": "claude-3-haiku-20240307", "name": "Claude 3 Haiku", "description": "Fastest model, most cost-effective"}
            ]
        except Exception as e:
            logger.warning(f"Error checking Anthropic models: {e}")
    
    # Check OpenAI models
    if HAS_OPENAI and os.environ.get("OPENAI_API_KEY"):
        try:
            client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            response = client.models.list()
            gpt_models = [
                model for model in response.data
                if model.id.startswith(("gpt-3.5", "gpt-4")) and not model.id.endswith("vision")
            ]
            
            for model in gpt_models:
                description = ""
                if "gpt-4" in model.id:
                    description = "Powerful for complex reasoning"
                elif "gpt-3.5" in model.id:
                    description = "Fast and cost effective"
                
                available_models["openai"].append({
                    "id": model.id,
                    "name": model.id.replace("-turbo", " Turbo").upper(),
                    "description": description
                })
        except Exception as e:
            logger.warning(f"Error checking OpenAI models: {e}")
            # Fallback to known models
            available_models["openai"] = [
                {"id": "gpt-4", "name": "GPT-4", "description": "Most powerful model"},
                {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "description": "Fast and cost effective"}
            ]
    
    # DeepSeek doesn't have a list_models endpoint, so we'll hardcode the main model
    if HAS_DEEPSEEK and os.environ.get("DEEPSEEK_API_KEY"):
        available_models["deepseek"] = [
            {"id": "deepseek-chat", "name": "DeepSeek Chat", "description": "Base conversational model"}
        ]
    
    return available_models

class AIProvider:
    """AI provider wrapper class."""
    
    def __init__(self):
        """Initialize AI provider."""
        self.providers = []
        self.clients = {}
        
        # Initialize available providers
        self._init_anthropic()
        self._init_openai()
        self._init_deepseek()
    
    def _init_anthropic(self):
        """Initialize Anthropic provider."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            try:
                import anthropic
                self.clients["anthropic"] = anthropic.Anthropic(api_key=api_key)
                self.providers.append("anthropic")
            except ImportError:
                pass
    
    def _init_openai(self):
        """Initialize OpenAI provider."""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                import openai
                self.clients["openai"] = openai.OpenAI(api_key=api_key)
                self.providers.append("openai")
            except ImportError:
                pass
    
    def _init_deepseek(self):
        """Initialize DeepSeek provider."""
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if api_key:
            try:
                # DeepSeek doesn't have an official Python client, use requests instead
                import requests
                class DeepSeekClient:
                    def __init__(self, api_key):
                        self.api_key = api_key
                        self.api_url = "https://api.deepseek.com/v1/chat/completions"
                        
                    def completions_create(self, model, prompt):
                        headers = {
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {self.api_key}"
                        }
                        
                        payload = {
                            "model": model,
                            "messages": [
                                {"role": "user", "content": prompt}
                            ],
                            "temperature": 0.7,
                            "max_tokens": 1000
                        }
                        
                        response = requests.post(self.api_url, headers=headers, json=payload)
                        response.raise_for_status()  # Raise exception for HTTP errors
                        data = response.json()
                        
                        # Create a response object with a structure similar to other clients
                        class Response:
                            class Choice:
                                def __init__(self, text):
                                    self.text = text
                                    
                            def __init__(self, choices):
                                self.choices = [self.Choice(choice["message"]["content"]) 
                                               for choice in choices]
                                
                        return Response(data["choices"])
                
                self.clients["deepseek"] = DeepSeekClient(api_key=api_key)
                self.providers.append("deepseek")
            except ImportError:
                pass
    
    def ai_query(self, prompt: str, provider: Optional[str] = None, model: Optional[str] = None) -> str:
        """
        Send a query to the AI provider.
        
        Args:
            prompt: The prompt to send to the AI
            provider: Specific provider to use (optional)
            model: Specific model to use (optional)
            
        Returns:
            str: AI response
        """
        if not self.providers:
            raise ValueError("No AI providers available")
        
        # Use specified provider or first available
        provider = provider or self.providers[0]
        
        if provider not in self.providers:
            raise ValueError(f"Provider {provider} not available")
        
        # Default models if not specified
        default_models = {
            "anthropic": "claude-3-haiku-20240307",
            "openai": "gpt-3.5-turbo",
            "deepseek": "deepseek-chat"
        }
        
        # Use specified model or default for the provider
        model_to_use = model or default_models.get(provider, "")
        
        if provider == "anthropic":
            response = self.clients["anthropic"].messages.create(
                model=model_to_use,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
            
        elif provider == "openai":
            response = self.clients["openai"].chat.completions.create(
                model=model_to_use,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
            
        elif provider == "deepseek":
            response = self.clients["deepseek"].completions_create(
                model=model_to_use,
                prompt=prompt
            )
            return response.choices[0].text
        
        raise ValueError(f"Unknown provider: {provider}")

_instance = None

def get_ai_provider():
    """Get the AI provider instance."""
    global _instance
    if _instance is None:
        _instance = AIProvider()
    return _instance

def generate_ai_project_plan(description, provider=None, model=None):
    """
    Generate a comprehensive AI project plan based on user description.
    
    Args:
        description: Project description string
        provider: Specific AI provider to use
        model: Specific model to use
    
    Returns:
        dict: AI project plan with components and recommendations
    """
    ai_provider = get_ai_provider()
    if not ai_provider.providers:
        return None
    
    # Specific system message for DeepSeek to help ensure JSON output
    system_message = ""
    if provider == "deepseek":
        system_message = "You are a helpful assistant that always responds in valid JSON format when requested. Do not include any text outside the JSON."
    
    prompt = f"""Based on the user's project description, create a comprehensive plan.
    
    USER DESCRIPTION:
    {description}
    
    Provide your response ONLY in valid JSON format without any other text before or after:
    {{
        "summary": "1-2 sentence summary of the project",
        "components": ["list of 3-5 main components"],
        "technology_stack": {{
            "backend": ["list of backend technologies"],
            "frontend": ["list of frontend technologies if applicable"],
            "data": ["list of data technologies if applicable"],
            "deployment": ["list of deployment technologies"]
        }},
        "implementation_steps": ["list of 3-5 initial steps"],
        "challenges": ["list of 2-3 potential challenges"]
    }}
    """
    
    try:
        # Add system message for DeepSeek
        if provider == "deepseek":
            # For DeepSeek we prepend the system message to the prompt
            full_prompt = f"{system_message}\n\n{prompt}"
            response = ai_provider.ai_query(full_prompt, provider, model)
        else:
            response = ai_provider.ai_query(prompt, provider, model)
        
        return safely_parse_json(response, default=None)
    except Exception as e:
        logger.warning(f"Failed to generate AI project plan: {e}")
        raise

def analyze_project_description(description):
    """
    Analyze project description to determine project type and requirements.
    
    Args:
        description: Project description string
    
    Returns:
        dict: Analysis results containing project types and features
    """
    keywords = {
        "web": ["web", "flask", "fastapi", "django", "http", "api", "rest"],
        "cli": ["cli", "command", "terminal", "console", "script"],
        "automation": ["automation", "automate", "schedule", "cron", "batch"],
        "ai": ["ai", "ml", "machine learning", "neural", "deep learning"],
        "data": ["data", "analysis", "pandas", "numpy", "statistics"],
    }
    
    detected_types = []
    for type_name, type_keywords in keywords.items():
        if any(keyword in description.lower() for keyword in type_keywords):
            detected_types.append(type_name)
    
    return {
        "project_types": detected_types or ["cli"],  # Default to CLI if no type detected
        "needs_ai": any(ai_term in description.lower() for ai_term in ["ai", "ml", "intelligent"]),
        "needs_web": any(web_term in description.lower() for web_term in ["web", "http", "api"]),
        "needs_security": any(sec_term in description.lower() for sec_term in ["secure", "auth", "login"])
    }

def get_ai_recommendations(description, provider=None, model=None):
    """
    Get AI-powered recommendations for project setup.
    
    Args:
        description: Project description string
        provider: Specific AI provider to use
        model: Specific model to use
    
    Returns:
        dict: AI recommendations for project setup
    """
    ai_provider = get_ai_provider()
    if not ai_provider.providers:
        return {}
    
    # Specific system message for DeepSeek to help ensure JSON output
    system_message = ""
    if provider == "deepseek":
        system_message = "You are a helpful assistant that always responds in valid JSON format when requested. Do not include any text outside the JSON."
    
    prompt = f"""The user has described their desired project outcome below. They may not be technical, so translate their needs into appropriate technical recommendations:

    USER DESCRIPTION:
    {description}
    
    First, identify what type of application would best serve these outcomes. Then recommend the appropriate setup.
    
    Provide your response ONLY in valid JSON format without any other text before or after:
    {{
        "user_friendly_summary": "Brief explanation of your recommendation in non-technical terms",
        "project_type": "main project type",
        "additional_types": ["other relevant types"],
        "suggested_dependencies": ["key packages needed"],
        "suggested_tools": ["recommended development tools"],
        "security_considerations": ["security features needed"]
    }}
    """
    
    try:
        # Add system message for DeepSeek
        if provider == "deepseek":
            # For DeepSeek we prepend the system message to the prompt
            full_prompt = f"{system_message}\n\n{prompt}"
            response = ai_provider.ai_query(full_prompt, provider, model)
        else:
            response = ai_provider.ai_query(prompt, provider, model)
        
        return safely_parse_json(response, default={})
    except Exception as e:
        logger.warning(f"Failed to get AI recommendations: {e}")
        raise

def select_dependencies_for_type(project_types):
    """
    Select appropriate dependencies based on project type.
    
    Args:
        project_types: List of project types
    
    Returns:
        list: Required dependencies
    """
    dependencies = ["python-dotenv"]  # Base dependencies
    
    type_deps = {
        "web": ["flask", "flask-login", "flask-wtf"],
        "cli": ["click", "rich"],
        "automation": ["schedule", "requests"],
        "ai": ["pandas", "scikit-learn"],
        "data": ["pandas", "numpy", "matplotlib"]
    }
    
    for project_type in project_types:
        if project_type in type_deps:
            dependencies.extend(type_deps[project_type])
    
    return list(set(dependencies))  # Remove duplicates

def get_available_models():
    """
    Get available models for each provider.
    
    Returns:
        dict: Dictionary of provider models
    """
    models = {
        "anthropic": [],
        "openai": [],
        "deepseek": []
    }
    
    # Check Anthropic models
    if HAS_ANTHROPIC and os.environ.get("ANTHROPIC_API_KEY"):
        models["anthropic"] = [
            {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus", "description": "Most powerful model for complex tasks"},
            {"id": "claude-3-sonnet-20240229", "name": "Claude 3 Sonnet", "description": "Balanced performance and cost"},
            {"id": "claude-3-haiku-20240307", "name": "Claude 3 Haiku", "description": "Fastest model, most cost-effective"}
        ]
    
    # Check OpenAI models
    if HAS_OPENAI and os.environ.get("OPENAI_API_KEY"):
        try:
            import openai
            client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            model_list = client.models.list()
            
            for model in model_list.data:
                if model.id.startswith(("gpt-3.5", "gpt-4")) and not model.id.endswith("vision"):
                    description = ""
                    if "gpt-4" in model.id:
                        description = "Powerful for complex reasoning"
                    elif "gpt-3.5" in model.id:
                        description = "Fast and cost effective"
                    
                    models["openai"].append({
                        "id": model.id,
                        "name": model.id.replace("-turbo", " Turbo").upper(),
                        "description": description
                    })
        except Exception as e:
            logger.warning(f"Error fetching OpenAI models: {e}")
            # Fallback to known models
            models["openai"] = [
                {"id": "gpt-4o", "name": "GPT-4o", "description": "Latest version, powerful with reduced cost"},
                {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "description": "Powerful for complex reasoning"},
                {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "description": "Fast and cost effective"}
            ]
    
    # DeepSeek models
    if HAS_DEEPSEEK and os.environ.get("DEEPSEEK_API_KEY"):
        models["deepseek"] = [
            {"id": "deepseek-chat", "name": "DeepSeek Chat", "description": "Base conversational model"},
            {"id": "deepseek-coder", "name": "DeepSeek Coder", "description": "Specialized for code generation"}
        ]
    
    return models

def select_ai_provider():
    """
    Allow the user to select which AI provider to use.
    
    Returns:
        tuple: (provider_id, model_id) or (None, None)
    """
    available_models = get_available_models()
    available_providers = []
    
    # Build list of available providers
    if available_models["anthropic"]:
        available_providers.append("anthropic")
    
    if available_models["openai"]:
        available_providers.append("openai")
    
    if available_models["deepseek"]:
        available_providers.append("deepseek")
    
    if not available_providers:
        print(f"{YELLOW}No AI providers available. Please install at least one of the following:{NC}")
        print("- pip install anthropic")
        print("- pip install openai")
        print("- pip install deepseek")
        print(f"\n{YELLOW}And set your API key in the .env file:{NC}")
        print("ANTHROPIC_API_KEY=your_api_key")
        print("OPENAI_API_KEY=your_api_key")
        print("DEEPSEEK_API_KEY=your_api_key")
        
        proceed = cli_question(
            "Continue without AI",
            "Do you want to continue without AI assistance?"
        )
        return (None, None) if proceed else sys.exit(1)
    
    # Display available providers
    print(f"{BLUE}Available AI Providers:{NC}")
    for i, provider in enumerate(available_providers, 1):
        provider_name = {
            "anthropic": "Claude (Anthropic)",
            "openai": "GPT (OpenAI)",
            "deepseek": "DeepSeek"
        }.get(provider, provider)
        
        # Show available models for this provider
        if available_models[provider]:
            default_model = available_models[provider][0]["id"]
            print(f"{i}. {provider_name} - Default: {default_model}")
        else:
            print(f"{i}. {provider_name}")
            
    print(f"{len(available_providers) + 1}. Proceed without AI")
    
    # Get provider selection
    provider_idx = None
    while provider_idx is None:
        try:
            choice = input(f"Select AI provider (1-{len(available_providers) + 1}): ").strip()
            idx = int(choice) - 1
            
            if 0 <= idx < len(available_providers):
                provider_idx = idx
            elif idx == len(available_providers):
                return (None, None)  # Proceed without AI
            else:
                print(f"Please enter a number between 1 and {len(available_providers) + 1}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            sys.exit(0)
    
    selected_provider = available_providers[provider_idx]
    
    # If only one model available, use it
    if len(available_models[selected_provider]) == 1:
        return (selected_provider, available_models[selected_provider][0]["id"])
    
    # Display model options for selected provider
    print(f"\n{BLUE}Available Models for {selected_provider.title()}:{NC}")
    for i, model in enumerate(available_models[selected_provider], 1):
        print(f"{i}. {model['name']} - {model['id']}")
        if model['description']:
            print(f"   {model['description']}")
    
    # Get model selection
    while True:
        try:
            choice = input(f"Select model (1-{len(available_models[selected_provider])}): ").strip()
            idx = int(choice) - 1
            
            if 0 <= idx < len(available_models[selected_provider]):
                return (selected_provider, available_models[selected_provider][idx]["id"])
            else:
                print(f"Please enter a number between 1 and {len(available_models[selected_provider])}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            sys.exit(0)

def get_project_info():
    """
    Collect project information through interactive dialogs with improved AI prompting.
    
    Returns:
        dict: Project configuration information
    """
    print(f"{BLUE}Collecting project information...{NC}")
    
    # First, let the user select an AI provider and model
    provider_tuple = select_ai_provider()
    selected_provider, selected_model = provider_tuple
    
    project_info = {
        "selected_ai_provider": selected_provider,
        "selected_ai_model": selected_model
    }
    
    if selected_provider:
        print(f"{GREEN}Using {selected_provider.title()} with model {selected_model}{NC}")
    
    current_step = "project_name"
    steps = ["project_name", "project_dir", "description", "project_types", "custom_keywords", "domain_questions", "python_version"]
    
    while current_step:
        print(f"\n{YELLOW}[Step {steps.index(current_step)+1}/{len(steps)}] {current_step.replace('_', ' ').title()}{NC}")
        print(f"{YELLOW}Type 'back' to go to previous step, 'restart' to start over, or 'exit' to quit.{NC}")
        
        if current_step == "project_name":
            response = cli_entry(
                "Project Name",
                "Enter the name of your Python project:",
                "my_project"
            )
            
            if response.lower() == "exit":
                print(f"{RED}Exiting project creation.{NC}")
                sys.exit(0)
            elif response.lower() == "restart":
                current_step = "project_name"
                project_info = {}
                continue
            elif response.lower() == "back":
                print(f"{YELLOW}Already at first step.{NC}")
                continue
            else:
                project_info["project_name"] = response
                current_step = "project_dir"
        
        elif current_step == "project_dir":
            response = cli_file_selection(
                "Project Location",
                directory=True
            )
            
            if response.lower() == "exit":
                print(f"{RED}Exiting project creation.{NC}")
                sys.exit(0)
            elif response.lower() == "restart":
                current_step = "project_name"
                project_info = {}
                continue
            elif response.lower() == "back":
                current_step = "project_name"
                continue
            else:
                project_info["project_dir"] = response
                current_step = "description"
        
        elif current_step == "description":
            response = cli_text_info(
                "Project Outcomes",
                "Describe what you want your project to accomplish:\n\n" +
                "• What problem does it solve?\n" +
                "• Who will use it?\n" +
                "• How will they interact with it?\n\n" +
                "Focus on outcomes rather than technologies.",
                editable=True
            )
            
            if response.lower() == "exit":
                print(f"{RED}Exiting project creation.{NC}")
                sys.exit(0)
            elif response.lower() == "restart":
                current_step = "project_name"
                project_info = {}
                continue
            elif response.lower() == "back":
                current_step = "project_dir"
                continue
            else:
                project_info["description"] = response
                
                # Generate AI project plan if provider selected
                selected_provider = project_info.get("selected_ai_provider")
                selected_model = project_info.get("selected_ai_model")
                
                if selected_provider:
                    print(f"{BLUE}Analyzing your project description with {selected_provider.title()} ({selected_model})...{NC}")
                    try:
                        project_plan = generate_ai_project_plan(response, selected_provider, selected_model)
                        
                        if project_plan:
                            print(f"\n{GREEN}AI Project Analysis:{NC}")
                            print(f"• Summary: {project_plan['summary']}")
                            print(f"• Main Components: {', '.join(project_plan['components'])}")
                            print(f"• Backend: {', '.join(project_plan['technology_stack']['backend'])}")
                            if project_plan['technology_stack']['frontend']:
                                print(f"• Frontend: {', '.join(project_plan['technology_stack']['frontend'])}")
                            print(f"• Next Steps: {project_plan['implementation_steps'][0]}")
                            
                            # Ask for confirmation
                            confirm = cli_question(
                                "Confirm Analysis",
                                "Does this analysis match your project goals? (Press 'n' to provide more details)"
                            )
                            
                            if not confirm:
                                print(f"{YELLOW}Please provide more details about your project.{NC}")
                                continue
                    except Exception as e:
                        print(f"{RED}Error using {selected_provider} with model {selected_model} for analysis: {e}{NC}")
                        retry = cli_question(
                            "AI Analysis Failed",
                            "Would you like to try with a different AI provider?"
                        )
                        if retry:
                            provider_tuple = select_ai_provider()
                            new_provider, new_model = provider_tuple
                            if new_provider:
                                project_info["selected_ai_provider"] = new_provider
                                project_info["selected_ai_model"] = new_model
                                continue
                        project_plan = None
                else:
                    print(f"{YELLOW}Proceeding without AI project plan analysis.{NC}")
                    project_plan = None
                
                # Analyze description for project types
                analysis = analyze_project_description(response)
                project_info["analysis"] = analysis
                project_info["project_plan"] = project_plan
                
                # Get AI recommendations if provider selected
                if selected_provider:
                    try:
                        ai_recommendations = get_ai_recommendations(response, selected_provider, selected_model)
                    except Exception as e:
                        print(f"{RED}Error getting AI recommendations: {e}{NC}")
                        ai_recommendations = {}
                else:
                    ai_recommendations = {}
                project_info["ai_recommendations"] = ai_recommendations
                
                current_step = "project_types"
                
        elif current_step == "project_types":
            # Get available AI models
            ai_models = check_available_ai_models()
            
            # Select project type(s)
            suggested_types = project_info["analysis"]["project_types"] if "analysis" in project_info else []
            all_types = ["cli", "web", "automation", "ai", "data"]
            
            # User-friendly descriptions of project types
            type_descriptions = {
                "cli": "Command-line tool (runs in terminal, no graphical interface)",
                "web": "Web application (accessed through a browser)",
                "automation": "Background service (runs automatically, minimal user interaction)",
                "ai": "AI/Machine Learning application (learns from data)",
                "data": "Data processing application (analyzes or transforms information)"
            }
            
            print("\nSelect applicable project types:")
            for type_code in all_types:
                is_suggested = type_code in suggested_types
                suggestion_marker = "*" if is_suggested else " "
                print(f"  [{suggestion_marker}] {type_code}: {type_descriptions[type_code]}")
            
            type_data = []
            for t in all_types:
                # Format as "TYPE: Description" for better user understanding
                display_name = f"{t}: {type_descriptions[t]}"
                type_data.extend(["TRUE" if t in suggested_types else "FALSE", display_name])
            
            selected_types_str = cli_list(
                "Project Types",
                "Select project type(s):",
                ["Select", "Type"],
                type_data,
                "checklist"
            )
            
            if selected_types_str.lower() == "exit":
                print(f"{RED}Exiting project creation.{NC}")
                sys.exit(0)
            elif selected_types_str.lower() == "restart":
                current_step = "project_name"
                project_info = {}
                continue
            elif selected_types_str.lower() == "back":
                current_step = "description"
                continue
            else:
                # Extract the base type from the display string (e.g., "cli: Command-line tool" -> "cli")
                selected_types = []
                if selected_types_str:
                    for type_with_desc in selected_types_str.split("|"):
                        base_type = type_with_desc.split(":", 1)[0].strip()
                        selected_types.append(base_type)
                
                project_info["project_types"] = selected_types
                current_step = "custom_keywords"
                
        elif current_step == "custom_keywords":
            # New step for collecting custom keywords
            response = cli_entry(
                "Custom Technology Keywords",
                "Enter comma-separated technology keywords that are central to your project:\n" +
                "(Examples: postgres, oauth, machine-learning, slack, gmail, etc.)",
                ""
            )
            
            if response.lower() == "exit":
                print(f"{RED}Exiting project creation.{NC}")
                sys.exit(0)
            elif response.lower() == "restart":
                current_step = "project_name"
                project_info = {}
                continue
            elif response.lower() == "back":
                current_step = "project_types"
                continue
            else:
                # Store a list of custom keywords
                project_info["custom_keywords"] = [k.strip() for k in response.split(',') if k.strip()]
                
                # Only proceed to domain questions if we have an AI provider and keywords
                if selected_provider and project_info["custom_keywords"]:
                    current_step = "domain_questions"
                else:
                    current_step = "python_version"
        
        elif current_step == "domain_questions":
            # New step for domain-specific questions
            ai_provider = get_ai_provider()
            
            print(f"{BLUE}Generating domain-specific questions based on your keywords...{NC}")
            
            # Try Do the same for the get_refined_recommendations import:multiple import paths for generate_domain_questions
            try:
                # Try local import first (when running as a package)
                from create_python_project.utils.ai_prompts import generate_domain_questions
            except ImportError:
                try:
                    # Try relative import (when running from within the directory)
                    from utils.ai_prompts import generate_domain_questions
                except ImportError:
                    # Fallback function if module isn't available
                    def generate_domain_questions(description, keywords, ai_provider, provider=None, model=None):
                        """Fallback function if ai_prompts module not available."""
                        print(f"{YELLOW}Warning: ai_prompts module not found. Using simplified question generation.{NC}")
                        # Generate simple questions based on keywords
                        questions = {}
                        for i, keyword in enumerate(keywords[:3], 1):
                            questions[f"q{i}"] = f"What specific requirements do you have for {keyword}?"
                        return questions
            
            domain_questions = generate_domain_questions(
                project_info["description"],
                project_info["custom_keywords"],
                ai_provider,
                selected_provider,
                selected_model
            )
            
            if domain_questions:
                # Ask domain-specific questions (limited to 5)
                domain_answers = {}
                question_count = 0
                
                for question_id, question_text in domain_questions.items():
                    if question_count >= 5:
                        break
                        
                    response = cli_entry(
                        f"Domain Question: {question_id}",
                        question_text
                    )
                    
                    if response.lower() == "exit":
                        print(f"{RED}Exiting project creation.{NC}")
                        sys.exit(0)
                    elif response.lower() == "restart":
                        current_step = "project_name"
                        project_info = {}
                        break
                    elif response.lower() == "back":
                        if question_count == 0:
                            current_step = "custom_keywords"
                            break
                        else:
                            # If we've already answered some questions, just continue
                            # with the next one - we don't want to lose progress
                            continue
                    else:
                        domain_answers[question_id] = response
                        question_count += 1
                
                # Store domain answers if we didn't break the loop due to restart/back
                if current_step == "domain_questions":
                    project_info["domain_answers"] = domain_answers
                    
                    # After domain questions, get refined recommendations
                    print(f"{BLUE}Getting refined project recommendations...{NC}")
                    
                    # Try multiple import paths for get_refined_recommendations
                    try:
                        # Try local import first (when running as a package)
                        from create_python_project.utils.ai_prompts import get_refined_recommendations
                    except ImportError:
                        try:
                            # Try relative import (when running from within the directory)
                            from utils.ai_prompts import get_refined_recommendations
                        except ImportError:
                            # Fallback function if module isn't available
                            def get_refined_recommendations(project_info, ai_provider, provider=None, model=None):
                                """Fallback function if ai_prompts module isn't available."""
                                print(f"{YELLOW}Warning: ai_prompts module not found. Using simplified recommendations.{NC}")
                                return {}
                    
                    refined_recommendations = get_refined_recommendations(
                        project_info,
                        ai_provider,
                        selected_provider,
                        selected_model
                    )
                    
                    if refined_recommendations:
                        project_info["refined_recommendations"] = refined_recommendations
                        
                        # Show dependency recommendations
                        if "suggested_dependencies" in refined_recommendations:
                            print(f"\n{GREEN}Recommended Dependencies:{NC}")
                            for dep in refined_recommendations["suggested_dependencies"]:
                                if isinstance(dep, dict) and "name" in dep and "description" in dep:
                                    print(f"• {dep['name']} - {dep['description']}")
                                elif isinstance(dep, str):
                                    print(f"• {dep}")
                    
                    current_step = "python_version"
            else:
                # If no questions were generated, skip to next step
                current_step = "python_version"
                
        elif current_step == "python_version":
            # Get Python version
            python_version = cli_list(
                "Python Version",
                "Select Python version:",
                ["Version"],
                ["3.12", "3.11", "3.10", "3.9"],
                "radiolist"
            )
            
            if python_version.lower() == "exit":
                print(f"{RED}Exiting project creation.{NC}")
                sys.exit(0)
            elif python_version.lower() == "restart":
                current_step = "project_name"
                project_info = {}
                continue
            elif python_version.lower() == "back":
                current_step = "domain_questions" if "domain_answers" in project_info else "custom_keywords"
                continue
            else:
                project_info["python_version"] = python_version or "3.12"
                project_info["main_module"] = project_info["project_name"].replace("-", "_").lower()
                
                # Use refined_recommendations for dependencies if available
                if "refined_recommendations" in project_info and "suggested_dependencies" in project_info["refined_recommendations"]:
                    refined_deps = project_info["refined_recommendations"]["suggested_dependencies"]
                    # Extract just the package names from the recommendations
                    additional_deps = []
                    for dep in refined_deps:
                        if isinstance(dep, dict) and "name" in dep:
                            additional_deps.append(dep["name"])
                        elif isinstance(dep, str):
                            additional_deps.append(dep)
                            
                    # Combine with auto-selected dependencies
                    auto_deps = select_dependencies_for_type(project_info["project_types"])
                    project_info["dependencies"] = list(set(auto_deps + additional_deps))
                else:
                    # Just use the auto-selected dependencies
                    project_info["dependencies"] = select_dependencies_for_type(project_info["project_types"])
                
                # Get available AI models
                ai_models = check_available_ai_models()
                project_info["ai_providers"] = [p for p in ["anthropic", "openai", "deepseek"] if ai_models[p]]
                project_info["ai_models"] = {p: models[0]["id"] for p, models in ai_models.items() if models}
                
                # Set security features
                project_info["security_features"] = project_info["analysis"]["needs_security"]
                
                # Set creation date
                project_info["creation_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Show summary and confirm
                print(f"\n{GREEN}Project Summary:{NC}")
                print(f"• Project Name: {project_info['project_name']}")
                print(f"• Location: {project_info['project_dir']}")
                print(f"• Types: {', '.join(project_info['project_types'])}")
                print(f"• Python: {project_info['python_version']}")
                print(f"• Dependencies: {', '.join(project_info['dependencies'][:5])}{'...' if len(project_info['dependencies']) > 5 else ''}")
                
                confirm = cli_question(
                    "Create Project",
                    "Do you want to create this project?"
                )
                
                if not confirm:
                    print(f"{YELLOW}Project creation cancelled.{NC}")
                    sys.exit(0)
                
                current_step = None
    
    return project_info

def create_project_structure(project_info):
    """Create the project structure."""
    project_name = project_info["project_name"]
    project_dir = project_info["project_dir"]
    main_module = project_info["main_module"]
    
    # Set full project path
    full_project_path = os.path.join(project_dir, project_name)
    
    print(f"{BLUE}Creating project structure at {full_project_path}...{NC}")
    
    # Create base directories
    os.makedirs(full_project_path, exist_ok=True)
    os.makedirs(os.path.join(full_project_path, main_module), exist_ok=True)
    os.makedirs(os.path.join(full_project_path, "tests"), exist_ok=True)
    os.makedirs(os.path.join(full_project_path, "docs"), exist_ok=True)
    
    # Create __init__.py files
    with open(os.path.join(full_project_path, main_module, "__init__.py"), "w") as f:
        f.write(f'''"""
{project_name} package.

{project_info["description"]}
"""

__version__ = "0.1.0"
''')
    
    with open(os.path.join(full_project_path, "tests", "__init__.py"), "w") as f:
        f.write('"""Test package."""\n')
    
    # Create utils directory if needed
    if "web" in project_info["project_types"] or "automation" in project_info["project_types"]:
        os.makedirs(os.path.join(full_project_path, main_module, "utils"), exist_ok=True)
        with open(os.path.join(full_project_path, main_module, "utils", "__init__.py"), "w") as f:
            f.write('"""Utility modules."""\n')
    
    # Create templates directory if web project
    if "web" in project_info["project_types"]:
        os.makedirs(os.path.join(full_project_path, main_module, "templates"), exist_ok=True)
        os.makedirs(os.path.join(full_project_path, main_module, "static"), exist_ok=True)
        os.makedirs(os.path.join(full_project_path, main_module, "static", "css"), exist_ok=True)
        os.makedirs(os.path.join(full_project_path, main_module, "static", "js"), exist_ok=True)
    
    print(f"{GREEN}Created directory structure{NC}")
    
    return full_project_path

def create_project_files(project_info, full_project_path):
    """Create project files."""
    project_name = project_info["project_name"]
    main_module = project_info["main_module"]
    python_version = project_info["python_version"]
    dependencies = project_info["dependencies"]
    project_description = project_info["description"]
    
    print(f"{BLUE}Creating project files...{NC}")
    
    # Create requirements.txt
    with open(os.path.join(full_project_path, "requirements.txt"), "w") as f:
        for dep in sorted(dependencies):
            f.write(f"{dep}\n")
    
    # Create requirements-dev.txt
    with open(os.path.join(full_project_path, "requirements-dev.txt"), "w") as f:
        f.write('''# Development dependencies
pytest>=7.0.0
pytest-cov>=4.0.0
black>=23.0.0
pylint>=2.15.0
pre-commit>=3.3.0
isort>=5.12.0
''')
    
    # Create setup.py
    setup_py_content = f'''#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="{project_name}",
    version="0.1.0",
    description="{project_description.split('.')[0] if '.' in project_description else project_description}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="YourName",
    author_email="your.email@example.com",
    url=f"https://github.com/yourusername/{project_name}",
    packages=find_packages(),
    python_requires=">={python_version}",
    install_requires={dependencies},
    entry_points={{
        'console_scripts': [
            f'{project_name}={main_module}.main:main',
        ],
    }},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        f"Programming Language :: Python :: {python_version}",
        "Operating System :: OS Independent",
    ],
)
'''
    
    with open(os.path.join(full_project_path, "setup.py"), "w") as f:
        f.write(setup_py_content)
    
    # Create README.md
    readme_content = f'''# {project_name.replace('_', ' ').title()}

{project_description}

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/{project_name}.git
cd {project_name}

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

## Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linting
pylint {main_module}

# Format code
black {main_module} tests
```

## License

MIT
'''
    
    with open(os.path.join(full_project_path, "README.md"), "w") as f:
        f.write(readme_content)
    
    # Create .gitignore
    gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Testing
.coverage
.pytest_cache/
htmlcov/

# Logs
*.log
'''
    
    with open(os.path.join(full_project_path, ".gitignore"), "w") as f:
        f.write(gitignore_content)
    
    print(f"{GREEN}Created project files{NC}")

def create_ai_provider_module(project_info, full_project_path):
    """Create AI provider module for projects using AI integration."""
    main_module = project_info["main_module"]
    ai_providers = project_info["ai_providers"]
    ai_models = project_info["ai_models"]
    
    print(f"{BLUE}Creating AI provider module...{NC}")
    
    utils_dir = os.path.join(full_project_path, main_module, "utils")
    os.makedirs(utils_dir, exist_ok=True)
    
    ai_provider_content = f'''"""AI provider integration module."""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIProvider:
    """AI provider wrapper class."""
    
    def __init__(self):
        """Initialize AI provider."""
        self.providers = []
        self.clients = {{}}
        
        # Initialize available providers
        self._init_anthropic()
        self._init_openai()
        self._init_deepseek()
    
    def _init_anthropic(self):
        """Initialize Anthropic provider."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            try:
                import anthropic
                self.clients["anthropic"] = anthropic.Anthropic(api_key=api_key)
                self.providers.append("anthropic")
            except ImportError:
                pass
    
    def _init_openai(self):
        """Initialize OpenAI provider."""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                import openai
                self.clients["openai"] = openai.OpenAI(api_key=api_key)
                self.providers.append("openai")
            except ImportError:
                pass
    
    def _init_deepseek(self):
        """Initialize DeepSeek provider."""
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if api_key:
            try:
                # DeepSeek doesn't have an official Python client, use requests instead
                import requests
                class DeepSeekClient:
                    def __init__(self, api_key):
                        self.api_key = api_key
                        self.api_url = "https://api.deepseek.com/v1/chat/completions"
                        
                    def completions_create(self, model, prompt):
                        headers = {
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {self.api_key}"
                        }
                        
                        payload = {
                            "model": model,
                            "messages": [
                                {"role": "user", "content": prompt}
                            ],
                            "temperature": 0.7,
                            "max_tokens": 1000
                        }
                        
                        response = requests.post(self.api_url, headers=headers, json=payload)
                        response.raise_for_status()  # Raise exception for HTTP errors
                        data = response.json()
                        
                        # Create a response object with a structure similar to other clients
                        class Response:
                            class Choice:
                                def __init__(self, text):
                                    self.text = text
                                    
                            def __init__(self, choices):
                                self.choices = [self.Choice(choice["message"]["content"]) 
                                               for choice in choices]
                                
                        return Response(data["choices"])
                
                self.clients["deepseek"] = DeepSeekClient(api_key=api_key)
                self.providers.append("deepseek")
            except ImportError:
                pass
    
    def ai_query(self, prompt: str, provider: Optional[str] = None) -> str:
        """
        Send a query to the AI provider.
        
        Args:
            prompt: The prompt to send to the AI
            provider: Specific provider to use (optional)
            
        Returns:
            str: AI response
        """
        if not self.providers:
            raise ValueError("No AI providers available")
        
        # Use specified provider or first available
        provider = provider or self.providers[0]
        
        if provider not in self.providers:
            raise ValueError(f"Provider {{provider}} not available")
        
        if provider == "anthropic":
            response = self.clients["anthropic"].messages.create(
                model="{ai_models.get('anthropic', 'claude-3-haiku-20240307')}",
                max_tokens=1000,
                messages=[
                    {{"role": "user", "content": prompt}}
                ]
            )
            return response.content[0].text
            
        elif provider == "openai":
            response = self.clients["openai"].chat.completions.create(
                model="{ai_models.get('openai', 'gpt-3.5-turbo')}",
                messages=[
                    {{"role": "system", "content": "You are a helpful AI assistant."}},
                    {{"role": "user", "content": prompt}}
                ]
            )
            return response.choices[0].message.content
            
        elif provider == "deepseek":
            response = self.clients["deepseek"].completions.create(
                model="{ai_models.get('deepseek', 'deepseek-chat')}",
                prompt=prompt
            )
            return response.choices[0].text
        
        raise ValueError(f"Unknown provider: {{provider}}")

_instance = None

def get_ai_provider():
    """Get the AI provider instance."""
    global _instance
    if _instance is None:
        _instance = AIProvider()
    return _instance

def analyze_project_description(description):
    """
    Analyze project description to determine project type and requirements.
    
    Args:
        description: Project description string
    
    Returns:
        dict: Analysis results containing project types and features
    """
    keywords = {{
        "web": ["web", "flask", "fastapi", "django", "http", "api", "rest"],
        "cli": ["cli", "command", "terminal", "console", "script"],
        "automation": ["automation", "automate", "schedule", "cron", "batch"],
        "ai": ["ai", "ml", "machine learning", "neural", "deep learning"],
        "data": ["data", "analysis", "pandas", "numpy", "statistics"],
    }}
    
    detected_types = []
    for type_name, type_keywords in keywords.items():
        if any(keyword in description.lower() for keyword in type_keywords):
            detected_types.append(type_name)
    
    return {{
        "project_types": detected_types or ["cli"],  # Default to CLI if no type detected
        "needs_ai": any(ai_term in description.lower() for ai_term in ["ai", "ml", "intelligent"]),
        "needs_web": any(web_term in description.lower() for web_term in ["web", "http", "api"]),
        "needs_security": any(sec_term in description.lower() for sec_term in ["secure", "auth", "login"])
    }}
'''
    
    with open(os.path.join(utils_dir, "ai_provider.py"), "w") as f:
        f.write(ai_provider_content)
    
    print(f"{GREEN}Created AI provider module{NC}")

def create_docker_files(project_info, full_project_path):
    """Create Docker files."""
    project_name = project_info["project_name"]
    main_module = project_info["main_module"]
    python_version = project_info["python_version"]
    project_types = project_info["project_types"]
    
    print(f"{BLUE}Creating Docker files...{NC}")
    
    # Create Dockerfile
    dockerfile_content = f'''FROM python:{python_version}-slim
WORKDIR /app
# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the application
COPY . .
# Install the package
RUN pip install -e .
# Command to run the application
CMD ["python", "-m", "{main_module}"]
'''
    
    with open(os.path.join(full_project_path, "Dockerfile"), "w") as f:
        f.write(dockerfile_content)
    
    # Create docker-compose.yml
    docker_compose_content = '''version: '3'
services:
'''
    docker_compose_content += f'''  app:
    build: .
    volumes:
      - .:/app
      - ./.env:/app/.env
'''
    
    # Add web-specific configurations
    if "web" in project_types:
        docker_compose_content += f'''    ports:
      - "5000:5000"
    environment:
      - PORT=5000
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_DB={project_name}
    ports:
      - "5432:5432"
volumes:
  postgres_data:
'''
    
    with open(os.path.join(full_project_path, "docker-compose.yml"), "w") as f:
        f.write(docker_compose_content)
    
    # Create .dockerignore
    dockerignore_content = '''.venv/
.git/
.vscode/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/
.hypothesis/
.egg-info/
.eggs/
*.egg
dist/
build/
'''
    
    with open(os.path.join(full_project_path, ".dockerignore"), "w") as f:  # Fixed syntax error here
        f.write(dockerignore_content)
    
    print(f"{GREEN}Created Docker files{NC}")

def create_security_modules(project_info, full_project_path):
    """Create security-related modules for web applications."""
    main_module = project_info["main_module"]
    security_features = project_info["security_features"]
    
    print(f"{BLUE}Creating security modules...{NC}")
    
    # Determine if we're using Flask or FastAPI
    is_flask = "flask" in [dep.lower() for dep in project_info["dependencies"]]
    
    if is_flask:
        # Create auth.py module for Flask
        flask_auth_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Authentication module."""

import os
import functools
from flask import Blueprint, request, session, redirect, url_for, flash, render_template, g
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

bp = Blueprint('auth', __name__, url_prefix='/auth')

def init_auth(app):
    """Initialize authentication."""
    app.register_blueprint(bp)
    app.before_request(load_logged_in_user)

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

def load_logged_in_user():
    """Load logged in user if session exists."""
    user_id = session.get('user_id')
    g.user = User.get(user_id) if user_id else None

class User:
    """User model."""
    
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash
    
    @staticmethod
    def get(user_id):
        """Get user by ID."""
        # Replace with actual database lookup
        if user_id == 1:
            return User(1, 'admin', generate_password_hash('admin'))
        return None
    
    @staticmethod
    def authenticate(username, password):
        """Authenticate a user."""
        # Replace with actual authentication
        if username == 'admin' and password == 'admin':
            return User(1, username, generate_password_hash(password))
        return None

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Handle login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        
        user = User.authenticate(username, password)
        
        if user is None:
            error = 'Invalid username or password.'
        
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))
        
        flash(error)
    
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    """Handle logout."""
    session.clear()
    return redirect(url_for('index'))
'''
        
        with open(os.path.join(full_project_path, main_module, "auth.py"), "w") as f:
            f.write(flask_auth_content)
    else:
        # Create auth.py module for FastAPI
        fastapi_auth_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Authentication module."""

import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    """Token model."""
    access_token: str
    token_type: str

class User(BaseModel):
    """User model."""
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    """User in database."""
    hashed_password: str

def verify_password(plain_password, hashed_password):
    """Verify password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Get password hash."""
    return pwd_context.hash(password)

def get_user(username: str):
    """Get user from database."""
    # Replace with actual database lookup
    if username == "admin":
        return UserInDB(
            username=username,
            email="admin@example.com",
            hashed_password=get_password_hash("admin")
        )

def authenticate_user(username: str, password: str):
    """Authenticate user."""
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({{"exp": expire}})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={{"WWW-Authenticate": "Bearer"}},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

def init_auth(app: FastAPI):
    """Initialize authentication routes."""
    
    @app.post("/token", response_model=Token)
    async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={{"WWW-Authenticate": "Bearer"}},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={{"sub": user.username}}, expires_delta=access_token_expires
        )
        return {{"access_token": access_token, "token_type": "bearer"}}
'''
        
        with open(os.path.join(full_project_path, main_module, "auth.py"), "w") as f:
            f.write(fastapi_auth_content)
    
    # Create HTML templates for login if using Flask
    if is_flask:
        templates_dir = os.path.join(full_project_path, main_module, "templates", "auth")
        os.makedirs(templates_dir, exist_ok=True)
        
        # Login page
        login_template = '''{% extends "base.html" %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card mt-5">
            <div class="card-body">
                <h2 class="card-title text-center mb-4">Login</h2>
                
                <form method="post">
                    <div class="form-group">
                        <label for="username">Username</label>
                        <input type="text" class="form-control" id="username" name="username" required>
                    </div>
                    
                    <div class="form-group mt-3">
                        <label for="password">Password</label>
                        <input type="password" class="form-control" id="password" name="password" required>
                    </div>
                    
                    <div class="d-grid mt-4">
                        <button type="submit" class="btn btn-primary">Login</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
        
        with open(os.path.join(templates_dir, "login.html"), "w") as f:
            f.write(login_template)
    
    print(f"{GREEN}Created security modules{NC}")

def create_logging_module(project_info, full_project_path):
    """Create a logging configuration module."""
    main_module = project_info["main_module"]
    
    utils_dir = os.path.join(full_project_path, main_module, "utils")
    os.makedirs(utils_dir, exist_ok=True)
    
    # Create logging_config.py
    logging_config_content = '''"""
Logging configuration for the project.
"""

import logging
import logging.config
import os
from pathlib import Path

def configure_logging(log_level="INFO", log_file=None):
    """
    Configure logging for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
    
    Returns:
        logging.Logger: The configured logger
    """
    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": log_level,
            "stream": "ext://sys.stdout",
        }
    }
    
    if log_file:
        # Create log directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            
        handlers["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "level": log_level,
            "filename": log_file,
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf8",
        }
    
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"
            },
        },
        "handlers": handlers,
        "loggers": {
            "": {  # Root logger
                "handlers": list(handlers.keys()),
                "level": log_level,
                "propagate": True,
            }
        },
    }
    
    logging.config.dictConfig(config)
    return logging.getLogger()
'''
    
    with open(os.path.join(utils_dir, "logging_config.py"), "w") as f:
        f.write(logging_config_content)
    
    print(f"{GREEN}Created logging module{NC}")

def create_systemd_service(project_info, full_project_path):
    """Create a systemd service file for automation projects."""
    project_name = project_info["project_name"]
    main_module = project_info["main_module"]
    
    print(f"{BLUE}Creating systemd service file...{NC}")
    
    # Create systemd directory
    systemd_dir = os.path.join(full_project_path, "systemd")
    os.makedirs(systemd_dir, exist_ok=True)
    
    # Create service file
    service_path = os.path.join(systemd_dir, f"{project_name}.service")
    service_content = f'''[Unit]
Description={project_name} automation service
After=network.target

[Service]
Type=simple
User=%i
WorkingDirectory={os.path.abspath(full_project_path)}
Environment=PYTHONPATH={os.path.abspath(full_project_path)}
ExecStart={os.path.join(full_project_path, ".venv/bin/python")} -m {main_module}
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
'''
    
    with open(service_path, "w") as f:
        f.write(service_content)
    
    print(f"{GREEN}Created systemd service file{NC}")

def create_vscode_files(project_info, full_project_path):
    """Create VS Code configuration files."""
    project_name = project_info["project_name"]
    main_module = project_info["main_module"]
    python_version = project_info["python_version"]
    
    print(f"{BLUE}Creating VS Code configuration files...{NC}")
    
    # Create .vscode directory
    os.makedirs(os.path.join(full_project_path, ".vscode"), exist_ok=True)
    
    # Create workspace file
    workspace_file = os.path.join(full_project_path, f"{project_name}.code-workspace")
    workspace_content = f'''{{
    "folders": [
        {{
            "name": "{project_name.capitalize()}",
            "path": "."
        }}
    ],
    "settings": {{
        "python.defaultInterpreterPath": "${{workspaceFolder}}/.venv/bin/python",
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": true,
        "python.formatting.provider": "black",
        "editor.formatOnSave": true,
        "python.testing.pytestEnabled": true,
        "python.testing.unittestEnabled": false,
        "python.analysis.extraPaths": [
            "${{workspaceFolder}}"
        ]
    }},
    "extensions": {{
        "recommendations": [
            "ms-python.python",
            "ms-python.vscode-pylance",
            "njpwerner.autodocstring",
            "streetsidesoftware.code-spell-checker",
            "eamodio.gitlens"
        ]
    }}
}}'''
    
    with open(workspace_file, "w") as f:
        f.write(workspace_content)
    
    # Create launch.json
    launch_content = f'''{{
    "version": "0.2.0",
    "configurations": [
        {{
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${{file}}",
            "console": "integratedTerminal",
            "justMyCode": false
        }},
        {{
            "name": "Python: Module",
            "type": "python",
            "request": "launch",
            "module": "{main_module}",
            "console": "integratedTerminal",
            "justMyCode": false,
            "env": {{
                "PYTHONPATH": "${{workspaceFolder}}"
            }}
        }}
    ]
}}'''
    
    with open(os.path.join(full_project_path, ".vscode", "launch.json"), "w") as f:
        f.write(launch_content)
    
    # Create settings.json
    settings_content = '''
{
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.linting.pylintArgs": [
        "--disable=C0111"
    ],
    "python.analysis.extraPaths": [
        "${workspaceFolder}"
    ],
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        }
    }
}'''
    
    with open(os.path.join(full_project_path, ".vscode", "settings.json"), "w") as f:
        f.write(settings_content)
    
    # Create tasks.json
    tasks_content = f'''{{
    "version": "2.0.0",
    "tasks": [
        {{
            "label": "Run Main Module",
            "type": "shell",
            "command": "${{workspaceFolder}}/.venv/bin/python -m {main_module}",
            "problemMatcher": [],
            "group": {{
                "kind": "build",
                "isDefault": true
            }}
        }},
        {{
            "label": "Install Dependencies",
            "type": "shell",
            "command": "${{workspaceFolder}}/.venv/bin/pip install -r requirements.txt",
            "problemMatcher": []
        }},
        {{
            "label": "Install Dev Dependencies",
            "type": "shell",
            "command": "${{workspaceFolder}}/.venv/bin/pip install -r requirements-dev.txt",
            "problemMatcher": []
        }},
        {{
            "label": "Run Tests",
            "type": "shell",
            "command": "${{workspaceFolder}}/.venv/bin/python -m pytest",
            "problemMatcher": []
        }},
        {{
            "label": "Setup Virtual Environment",
            "type": "shell",
            "command": "python{python_version} -m venv .venv && .venv/bin/pip install -U pip && .venv/bin/pip install -r requirements.txt -r requirements-dev.txt",
            "problemMatcher": []
        }}
    ]
}}'''
    
    with open(os.path.join(full_project_path, ".vscode", "tasks.json"), "w") as f:
        f.write(tasks_content)
    
    print(f"{GREEN}Created VS Code configuration files{NC}")
    
    return workspace_file

def run_with_sample_input():
    """Run with sample input for testing."""
    print_banner()
    check_dependencies()
    
    # Use sample data for testing
    project_info = {
        "project_name": "test_project",
        "project_dir": "/tmp",
        "main_module": "test_project",
        "description": "A sample project for testing the CLI interface.\n\nThis project will help users manage their tasks and schedule.",
        "project_types": ["cli", "automation"],
        "python_version": "3.12",
        "dependencies": ["python-dotenv", "click", "rich", "schedule", "requests"],
        "ai_providers": [],
        "ai_models": {},
        "security_features": False,
        "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    print(f"{BLUE}Using sample project information for testing:{NC}")
    print(f"  Project Name: {project_info['project_name']}")
    print(f"  Project Directory: {project_info['project_dir']}")
    print(f"  Project Types: {', '.join(project_info['project_types'])}")
    print(f"  Python Version: {project_info['python_version']}")
    print()
    
    # Create project
    full_project_path = create_project_structure(project_info)
    
    # Create project files
    create_project_files(project_info, full_project_path)
    
    # Create Docker files
    create_docker_files(project_info, full_project_path)
    
    # Create security modules
    create_security_modules(project_info, full_project_path)
    
    # Create logging module
    create_logging_module(project_info, full_project_path)
    
    # Create systemd service file
    create_systemd_service(project_info, full_project_path)
    
    # Create VS Code files
    workspace_file = create_vscode_files(project_info, full_project_path)
    
    # Create environment dump if available
    if HAS_ENV_DUMP:
        try:
            # Create a project info object to include in the dump
            dump_project_info = {
                "name": project_info["project_name"],
                "description": project_info["description"],
                "types": project_info["project_types"],
                "python_version": project_info["python_version"],
                "dependencies": project_info["dependencies"],
                "creation_date": project_info["creation_date"],
                "creator": "create_python_project.py"
            }
            
            # Create the environment dump
            dump_file = create_environment_dump(
                output_file=os.path.join(full_project_path, "environment_dump.md"),
                project_path=full_project_path,
                project_info=dump_project_info
            )
            print(f"{GREEN}Created environment dump: {os.path.basename(dump_file)}{NC}")
        except Exception as e:
            print(f"{YELLOW}Warning: Could not create environment dump: {e}{NC}")
    
    print(f"\n{GREEN}Project created successfully!{NC}")
    print(f"\nNext steps:")
    print(f"1. cd {full_project_path}")
    print(f"2. python -m venv .venv")
    print(f"3. source .venv/bin/activate")
    print(f"4. pip install -r requirements.txt -r requirements-dev.txt")
    print(f"5. code {workspace_file}")
    return full_project_path

def setup_virtual_environment(project_path, python_version):
    """Set up a virtual environment and install dependencies."""
    print(f"{BLUE}Setting up virtual environment...{NC}")
    
    try:
        # Use system Python instead of a specific version
        venv_cmd = f"python3 -m venv {os.path.join(project_path, '.venv')}"
        subprocess.run(venv_cmd, shell=True, check=True)
        
        # Get venv activation script path
        if platform.system() == "Windows":
            activate_script = os.path.join(project_path, ".venv", "Scripts", "activate")
            pip_path = os.path.join(project_path, ".venv", "Scripts", "pip")
        else:
            activate_script = os.path.join(project_path, ".venv", "bin", "activate")
            pip_path = os.path.join(project_path, ".venv", "bin", "pip")
        
        # Install dependencies
        pip_cmd = f"{pip_path} install -r {os.path.join(project_path, 'requirements.txt')}"
        subprocess.run(pip_cmd, shell=True, check=True)
        
        # Install dev dependencies
        pip_dev_cmd = f"{pip_path} install -r {os.path.join(project_path, 'requirements-dev.txt')}"
        subprocess.run(pip_dev_cmd, shell=True, check=True)
        
        print(f"{GREEN}Virtual environment set up successfully!{NC}")
        
        return True, activate_script
    except Exception as e:
        print(f"{RED}Failed to set up virtual environment: {e}{NC}")
        print(f"{YELLOW}You'll need to set up the virtual environment manually.{NC}")
        return False, None

def create_ai_conversation_log(project_info, project_path):
    """Create an AI conversation log for the project."""
    print(f"{BLUE}Creating AI conversation log...{NC}")
    
    conversation_log_path = os.path.join(project_path, "ai_conversation_log.md")
    
    # Start building the content
    content = f"# AI Conversation Log for {project_info['project_name']}\n\n"
    content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Add project description
    content += "## Project Description\n\n"
    content += f"{project_info['description']}\n\n"
    
    # Add AI analysis
    content += "## AI Analysis\n\n"
    
    # Add project types analysis
    content += "### Detected Project Types\n\n"
    if "analysis" in project_info and project_info["analysis"]:
        content += f"- Detected types: {', '.join(project_info['analysis']['project_types'])}\n"
        content += f"- AI integration needed: {'Yes' if project_info['analysis']['needs_ai'] else 'No'}\n"
        content += f"- Web components needed: {'Yes' if project_info['analysis']['needs_web'] else 'No'}\n"
        content += f"- Security features needed: {'Yes' if project_info['analysis']['needs_security'] else 'No'}\n\n"
    else:
        content += "No automated analysis available.\n\n"
    
    # Add AI project plan
    if "project_plan" in project_info and project_info["project_plan"]:
        plan = project_info["project_plan"]
        content += "### Project Plan\n\n"
        content += f"**Summary**: {plan['summary']}\n\n"
        
        content += "**Components**:\n"
        for component in plan["components"]:
            content += f"- {component}\n"
        content += "\n"
        
        content += "**Technology Stack**:\n"
        for stack_type, technologies in plan["technology_stack"].items():
            if technologies:
                content += f"- {stack_type.title()}: {', '.join(technologies)}\n"
        content += "\n"
        
        content += "**Implementation Steps**:\n"
        for i, step in enumerate(plan["implementation_steps"], 1):
            content += f"{i}. {step}\n"
        content += "\n"
        
        content += "**Potential Challenges**:\n"
        for challenge in plan["challenges"]:
            content += f"- {challenge}\n"
        content += "\n"
    
    # Add AI recommendations
    if "ai_recommendations" in project_info and project_info["ai_recommendations"]:
        recommendations = project_info["ai_recommendations"]
        content += "### Technical Recommendations\n\n"
        
        if "user_friendly_summary" in recommendations:
            content += f"**Summary**: {recommendations['user_friendly_summary']}\n\n"
        
        if "project_type" in recommendations:
            content += f"**Main Project Type**: {recommendations['project_type']}\n\n"
        
        if "additional_types" in recommendations:
            content += "**Additional Types**:\n"
            for type_name in recommendations["additional_types"]:
                content += f"- {type_name}\n"
            content += "\n"
        
        if "suggested_dependencies" in recommendations:
            content += "**Suggested Dependencies**:\n"
            for dep in recommendations["suggested_dependencies"]:
                content += f"- {dep}\n"
            content += "\n"
        
        if "suggested_tools" in recommendations:
            content += "**Suggested Tools**:\n"
            for tool in recommendations["suggested_tools"]:
                content += f"- {tool}\n"
            content += "\n"
        
        if "security_considerations" in recommendations:
            content += "**Security Considerations**:\n"
            for security in recommendations["security_considerations"]:
                content += f"- {security}\n"
            content += "\n"
    
    # Add project setup details
    content += "## Project Setup Details\n\n"
    content += f"- Project Name: {project_info['project_name']}\n"
    content += f"- Main Module: {project_info['main_module']}\n"
    content += f"- Python Version: {project_info['python_version']}\n"
    content += f"- Selected Project Types: {', '.join(project_info['project_types'])}\n"
    content += f"- Dependencies: {', '.join(project_info['dependencies'])}\n\n"
    
    # Write to file
    with open(conversation_log_path, "w") as f:
        f.write(content)
    
    print(f"{GREEN}Created AI conversation log: {os.path.basename(conversation_log_path)}{NC}")
    return conversation_log_path

def run_interactive():
    """Run in interactive mode with user input."""
    print_banner()
    check_dependencies()
    
    # Get project information
    project_info = get_project_info()
    
    # Create project
    full_project_path = create_project_structure(project_info)
    
    # Create project files
    create_project_files(project_info, full_project_path)
    
    # Create Docker files
    create_docker_files(project_info, full_project_path)
    
    # Create security modules
    create_security_modules(project_info, full_project_path)
    
    # Create logging module
    create_logging_module(project_info, full_project_path)
    
    # Create systemd service file
    create_systemd_service(project_info, full_project_path)
    
    # Create VS Code files
    workspace_file = create_vscode_files(project_info, full_project_path)
    
    # Create AI conversation log
    create_ai_conversation_log(project_info, full_project_path)
    
    # Create environment dump if available
    if HAS_ENV_DUMP:
        try:
            # Copy dump_environment.py to project directory
            shutil.copy(
                os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dump_environment.py"),
                os.path.join(full_project_path, "dump_environment.py")
            )
            
            # Create a project info object to include in the dump
            dump_project_info = {
                "name": project_info["project_name"],
                "description": project_info["description"],
                "types": project_info["project_types"],
                "python_version": project_info["python_version"],
                "dependencies": project_info["dependencies"],
                "creation_date": project_info["creation_date"],
                "creator": "create_python_project.py"
            }
            
            # Create the environment dump
            dump_file = create_environment_dump(
                output_file=os.path.join(full_project_path, "environment_dump.md"),
                project_path=full_project_path,
                project_info=dump_project_info
            )
            print(f"{GREEN}Created environment dump: {os.path.basename(dump_file)}{NC}")
        except Exception as e:
            print(f"{YELLOW}Warning: Could not create environment dump: {e}{NC}")
    
    # Set up virtual environment
    venv_success, activate_script = setup_virtual_environment(
        full_project_path, 
        project_info["python_version"]
    )
    
    print(f"\n{GREEN}Project created successfully!{NC}")
    
    if venv_success:
        print(f"\nNext steps:")
        print(f"1. cd {full_project_path}")
        print(f"2. source {os.path.basename(activate_script)}")
        print(f"3. Start coding! The main files are in the {project_info['main_module']} directory")
        
        # Try to initialize git repository
        try:
            subprocess.run(f"cd {full_project_path} && git init", shell=True, check=False)
            print(f"4. A git repository has been initialized for you")
        except:
            pass
    else:
        print(f"\nNext steps:")
        print(f"1. cd {full_project_path}")
        print(f"2. python -m venv .venv")
        print(f"3. source .venv/bin/activate")
        print(f"4. pip install -r requirements.txt -r requirements-dev.txt")
    
    # Open VS Code if available
    if shutil.which("code"):
        try:
            subprocess.run(f"code {workspace_file}", shell=True, check=False)
        except:
            print(f"5. code {workspace_file}")
    
    return full_project_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new Python project")
    parser.add_argument("--test", action="store_true", help="Run with sample data for testing")
    parser.add_argument("--name", type=str, help="Project name")
    parser.add_argument("--dir", type=str, help="Project directory")
    args = parser.parse_args()
    
    if args.test:
        # Run with sample data
        run_with_sample_input()
    else:
        # Run in interactive mode
        run_interactive()