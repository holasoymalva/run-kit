"""
{{ project_name }} - Specialized AI Agent
Generated with RunKit
"""

import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

# CRITICAL: set_page_config MUST be the first Streamlit call
st.set_page_config(
    page_title="{{ project_name }} - Specialized Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_mode" not in st.session_state:
    st.session_state.agent_mode = "General Assistant"
if "history" not in st.session_state:
    st.session_state.history = []

# Define agent modes
AGENT_MODES = {
    "General Assistant": {
        "icon": "🤖",
        "description": "A general-purpose AI assistant that can help with a wide range of tasks.",
        "system_prompt": "You are a helpful AI assistant.",
    },
    "Technical Expert": {
        "icon": "👨‍💻",
        "description": "Specialized in technical topics such as programming, data science, and engineering.",
        "system_prompt": "You are a technical expert with deep knowledge of programming, computer science, data science, and engineering. Provide detailed technical explanations and code examples when appropriate.",
    },
    "Creative Writer": {
        "icon": "✍️",
        "description": "Helps with creative writing, story development, and content creation.",
        "system_prompt": "You are a creative writing assistant. Help with developing stories, characters, plots, and other creative content. Be imaginative and offer suggestions that spark creativity.",
    },
    "Learning Coach": {
        "icon": "🧑‍🏫",
        "description": "Assists with learning new subjects and concepts through explanations and examples.",
        "system_prompt": "You are a learning coach focused on helping people understand complex topics. Explain concepts clearly, use analogies when helpful, and adapt your explanations to different levels of understanding.",
    },
    "Research Assistant": {
        "icon": "🔍",
        "description": "Helps organize information and provides structured responses for research.",
        "system_prompt": "You are a research assistant. Help organize information, provide structured responses, and suggest approaches for investigation. Present information in a clear, logical manner suitable for research purposes.",
    }
}

# App title and description
st.title(f"{AGENT_MODES[st.session_state.agent_mode]['icon']} {{ project_name }}")
st.markdown(f"#### *Specialized AI Agent - {st.session_state.agent_mode} Mode*")

# Safe import function
def load_llm_client():
    """Safely load the LLM client after Streamlit initialization"""
    {% if provider == "Anthropic (Claude)" %}
    try:
        from app.llm.llm_config import get_anthropic_response
        return get_anthropic_response
    except ImportError:
        return lambda x: f"Error: Anthropic client not available. Please check your installation."
    {% elif provider == "Google (Gemini)" %}
    try:
        from app.llm.llm_config import get_gemini_response
        return get_gemini_response
    except ImportError:
        return lambda x: f"Error: Gemini client not available. Please check your installation."
    {% elif provider == "LLM Local (Ollama)" %}
    try:
        from app.llm.llm_config import get_ollama_response
        return get_ollama_response
    except ImportError:
        return lambda x: f"Error: Ollama client not available. Please check your installation."
    {% else %}
    # Default for multiple providers
    try:
        from app.llm.anthropic.llm_config import get_anthropic_response
        return get_anthropic_response
    except ImportError:
        return lambda x: f"Error: LLM client not available. Please check your installation."
    {% endif %}

# Load LLM client
llm_client = load_llm_client()

# Helper functions
def get_agent_response(prompt, mode):
    """Get a response from the AI with the appropriate agent mode"""
    system_prompt = AGENT_MODES[mode]["system_prompt"]
    
    # Build the full prompt
    full_prompt = f"""
    {system_prompt}
    
    User query: {prompt}
    
    Please respond in a manner appropriate for your role as a {mode}.
    """
    
    try:
        return llm_client(full_prompt)
    except Exception as e:
        return f"I'm having trouble generating a response. Error: {str(e)}"

# Sidebar for configuration
with st.sidebar:
    st.header("Agent Configuration")
    
    # Mode selection
    st.subheader("Select Agent Mode")
    
    for mode, details in AGENT_MODES.items():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write(details["icon"])
        with col2:
            if st.button(mode, key=f"mode_{mode}"):
                # Reset conversation when changing modes
                if st.session_state.agent_mode != mode:
                    # Save current conversation to history
                    if st.session_state.messages:
                        st.session_state.history.append({
                            "mode": st.session_state.agent_mode,
                            "messages": st.session_state.messages.copy(),
                            "timestamp": datetime.now().isoformat()
                        })
                    
                    st.session_state.agent_mode = mode
                    st.session_state.messages = []
                    st.rerun()
    
    # Show description of current mode
    st.info(AGENT_MODES[st.session_state.agent_mode]["description"])
    
    st.divider()
    
    # API Key configuration
    st.subheader("Configuration")
    
    {% if provider == "Anthropic (Claude)" or provider == "Multiple providers" %}
    anthropic_key = st.text_input("Anthropic API Key", 
                                value=os.getenv("ANTHROPIC_API_KEY", ""), 
                                type="password")
    if anthropic_key:
        os.environ["ANTHROPIC_API_KEY"] = anthropic_key
    {% endif %}
    
    {% if provider == "Google (Gemini)" or provider == "Multiple providers" %}
    gemini_key = st.text_input("Google API Key", 
                             value=os.getenv("GOOGLE_API_KEY", ""), 
                             type="password")
    if gemini_key:
        os.environ["GOOGLE_API_KEY"] = gemini_key
    {% endif %}
    
    {% if provider == "LLM Local (Ollama)" or provider == "Multiple providers" %}
    ollama_url = st.text_input("Ollama URL", 
                            value=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
    if ollama_url:
        os.environ["OLLAMA_BASE_URL"] = ollama_url
        
    ollama_model = st.text_input("Ollama Model", 
                              value=os.getenv("OLLAMA_MODEL", "llama3"))
    if ollama_model:
        os.environ["OLLAMA_MODEL"] = ollama_model
    {% endif %}
    
    st.divider()
    
    # History and conversation management
    st.subheader("Conversation History")
    
    if st.button("New Conversation"):
        # Save current conversation to history
        if st.session_state.messages:
            st.session_state.history.append({
                "mode": st.session_state.agent_mode,
                "messages": st.session_state.messages.copy(),
                "timestamp": datetime.now().isoformat()
            })
        
        st.session_state.messages = []
        st.rerun()
    
    # Display conversation history
    if st.session_state.history:
        st.write("Previous conversations:")
        for i, conversation in enumerate(reversed(st.session_state.history[-5:])):  # Show only the last 5
            if st.button(f"{conversation['mode']} - {conversation['timestamp'][:16]}", key=f"history_{i}"):
                st.session_state.agent_mode = conversation['mode']
                st.session_state.messages = conversation['messages']
                st.rerun()

# Main chat area
st.subheader(f"Chat with {st.session_state.agent_mode} {AGENT_MODES[st.session_state.agent_mode]['icon']}")

# Display welcome message if no messages yet
if not st.session_state.messages:
    mode = st.session_state.agent_mode
    st.info(f"You're now chatting with the {mode} agent. {AGENT_MODES[mode]['description']}")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input(f"Ask the {st.session_state.agent_mode}...")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response based on current mode
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        response = get_agent_response(prompt, st.session_state.agent_mode)
        
        # Display the response
        message_placeholder.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Add tools panel based on agent mode
if st.session_state.agent_mode == "Technical Expert":
    with st.expander("Code Templates"):
        st.code("""
def example_function(param1, param2):
    """Example function template"""
    result = param1 + param2
    return result
        """, language="python")
        
        if st.button("Insert Python Template"):
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "Here's a Python function template:\n```python\ndef function_name(parameters):\n    \"\"\"Docstring explaining the function\"\"\"\n    # Function body\n    result = parameters\n    return result\n```"
            })
            st.rerun()

elif st.session_state.agent_mode == "Creative Writer":
    with st.expander("Writing Prompts"):
        prompts = [
            "Write a short story about a character who discovers an unusual ability",
            "Create a descriptive paragraph about a bustling marketplace",
            "Write dialogue between two characters with opposing viewpoints",
            "Develop a character profile for an antihero in a dystopian setting"
        ]
        
        for prompt in prompts:
            if st.button(prompt):
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.rerun()

elif st.session_state.agent_mode == "Research Assistant":
    with st.expander("Research Templates"):
        templates = [
            "Create an outline for a research paper on [TOPIC]",
            "Summarize the key points about [SUBJECT]",
            "What are the main arguments for and against [CONCEPT]?",
            "Create a literature review structure for [FIELD]"
        ]
        
        selected_template = st.selectbox("Select a template:", templates)
        topic = st.text_input("Enter your topic:")
        
        if topic and st.button("Use Template"):
            formatted_prompt = selected_template.replace("[TOPIC]", topic).replace("[SUBJECT]", topic).replace("[CONCEPT]", topic).replace("[FIELD]", topic)
            st.session_state.messages.append({"role": "user", "content": formatted_prompt})
            st.rerun()