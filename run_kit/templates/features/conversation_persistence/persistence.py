"""
Conversation persistence system to save and load conversation history.
"""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

# Conversations directory
CONVERSATIONS_DIR = os.path.join("app", "data", "conversations")
os.makedirs(CONVERSATIONS_DIR, exist_ok=True)

class ConversationStore:
    """
    A system for persisting conversation history.
    """
    
    def __init__(self, storage_dir: str = CONVERSATIONS_DIR):
        """
        Initialize the conversation store.
        
        Args:
            storage_dir: Directory to store conversation files
        """
        self.storage_dir = storage_dir
    
    def save_conversation(self, 
                         messages: List[Dict[str, str]], 
                         conversation_id: Optional[str] = None, 
                         metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Save a conversation history to disk.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            conversation_id: Optional ID for the conversation, generated if not provided
            metadata: Optional metadata to store with the conversation
            
        Returns:
            str: The conversation ID
        """
        # Generate ID if not provided
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        
        # Create metadata if not provided
        if metadata is None:
            metadata = {}
        
        # Add timestamp if not present
        if "timestamp" not in metadata:
            metadata["timestamp"] = datetime.now().isoformat()
        
        # Prepare conversation data
        conversation_data = {
            "id": conversation_id,
            "messages": messages,
            "metadata": metadata
        }
        
        # Save to file
        file_path = os.path.join(self.storage_dir, f"{conversation_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(conversation_data, f, ensure_ascii=False, indent=2)
        
        return conversation_id
    
    def load_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """
        Load a conversation history from disk.
        
        Args:
            conversation_id: The ID of the conversation to load
            
        Returns:
            Optional[Dict[str, Any]]: The conversation data or None if not found
        """
        file_path = os.path.join(self.storage_dir, f"{conversation_id}.json")
        
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading conversation: {str(e)}")
            return None
    
    def list_conversations(self, limit: int = 20, sort_by_date: bool = True) -> List[Dict[str, Any]]:
        """
        List available conversations.
        
        Args:
            limit: Maximum number of conversations to return
            sort_by_date: Whether to sort by date (newest first)
            
        Returns:
            List[Dict[str, Any]]: List of conversation metadata
        """
        conversations = []
        
        for filename in os.listdir(self.storage_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(self.storage_dir, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        conv_data = json.load(f)
                        # Extract just the metadata for the listing
                        conversations.append({
                            "id": conv_data.get("id"),
                            "metadata": conv_data.get("metadata", {}),
                            "message_count": len(conv_data.get("messages", [])),
                            "file_path": file_path
                        })
                except Exception as e:
                    print(f"Error reading conversation file {filename}: {str(e)}")
        
        # Sort by date if requested
        if sort_by_date and conversations:
            conversations.sort(
                key=lambda x: x.get("metadata", {}).get("timestamp", ""),
                reverse=True
            )
        
        # Apply limit
        return conversations[:limit]
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """
        Delete a conversation.
        
        Args:
            conversation_id: The ID of the conversation to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        file_path = os.path.join(self.storage_dir, f"{conversation_id}.json")
        
        if not os.path.exists(file_path):
            return False
        
        try:
            os.remove(file_path)
            return True
        except Exception as e:
            print(f"Error deleting conversation: {str(e)}")
            return False


# Singleton instance
conversation_store = ConversationStore()