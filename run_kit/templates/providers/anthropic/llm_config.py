"""
Anthropic (Claude) configuration for LLM integration.
"""

import os
import anthropic
from anthropic import Anthropic
from typing import Dict, Any, Optional

# Load API key from environment variables
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Model configuration
DEFAULT_MODEL = "claude-3-opus-20240229"
DEFAULT_PARAMS = {
    "temperature": 0.7,
    "max_tokens": 1024,
    "top_p": 0.95,
}

def get_client() -> Anthropic:
    """
    Get an initialized Anthropic client.
    
    Returns:
        Anthropic: The Anthropic client.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("Anthropic API key not found. Please set the ANTHROPIC_API_KEY environment variable.")
    
    return Anthropic(api_key=ANTHROPIC_API_KEY)

def get_anthropic_response(prompt: str, params: Optional[Dict[str, Any]] = None) -> str:
    """
    Get a response from Anthropic's Claude.
    
    Args:
        prompt: The user's input prompt
        params: Optional parameters to override defaults
    
    Returns:
        str: The AI response
    """
    client = get_client()
    
    # Merge default params with any provided params
    request_params = DEFAULT_PARAMS.copy()
    if params:
        request_params.update(params)
    
    # Create message
    response = client.messages.create(
        model=DEFAULT_MODEL,
        max_tokens=request_params["max_tokens"],
        temperature=request_params["temperature"],
        system="You are a helpful AI assistant.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.content[0].text