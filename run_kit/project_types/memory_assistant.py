"""
{{ project_name }} - Memory Enhanced AI Assistant
Generated with RunKit
"""

import streamlit as st
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# CRITICAL: set_page_config MUST be the first Streamlit call
st.set_page_config(
    page_title="{{ project_name }} - Memory Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "memory" not in st.session_state:
    st.session_state.memory = {}
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None
if "current_topic" not in st.session_state:
    st.session_state.current_topic = "General"

# App title and description
st.title("{{ project_name }}")
st.markdown("#### *Memory-Enhanced AI Assistant powered by {{ provider }}*")

# Safe imports - after st.set_page_config
def load_llm_client():
    """Safely load the LLM client"""
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

# Load additional modules safely
llm_client = load_llm_client()

# Helper functions for memory management
def save_memory(topic: str, information: str):
    """Save information to a specific topic in memory"""
    if topic not in st.session_state.memory:
        st.session_state.memory[topic] = []
    
    # Add timestamp and information
    memory_item = {
        "timestamp": datetime.now().isoformat(),
        "information": information
    }
    
    st.session_state.memory[topic].append(memory_item)

def get_memory_for_topic(topic: str) -> str:
    """Get all memory items for a specific topic"""
    if topic not in st.session_state.memory:
        return "No information stored on this topic."
    
    memory_items = st.session_state.memory[topic]
    result = f"Memory for '{topic}':\n\n"
    
    for item in memory_items:
        timestamp = datetime.fromisoformat(item["timestamp"]).strftime("%Y-%m-%d %H:%M")
        result += f"• {timestamp}: {item['information']}\n\n"
    
    return result

def get_relevant_memories(query: str) -> str:
    """Get all memories that might be relevant to the query"""
    if not st.session_state.memory:
        return ""
    
    # In a real implementation, this would use semantic search
    # For simplicity, we'll just return the current topic's memories
    return get_memory_for_topic(st.session_state.current_topic)

# Layout - sidebar first for topic selection
with st.sidebar:
    st.header("Memory Topics")
    
    # Topic selection/creation
    new_topic = st.text_input("Create New Topic")
    if new_topic and st.button("Add Topic"):
        if new_topic not in st.session_state.memory:
            st.session_state.memory[new_topic] = []
            st.session_state.current_topic = new_topic
            st.rerun()
    
    # Display existing topics
    st.subheader("Select Topic")
    topics = list(st.session_state.memory.keys())
    if not topics:
        topics = ["General"]
        st.session_state.memory["General"] = []
    
    for topic in topics:
        if st.button(f"📁 {topic}", key=f"topic_{topic}"):
            st.session_state.current_topic = topic
            st.rerun()
    
    st.divider()
    
    # Display current topic memory
    st.subheader(f"Current Topic: {st.session_state.current_topic}")
    
    # View memory button
    if st.button("View Memory"):
        memory_content = get_memory_for_topic(st.session_state.current_topic)
        st.session_state.messages.append({
            "role": "assistant", 
            "content": memory_content
        })
        st.rerun()
    
    # Clear memory button
    if st.button("Clear Topic Memory"):
        if st.session_state.current_topic in st.session_state.memory:
            st.session_state.memory[st.session_state.current_topic] = []
            st.rerun()
    
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
    
    # Reset conversation
    if st.button("New Conversation"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.subheader(f"Chat - {st.session_state.current_topic}")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input(f"Ask about {st.session_state.current_topic}...")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Get relevant memories
        memories = get_relevant_memories(prompt)
        
        # Build prompt with memories
        enhanced_prompt = f"""
        Current topic: {st.session_state.current_topic}
        
        Previous information about this topic:
        {memories}
        
        User question: {prompt}
        
        Use the previous information when relevant to provide a more helpful response.
        """
        
        # Get response from LLM
        try:
            response = llm_client(enhanced_prompt)
        except Exception as e:
            response = f"I'm having trouble connecting to the AI service. Error: {str(e)}"
        
        # Display the response
        message_placeholder.markdown(response)
        
        # Extract potentially useful information to remember
        memory_prompt = f"""
        Given the user question: '{prompt}'
        And your response: '{response}'
        
        Is there any key information worth remembering for future reference?
        If yes, extract only that information as concise bullet points.
        If no, respond with 'No key information to remember.'
        """
        
        try:
            memory_extraction = llm_client(memory_prompt)
            if "No key information to remember" not in memory_extraction:
                save_memory(st.session_state.current_topic, memory_extraction)
        except:
            # Silently fail if memory extraction fails
            pass
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})