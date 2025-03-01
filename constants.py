"""
Constants used throughout the RunKit package.
"""

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

# Template paths
TEMPLATE_BASE_PATH = "templates/base"
TEMPLATE_PROVIDERS_PATH = "templates/providers"
TEMPLATE_FEATURES_PATH = "templates/features"
TEMPLATE_PROJECT_TYPES_PATH = "project_types"

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