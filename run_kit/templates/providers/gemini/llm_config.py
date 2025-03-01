"""
Google (Gemini) configuration for LLM integration.
"""

import os
import google.generativeai as genai
from typing import Dict, Any, Optional

# Load API key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Model configuration
DEFAULT_MODEL = "gemini-1.5-pro"
DEFAULT_PARAMS = {
    "temperature": 0.7,
    "max_output_tokens": 1024,
    "top_p": 0.95,
    "top_k": 40,
}

def initialize_genai():
    """
    Initialize the Google Generative AI client.
    """
    if not GOOGLE_API_KEY:
        raise ValueError("Google API key not found. Please set the GOOGLE_API_KEY environment variable.")
    
    genai.configure(api_key=GOOGLE_API_KEY)

def get_gemini_response(prompt: str, params: Optional[Dict[str, Any]] = None) -> str:
    """
    Get a response from Google's Gemini.
    
    Args:
        prompt: The user's input prompt
        params: Optional parameters to override defaults
    
    Returns:
        str: The AI response
    """
    # Initialize the client
    initialize_genai()
    
    # Merge default params with any provided params
    request_params = DEFAULT_PARAMS.copy()
    if params:
        request_params.update(params)
    
    # Configure the model
    model = genai.GenerativeModel(
        model_name=DEFAULT_MODEL,
        generation_config=request_params
    )
    
    # Generate response
    response = model.generate_content(prompt)
    
    return response.text