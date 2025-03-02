"""
Utilities for file operations in RunKit.
"""

import os
import shutil
import importlib.resources as pkg_resources
from pathlib import Path
from typing import List, Dict, Union, Any

from jinja2 import Environment, FileSystemLoader

def create_directory(path: str) -> None:
    """
    Create directory if it doesn't exist.
    
    Args:
        path: Path to the directory to create
    """
    os.makedirs(path, exist_ok=True)

def create_file(path: str, content: str = "") -> None:
    """
    Create a file with optional content.
    
    Args:
        path: Path to the file to create
        content: Content to write to the file
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def copy_template_file(src_path: str, dest_path: str, context: Dict[str, Any] = None) -> None:
    """
    Copy a template file from the package to the destination path,
    optionally rendering it with Jinja2 if context is provided.
    
    Args:
        src_path: Path to the source template file
        dest_path: Path to the destination file
        context: Optional context for Jinja2 rendering
    """
    # Verbose debug for troubleshooting
    print(f"Source template: {src_path}")
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Template file not found: {src_path}")
    
    template_dir = os.path.dirname(src_path)
    template_file = os.path.basename(src_path)
    
    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    if context:
        # Render the template with Jinja2
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(template_file)
        rendered = template.render(**context)
        
        # Write the rendered template to the destination
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(rendered)
    else:
        # Simple copy without rendering
        shutil.copy2(os.path.join(template_dir, template_file), dest_path)

def merge_requirements(requirement_files: List[str]) -> str:
    """
    Merge multiple requirements.txt files into a single content string,
    removing duplicates.
    
    Args:
        requirement_files: List of paths to requirements.txt files
        
    Returns:
        A string with the merged requirements
    """
    requirements = set()
    
    for req_file in requirement_files:
        try:
            with open(req_file, "r", encoding="utf-8") as f:
                file_requirements = [
                    line.strip() for line in f.readlines() 
                    if line.strip() and not line.startswith("#")
                ]
                requirements.update(file_requirements)
        except FileNotFoundError:
            print(f"Warning: Requirements file not found: {req_file}")
            # Add a minimal set of requirements so the project can still function
            if "anthropic" in req_file:
                requirements.add("anthropic>=0.18.0")
            elif "gemini" in req_file:
                requirements.add("google-generativeai>=0.3.0")
                
    # Always include base requirements
    requirements.add("streamlit>=1.24.0")
    requirements.add("python-dotenv>=1.0.0")
    requirements.add("requests>=2.31.0")
    
    # Sort alphabetically for consistency
    return "\n".join(sorted(requirements)) + "\n"

def generate_project_structure(
    project_path: str,
    project_name: str,
    provider: str,
    features: List[str],
    project_type: str,
    context: Dict[str, Any]
) -> None:
    """
    Generate the complete project structure based on selections.
    
    Args:
        project_path: Path where the project will be created
        project_name: Name of the project
        provider: Selected LLM provider
        features: List of selected features
        project_type: Selected project type
        context: Context variables for templating
    """
    from run_kit.constants import (
        PROVIDER_DIRS, FEATURE_DIRS, PROJECT_TYPE_FILES,
        TEMPLATE_BASE_PATH, TEMPLATE_PROVIDERS_PATH, TEMPLATE_FEATURES_PATH,
        TEMPLATE_PROJECT_TYPES_PATH
    )
    
    # Debug print
    print(f"Generating project structure in: {project_path}")
    print(f"Base template path: {TEMPLATE_BASE_PATH}")
    
    # Create the main project directory
    create_directory(project_path)
    
    # Create a minimal app.py if we can't find templates
    if not os.path.exists(TEMPLATE_BASE_PATH):
        print(f"Warning: Base template directory not found: {TEMPLATE_BASE_PATH}")
        print("Creating minimal project structure...")
        
        # Create minimal app.py
        minimal_app = f"""
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="{project_name}",
    page_icon="🚀",
    layout="wide"
)

# App title
st.title("{project_name}")
st.markdown("#### AI Assistant")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask me anything...")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({{"role": "user", "content": prompt}})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        response = f"This is a placeholder response. To get actual AI responses, please configure the {provider} integration."
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({{"role": "assistant", "content": response}})

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("This is a minimal AI assistant app generated with RunKit.")
    
    st.divider()
    
    # Reset conversation button
    if st.button("Reset Conversation"):
        st.session_state.messages = []
        st.rerun()
"""
        
        # Create the basic structure
        create_directory(os.path.join(project_path, "app"))
        create_directory(os.path.join(project_path, "app", "data"))
        create_directory(os.path.join(project_path, "app", "llm"))
        create_directory(os.path.join(project_path, "app", "utils"))
        
        # Create app.py
        create_file(os.path.join(project_path, "app.py"), minimal_app)
        
        # Create minimal .env.example
        env_example = """
# API Keys
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
OLLAMA_BASE_URL=http://localhost:11434
"""
        create_file(os.path.join(project_path, ".env.example"), env_example)
        
        # Create requirements.txt
        requirements = """
