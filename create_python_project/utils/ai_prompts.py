"""AI prompting utilities for project creation."""

import json
import re
import logging
from typing import Dict, List, Optional, Any

# Import the safely_parse_json function from main module
try:
    from create_python_project.create_python_project import safely_parse_json
except ImportError:
    # Fallback implementation if import fails
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
                    logging.warning(f"Failed to extract valid JSON")
                    return default
            else:
                logging.warning(f"No JSON found in response")
                return default

def generate_domain_questions(
    description: str,
    keywords: List[str],
    ai_provider: Any,
    provider: Optional[str] = None,
    model: Optional[str] = None
) -> Dict[str, str]:
    """
    Generate domain-specific questions based on project description and keywords.
    
    Args:
        description: Project description string
        keywords: List of technology keywords
        ai_provider: AI provider instance
        provider: Specific AI provider to use (optional)
        model: Specific model to use (optional)
    
    Returns:
        dict: Dictionary mapping question_id to question_text
    """
    prompt = f"""
    Based on the following project description and technology keywords, generate 3-5 
    important questions that would help determine the specific technical requirements.
    
    PROJECT DESCRIPTION:
    {description}
    
    TECHNOLOGY KEYWORDS:
    {', '.join(keywords)}
    
    For each question, provide a clear, concise prompt that would help determine:
    1. Integration details with external services
    2. Data storage or database requirements
    3. Authentication or security needs
    4. Deployment or scaling considerations
    
    Return ONLY a JSON object like this:
    {{
        "q1": "Question text for the first domain-specific question?",
        "q2": "Question text for the second domain-specific question?",
        ...
    }}
    """
    
    # Send to AI provider
    try:
        ai_response = ai_provider.ai_query(prompt, provider, model)
        
        # Parse response as JSON
        try:
            return json.loads(ai_response)
        except json.JSONDecodeError:
            # Extract JSON if parsing fails
            json_pattern = r'\{[\s\S]*\}'
            match = re.search(json_pattern, ai_response)
            if match:
                return json.loads(match.group(0))
            else:
                # Return a default question if extraction fails
                return {"q1": "What specific features will your project need?"}
    except Exception as e:
        # Log the error and return a default question
        print(f"Error generating domain questions: {e}")
        return {"q1": "What specific features will your project need?"}

def get_refined_recommendations(
    project_info: Dict[str, Any],
    ai_provider: Any,
    provider: Optional[str] = None,
    model: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get detailed recommendations based on all collected project information.
    
    Args:
        project_info: Dictionary containing project information
        ai_provider: AI provider instance
        provider: Specific AI provider to use (optional)
        model: Specific model to use (optional)
    
    Returns:
        dict: Dictionary with refined recommendations
    """
    # Extract relevant information
    description = project_info.get('description', '')
    project_types = project_info.get('project_types', [])
    custom_keywords = project_info.get('custom_keywords', [])
    domain_answers = project_info.get('domain_answers', {})
    
    # Combine all information into a comprehensive prompt
    prompt = f"""
    Based on the following project information, provide specific technical recommendations
    for setting up this Python project.
    
    PROJECT DESCRIPTION:
    {description}
    
    PROJECT TYPES:
    {', '.join(project_types)}
    
    CUSTOM KEYWORDS:
    {', '.join(custom_keywords)}
    
    DOMAIN-SPECIFIC INFORMATION:
    {json.dumps(domain_answers, indent=2)}
    
    Provide your response as a JSON object with the following structure:
    {{
        "suggested_dependencies": [
            {{"name": "package-name", "description": "Brief explanation of what this package provides"}},
            ...
        ],
        "suggested_project_structure": [
            {{"path": "path/to/module.py", "purpose": "Brief description of this module's purpose"}},
            ...
        ],
        "deployment_recommendations": [
            "Specific deployment recommendation",
            ...
        ],
        "security_considerations": [
            "Specific security consideration",
            ...
        ]
    }}
    """
    
    # Send to AI provider
    try:
        ai_response = ai_provider.ai_query(prompt, provider, model)
        return safely_parse_json(ai_response, default={})
    except Exception as e:
        # Log the error and return an empty dict
        print(f"Error getting refined recommendations: {e}")
        return {}