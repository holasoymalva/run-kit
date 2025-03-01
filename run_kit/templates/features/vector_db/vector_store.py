"""
Vector database integration using ChromaDB for semantic search capabilities.
"""

import os
import json
import hashlib
import numpy as np
from typing import List, Dict, Any, Optional, Union, Tuple

# Check if ChromaDB is installed
try:
    import chromadb
    from chromadb.config import Settings
    HAS_CHROMADB = True
except ImportError:
    HAS_CHROMADB = False

class VectorDatabase:
    """
    A vector database for storing and retrieving document embeddings.
    """
    
    def __init__(self, collection_name: str = "documents", persist_directory: str = None):
        """
        Initialize the vector database.
        
        Args:
            collection_name: Name of the collection to store documents in
            persist_directory: Directory to persist the database to
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory or os.path.join("app", "data", "chromadb")
        self.client = None
        self.collection = None
        
        # Create the persist directory if it doesn't exist
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize the database
        self._initialize()
    
    def _initialize(self) -> None:
        """
        Initialize the database connection.
        """
        if not HAS_CHROMADB:
            print("ChromaDB is not installed. Install with: pip install chromadb")
            return
        
        try:
            self.client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create the collection
            try:
                self.collection = self.client.get_collection(self.collection_name)
                print(f"Loaded existing collection: {self.collection_name}")
            except ValueError:
                self.collection = self.client.create_collection(self.collection_name)
                print(f"Created new collection: {self.collection_name}")
        
        except Exception as e:
            print(f"Error initializing vector database: {str(e)}")
            self.client = None
            self.collection = None
    
    def is_available(self) -> bool:
        """
        Check if the vector database is available.
        
        Returns:
            bool: True if available, False otherwise
        """
        return HAS_CHROMADB and self.client is not None and self.collection is not None
    
    def add_texts(self, 
                 texts: List[str], 
                 metadatas: Optional[List[Dict[str, Any]]] = None,
                 ids: Optional[List[str]] = None,
                 embeddings: Optional[List[List[float]]] = None) -> List[str]:
        """
        Add texts to the vector database.
        
        Args:
            texts: List of text chunks to add
            metadatas: Optional list of metadata dictionaries for each text
            ids: Optional list of IDs for each text
            embeddings: Optional list of pre-computed embeddings
            
        Returns:
            List[str]: The IDs of the added texts
        """
        if not self.is_available():
            print("Vector database is not available")
            return []
        
        # Generate IDs if not provided
        if ids is None:
            ids = [hashlib.md5(text.encode()).hexdigest() for text in texts]
        
        # Generate metadata if not provided
        if metadatas is None:
            metadatas = [{} for _ in texts]
        
        # Add to the collection
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )
        
        return ids
    
    def search(self, 
              query: str, 
              n_results: int = 5,
              where: Optional[Dict[str, Any]] = None,
              embedding: Optional[List[float]] = None) -> Dict[str, Any]:
        """
        Search for similar texts in the database.
        
        Args:
            query: The search query
            n_results: Number of results to return
            where: Optional filtering criteria
            embedding: Optional pre-computed query embedding
            
        Returns:
            Dict[str, Any]: Search results with 'documents', 'metadatas', 'distances', and 'ids'
        """
        if not self.is_available():
            print("Vector database is not available")
            return {
                "documents": [],
                "metadatas": [],
                "distances": [],
                "ids": []
            }
        
        results = self.collection.query(
            query_texts=[query] if embedding is None else None,
            query_embeddings=[embedding] if embedding is not None else None,
            n_results=n_results,
            where=where
        )
        
        return results
    
    def get(self, ids: List[str]) -> Dict[str, Any]:
        """
        Get documents by their IDs.
        
        Args:
            ids: List of document IDs
            
        Returns:
            Dict[str, Any]: The documents with 'documents', 'metadatas', and 'ids'
        """
        if not self.is_available():
            print("Vector database is not available")
            return {
                "documents": [],
                "metadatas": [],
                "ids": []
            }
        
        return self.collection.get(ids=ids)
    
    def delete(self, ids: List[str]) -> None:
        """
        Delete documents by their IDs.
        
        Args:
            ids: List of document IDs to delete
        """
        if not self.is_available():
            print("Vector database is not available")
            return
        
        self.collection.delete(ids=ids)
    
    def count(self) -> int:
        """
        Get the count of documents in the collection.
        
        Returns:
            int: Number of documents
        """
        if not self.is_available():
            print("Vector database is not available")
            return 0
        
        return self.collection.count()

# Singleton instance
vector_db = VectorDatabase()