streamlit>=1.24.0
python-dotenv>=1.0.0
requests>=2.31.0
"""
        if provider == "Anthropic (Claude)" or provider == "Multiple providers":
            requirements += "anthropic>=0.18.0\n"
        if provider == "Google (Gemini)" or provider == "Multiple providers":
            requirements += "google-generativeai>=0.3.0\n"
            
        create_file(os.path.join(project_path, "requirements.txt"), requirements)
        
        return
    
    # Copy base template files
    try:
        for template_file in os.listdir(TEMPLATE_BASE_PATH):
            src_path = os.path.join(TEMPLATE_BASE_PATH, template_file)
            dest_path = os.path.join(project_path, template_file)
            copy_template_file(src_path, dest_path, context)
    except FileNotFoundError as e:
        print(f"Warning: {str(e)}")
        raise
    
    # Create the basic directory structure
    for dir_path in ["app", "app/components", "app/llm", "app/utils", "app/data", "app/styles", "tests"]:
        create_directory(os.path.join(project_path, dir_path))
    
    # Add provider-specific files
    provider_dir = PROVIDER_DIRS[provider]
    if isinstance(provider_dir, list):
        # Multiple providers
        for p_dir in provider_dir:
            provider_templates_dir = os.path.join(TEMPLATE_PROVIDERS_PATH, p_dir)
            provider_dest_dir = os.path.join(project_path, "app/llm", p_dir)
            create_directory(provider_dest_dir)
            
            try:
                for template_file in os.listdir(provider_templates_dir):
                    src_path = os.path.join(provider_templates_dir, template_file)
                    dest_path = os.path.join(provider_dest_dir, template_file)
                    copy_template_file(src_path, dest_path, context)
            except FileNotFoundError:
                print(f"Warning: Provider template directory not found: {provider_templates_dir}")
    else:
        # Single provider
        provider_templates_dir = os.path.join(TEMPLATE_PROVIDERS_PATH, provider_dir)
        provider_dest_dir = os.path.join(project_path, "app/llm")
        
        try:
            for template_file in os.listdir(provider_templates_dir):
                src_path = os.path.join(provider_templates_dir, template_file)
                dest_path = os.path.join(provider_dest_dir, template_file)
                copy_template_file(src_path, dest_path, context)
        except FileNotFoundError:
            print(f"Warning: Provider template directory not found: {provider_templates_dir}")
    
    # Add feature-specific files
    for feature in features:
        feature_dir = FEATURE_DIRS[feature]
        feature_templates_dir = os.path.join(TEMPLATE_FEATURES_PATH, feature_dir)
        
        if feature == "Vector database":
            # Special case for vector database - creates a db directory
            create_directory(os.path.join(project_path, "app/db"))
            feature_dest_dir = os.path.join(project_path, "app/db")
        else:
            feature_dest_dir = os.path.join(project_path, "app", feature_dir.lower())
            create_directory(feature_dest_dir)
        
        try:
            for template_file in os.listdir(feature_templates_dir):
                src_path = os.path.join(feature_templates_dir, template_file)
                dest_path = os.path.join(feature_dest_dir, template_file)
                copy_template_file(src_path, dest_path, context)
        except FileNotFoundError:
            print(f"Warning: Feature template directory not found: {feature_templates_dir}")
    
    # Add project type specific app.py
    project_type_file = PROJECT_TYPE_FILES[project_type]
    project_type_src = os.path.join(TEMPLATE_PROJECT_TYPES_PATH, project_type_file)
    project_type_dest = os.path.join(project_path, "app.py")
    
    try:
        copy_template_file(project_type_src, project_type_dest, context)
    except FileNotFoundError:
        print(f"Warning: Project type file not found: {project_type_src}")
        # Create a minimal app.py
        minimal_app = f"""
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="{project_name}",
    page_icon="🚀",
    layout="wide"
)

# App title
st.title("{project_name}")
st.markdown("#### AI Assistant")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask me anything...")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({{"role": "user", "content": prompt}})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        response = f"This is a placeholder response. To get actual AI responses, please configure the {provider} integration."
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({{"role": "assistant", "content": response}})

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("This is a minimal AI assistant app generated with RunKit.")
    
    st.divider()
    
    # Reset conversation button
    if st.button("Reset Conversation"):
        st.session_state.messages = []
        st.rerun()
"""
        create_file(project_type_dest, minimal_app)
    
    # Merge requirements.txt files
    req_files = [os.path.join(TEMPLATE_BASE_PATH, "requirements.base.txt")]
    
    # Add provider requirements
    if isinstance(provider_dir, list):
        for p_dir in provider_dir:
            req_files.append(os.path.join(TEMPLATE_PROVIDERS_PATH, p_dir, "requirements.txt"))
    else:
        req_files.append(os.path.join(TEMPLATE_PROVIDERS_PATH, provider_dir, "requirements.txt"))
    
    # Add feature requirements
    for feature in features:
        feature_dir = FEATURE_DIRS[feature]
        req_files.append(os.path.join(TEMPLATE_FEATURES_PATH, feature_dir, "requirements.txt"))
    
    # Write the merged requirements.txt
    merged_requirements = merge_requirements(req_files)
    create_file(os.path.join(project_path, "requirements.txt"), merged_requirements)