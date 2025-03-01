"""
Ollama configuration for local LLM integration.
"""

import os
import requests
from typing import Dict, Any, Optional

# Load configuration from environment variables
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# Model configuration
DEFAULT_PARAMS = {
    "temperature": la.7,
    "max_tokens": 1024,
    "top_p": 0.95,
    "stream": False,
}

def get_ollama_response(prompt: str, params: Optional[Dict[str, Any]] = None) -> str:
    """
    Get a response from a local Ollama instance.
    
    Args:
        prompt: The user's input prompt
        params: Optional parameters to override defaults
    
    Returns:
        str: The AI response
    """
    # Merge default params with any provided params
    request_params = DEFAULT_PARAMS.copy()
    if params:
        request_params.update(params)
    
    # Build the request payload
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        **request_params
    }
    
    # Make the API request to Ollama
    url = f"{OLLAMA_BASE_URL}/api/generate"
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "No response generated")
    except requests.exceptions.RequestException as e:
        error_msg = f"Error connecting to Ollama: {str(e)}"
        print(error_msg)
        return f"Error: {error_msg}. Make sure Ollama is running locally and the model is available."