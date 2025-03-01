"""
{{ project_name }} - AI Application
Generated with RunKit
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="{{ project_name }}",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open("app/styles/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# App title
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
        
        # Import the appropriate LLM based on provider
        {% if provider == "Anthropic (Claude)" %}
        from app.llm.client import get_anthropic_response
        response = get_anthropic_response(prompt)
        {% elif provider == "Google (Gemini)" %}
        from app.llm.client import get_gemini_response
        response = get_gemini_response(prompt)
        {% elif provider == "LLM Local (Ollama)" %}
        from app.llm.client import get_ollama_response
        response = get_ollama_response(prompt)
        {% else %}
        # Multiple providers
        from app.llm.client import get_response
        response = get_response(prompt)
        {% endif %}
        
        # Display the response
        message_placeholder.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This is an AI assistant app generated with RunKit.
    
    The application uses:
    - {{ provider }}
    {% for feature in features %}
    - {{ feature }}
    {% endfor %}
    
    Project type: {{ project_type }}
    """)
    
    st.divider()
    
    # API Key configuration section
    st.subheader("Configuration")
    
    {% if provider == "Anthropic (Claude)" %}
    anthropic_key = st.text_input("Anthropic API Key", 
                                  value=os.getenv("ANTHROPIC_API_KEY", ""), 
                                  type="password")
    if anthropic_key:
        os.environ["ANTHROPIC_API_KEY"] = anthropic_key
    {% elif provider == "Google (Gemini)" %}
    gemini_key = st.text_input("Google API Key", 
                               value=os.getenv("GOOGLE_API_KEY", ""), 
                               type="password")
    if gemini_key:
        os.environ["GOOGLE_API_KEY"] = gemini_key
    {% endif %}
    
    # Reset conversation button
    if st.button("Reset Conversation"):
        st.session_state.messages = []
        st.rerun()