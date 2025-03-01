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
    # Get the package directory
    package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(package_dir, os.path.dirname(src_path))
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
        with open(req_file, "r", encoding="utf-8") as f:
            file_requirements = [
                line.strip() for line in f.readlines() 
                if line.strip() and not line.startswith("#")
            ]
            requirements.update(file_requirements)
    
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
        TEMPLATE_BASE_PATH, TEMPLATE_PROVIDERS_PATH, TEMPLATE_FEATURES_PATH
    )
    
    # Create the main project directory
    create_directory(project_path)
    
    # Copy base template files
    base_templates_dir = os.path.join(TEMPLATE_BASE_PATH)
    for template_file in os.listdir(base_templates_dir):
        src_path = os.path.join(base_templates_dir, template_file)
        dest_path = os.path.join(project_path, template_file)
        copy_template_file(src_path, dest_path, context)
    
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
            
            for template_file in os.listdir(provider_templates_dir):
                src_path = os.path.join(provider_templates_dir, template_file)
                dest_path = os.path.join(provider_dest_dir, template_file)
                copy_template_file(src_path, dest_path, context)
    else:
        # Single provider
        provider_templates_dir = os.path.join(TEMPLATE_PROVIDERS_PATH, provider_dir)
        provider_dest_dir = os.path.join(project_path, "app/llm")
        
        for template_file in os.listdir(provider_templates_dir):
            src_path = os.path.join(provider_templates_dir, template_file)
            dest_path = os.path.join(provider_dest_dir, template_file)
            copy_template_file(src_path, dest_path, context)
    
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
        
        for template_file in os.listdir(feature_templates_dir):
            src_path = os.path.join(feature_templates_dir, template_file)
            dest_path = os.path.join(feature_dest_dir, template_file)
            copy_template_file(src_path, dest_path, context)
    
    # Add project type specific app.py
    project_type_file = PROJECT_TYPE_FILES[project_type]
    project_type_src = os.path.join(TEMPLATE_PROJECT_TYPES_PATH, project_type_file)
    project_type_dest = os.path.join(project_path, "app.py")
    copy_template_file(project_type_src, project_type_dest, context)
    
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