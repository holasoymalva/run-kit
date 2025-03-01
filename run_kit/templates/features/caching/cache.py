"""
Caching system for LLM responses to reduce API calls and improve response time.
"""

import hashlib
import json
import os
import pickle
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple

# Cache directory
CACHE_DIR = os.path.join("app", "data", "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

class ResponseCache:
    """
    A simple caching system for LLM responses.
    """
    
    def __init__(self, cache_dir: str = CACHE_DIR, ttl_hours: int = 24):
        """
        Initialize the cache.
        
        Args:
            cache_dir: Directory to store cache files
            ttl_hours: Time-to-live in hours for cache entries
        """
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
    
    def _get_cache_key(self, prompt: str, params: Dict[str, Any]) -> str:
        """
        Generate a unique cache key based on the prompt and parameters.
        
        Args:
            prompt: The user's input prompt
            params: The parameters used for the LLM request
            
        Returns:
            str: A hash to use as the cache key
        """
        # Create a deterministic representation of the input
        cache_input = {
            "prompt": prompt,
            "params": params
        }
        serialized = json.dumps(cache_input, sort_keys=True)
        return hashlib.md5(serialized.encode()).hexdigest()
    
    def _get_cache_path(self, key: str) -> str:
        """
        Get the filesystem path for a cache entry.
        
        Args:
            key: The cache key
            
        Returns:
            str: Path to the cache file
        """
        return os.path.join(self.cache_dir, f"{key}.pkl")
    
    def get(self, prompt: str, params: Dict[str, Any]) -> Optional[str]:
        """
        Retrieve a cached response if available and not expired.
        
        Args:
            prompt: The user's input prompt
            params: The parameters used for the LLM request
            
        Returns:
            Optional[str]: The cached response or None if not found/expired
        """
        key = self._get_cache_key(prompt, params)
        cache_path = self._get_cache_path(key)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, "rb") as f:
                timestamp, response = pickle.load(f)
            
            # Check if cache has expired
            if datetime.now() - timestamp > self.ttl:
                os.remove(cache_path)
                return None
            
            return response
        except Exception as e:
            print(f"Cache error: {str(e)}")
            return None
    
    def set(self, prompt: str, params: Dict[str, Any], response: str) -> None:
        """
        Store a response in the cache.
        
        Args:
            prompt: The user's input prompt
            params: The parameters used for the LLM request
            response: The LLM response to cache
        """
        key = self._get_cache_key(prompt, params)
        cache_path = self._get_cache_path(key)
        
        try:
            with open(cache_path, "wb") as f:
                pickle.dump((datetime.now(), response), f)
        except Exception as e:
            print(f"Cache save error: {str(e)}")
    
    def clear(self) -> None:
        """
        Clear all cache entries.
        """
        for filename in os.listdir(self.cache_dir):
            if filename.endswith(".pkl"):
                os.remove(os.path.join(self.cache_dir, filename))


# Singleton instance
cache = ResponseCache()

def get_cached_response(prompt: str, params: Dict[str, Any] = None) -> Optional[str]:
    """
    Get a cached response for the given prompt and parameters.
    
    Args:
        prompt: The user's input prompt
        params: The parameters used for the LLM request
        
    Returns:
        Optional[str]: The cached response or None if not found
    """
    if params is None:
        params = {}
    return cache.get(prompt, params)

def cache_response(prompt: str, params: Dict[str, Any], response: str) -> None:
    """
    Cache a response for the given prompt and parameters.
    
    Args:
        prompt: The user's input prompt
        params: The parameters used for the LLM request
        response: The LLM response to cache
    """
    if params is None:
        params = {}
    cache.set(prompt, params, response)