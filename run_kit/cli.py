"""
Command-line interface for RunKit.
"""

import os
import sys
import click
import inquirer
from colorama import init, Fore, Style

from run_kit.constants import (
    PROVIDERS, FEATURES, PROJECT_TYPES, BANNER
)
from run_kit.utils.files import generate_project_structure

# Initialize colorama for cross-platform colored terminal output
init()

def print_banner():
    """Print the RunKit ASCII art banner."""
    print(Fore.CYAN + BANNER + Style.RESET_ALL)

def print_success(message):
    """Print a success message in green."""
    print(Fore.GREEN + f"✅ {message}" + Style.RESET_ALL)

def print_info(message):
    """Print an info message in blue."""
    print(Fore.BLUE + f"ℹ️ {message}" + Style.RESET_ALL)

def print_error(message):
    """Print an error message in red."""
    print(Fore.RED + f"❌ {message}" + Style.RESET_ALL)

def interactive_setup():
    """
    Run the interactive setup to gather user preferences.
    
    Returns:
        dict: Configuration options selected by the user
    """
    questions = [
        inquirer.List(
            'provider',
            message="Select the LLM provider you want to use",
            choices=PROVIDERS,
        ),
        inquirer.Checkbox(
            'features',
            message="Select additional features",
            choices=FEATURES,
            default=["Caching system", "Conversation persistence"]
        ),
        inquirer.List(
            'project_type',
            message="What type of project do you want to create?",
            choices=PROJECT_TYPES,
        ),
    ]
    
    return inquirer.prompt(questions)

@click.command()
@click.argument('project_name')
@click.option('--provider', type=click.Choice(PROVIDERS), help='LLM provider to use')
@click.option('--features', multiple=True, type=click.Choice(FEATURES), help='Additional features to include')
@click.option('--project-type', 'project_type', type=click.Choice(PROJECT_TYPES), help='Type of project to create')
def main(project_name, provider, features, project_type):
    """
    Initialize a new AI project with RunKit.
    
    PROJECT_NAME is the name of the project to create.
    """
    print_banner()
    print_info(f"Initializing AI project: {project_name}")
    
    # If not all options are provided, run interactive setup
    if not all([provider, features, project_type]):
        config = interactive_setup()
        provider = config.get('provider', provider)
        features = config.get('features', features)
        project_type = config.get('project_type', project_type)
    
    # Create project directory path
    project_path = os.path.abspath(project_name)
    
    # Check if directory already exists
    if os.path.exists(project_path):
        if os.listdir(project_path):
            print_error(f"Directory '{project_name}' already exists and is not empty.")
            sys.exit(1)
    
    # Prepare context for template rendering
    context = {
        'project_name': project_name,
        'provider': provider,
        'features': features,
        'project_type': project_type
    }
    
    # Generate the project files and structure
    try:
        generate_project_structure(
            project_path,
            project_name,
            provider,
            features,
            project_type,
            context
        )
        print_success(f"Project '{project_name}' created successfully!")
        print_info(f"To get started, run:")
        print(f"\ncd {project_name}")
        print("pip install -r requirements.txt")
        print("cp .env.example .env  # Add your API keys")
        print("streamlit run app.py")
    except Exception as e:
        print_error(f"Error creating project: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()