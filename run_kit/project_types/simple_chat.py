"""
{{ project_name }} - Simple Chat AI Application
Generated with RunKit
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# CRITICAL: set_page_config MUST be the first Streamlit call
st.set_page_config(
    page_title="{{ project_name }}",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
st.title("{{ project_name }}")
st.markdown("#### *Your AI assistant powered by {{ provider }}*")

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
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Placeholder response
        response = f"This is a placeholder response. To get actual AI responses, please configure the {{ provider }} integration."
        
        # Display the response
        message_placeholder.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar
with st.sidebar:
    st.header("{{ project_name }}")
    st.markdown("""
    This is a simple AI chat application generated with RunKit.
    
    The application uses:
    - {{ provider }}
    {% for feature in features %}
    - {{ feature }}
    {% endfor %}
    """)
    
    st.divider()
    
    # API Key configuration section
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
    
    # Reset conversation button
    if st.button("Reset Conversation"):
        st.session_state.messages = []
        st.rerun()