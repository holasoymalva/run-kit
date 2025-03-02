"""
Constants used throughout the RunKit package.
"""

import os
import sys
from pathlib import Path

# Get the package directory (absolute path)
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

# Provider options
PROVIDER_ANTHROPIC = "Anthropic (Claude)"
PROVIDER_GEMINI = "Google (Gemini)"
PROVIDER_OLLAMA = "LLM Local (Ollama)"
PROVIDER_MULTIPLE = "Multiple providers"

PROVIDERS = [
    PROVIDER_ANTHROPIC,
    PROVIDER_GEMINI,
    PROVIDER_OLLAMA,
    PROVIDER_MULTIPLE
]

# Feature options
FEATURE_CACHING = "Caching system"
FEATURE_PERSISTENCE = "Conversation persistence"
FEATURE_FILE_UPLOADS = "File uploads"
FEATURE_VECTOR_DB = "Vector database"

FEATURES = [
    FEATURE_CACHING,
    FEATURE_PERSISTENCE,
    FEATURE_FILE_UPLOADS,
    FEATURE_VECTOR_DB
]

# Project type options
PROJECT_SIMPLE_CHAT = "Simple chat"
PROJECT_MEMORY_ASSISTANT = "Memory-enhanced assistant"
PROJECT_DOCUMENT_ANALYZER = "Document analyzer"
PROJECT_SPECIALIZED_AGENT = "Specialized agent"

PROJECT_TYPES = [
    PROJECT_SIMPLE_CHAT,
    PROJECT_MEMORY_ASSISTANT,
    PROJECT_DOCUMENT_ANALYZER,
    PROJECT_SPECIALIZED_AGENT
]

# Template paths (absolute paths)
TEMPLATE_BASE_PATH = os.path.join(PACKAGE_DIR, "templates", "base")
TEMPLATE_PROVIDERS_PATH = os.path.join(PACKAGE_DIR, "templates", "providers")
TEMPLATE_FEATURES_PATH = os.path.join(PACKAGE_DIR, "templates", "features")
TEMPLATE_PROJECT_TYPES_PATH = os.path.join(PACKAGE_DIR, "project_types")

# Debug information - print important paths
def print_debug_info():
    print(f"Package directory: {PACKAGE_DIR}")
    print(f"Template base path: {TEMPLATE_BASE_PATH}")
    print(f"Template providers path: {TEMPLATE_PROVIDERS_PATH}")
    print(f"Template features path: {TEMPLATE_FEATURES_PATH}")
    print(f"Template project types path: {TEMPLATE_PROJECT_TYPES_PATH}")
    
    # Check if directories exist
    print(f"Template base path exists: {os.path.exists(TEMPLATE_BASE_PATH)}")
    print(f"Template providers path exists: {os.path.exists(TEMPLATE_PROVIDERS_PATH)}")
    print(f"Template features path exists: {os.path.exists(TEMPLATE_FEATURES_PATH)}")
    print(f"Template project types path exists: {os.path.exists(TEMPLATE_PROJECT_TYPES_PATH)}")

# File structure templates
STRUCTURE_BASE = [
    "app.py",
    ".env.example",
    "README.md",
    "requirements.txt",
    "app/",
    "app/components/",
    "app/llm/",
    "app/utils/",
    "app/data/",
    "app/styles/",
    "tests/"
]

# Map of provider names to their directory names
PROVIDER_DIRS = {
    PROVIDER_ANTHROPIC: "anthropic",
    PROVIDER_GEMINI: "gemini",
    PROVIDER_OLLAMA: "ollama",
    PROVIDER_MULTIPLE: ["anthropic", "gemini", "ollama"]
}

# Map of feature names to their directory names
FEATURE_DIRS = {
    FEATURE_CACHING: "caching",
    FEATURE_PERSISTENCE: "conversation_persistence",
    FEATURE_FILE_UPLOADS: "file_uploads",
    FEATURE_VECTOR_DB: "vector_db"
}

# Map of project types to their filenames
PROJECT_TYPE_FILES = {
    PROJECT_SIMPLE_CHAT: "simple_chat.py",
    PROJECT_MEMORY_ASSISTANT: "memory_assistant.py",
    PROJECT_DOCUMENT_ANALYZER: "document_analyzer.py",
    PROJECT_SPECIALIZED_AGENT: "specialized_agent.py"
}

# ASCII Art banner
BANNER = r"""
╭──────────────────────────────────────────────────╮
│                                                  │
│   🚀 RunKit - AI Project Scaffolding Tool        │
│                                                  │
╰──────────────────────────────────────────────────╯
"""