# D:\Ecommerce_Chatbot_Recommendation\backend\database\vector_store.py
import numpy as np
from typing import List, Dict, Any, Optional, Tuple

class VectorStore:
    """
    Vector database for storing and retrieving product embeddings.
    """
    
    def __init__(self, embedding_dim: int = 768):
        """Initialize the vector store with a specified embedding dimension"""
        self.embedding_dim = embedding_dim
        self.embeddings: Dict[str, np.ndarray] = {}  # product_id -> embedding
        self.product_ids: List[str] = []
        self.embedding_matrix: Optional[np.ndarray] = None
    
    def add_embedding(self, product_id: str, embedding: np.ndarray) -> None:
        """Add a product embedding to the vector store"""
        if embedding.shape[0] != self.embedding_dim:
            raise ValueError(f"Embedding dimension mismatch: expected {self.embedding_dim}, got {embedding.shape[0]}")
        
        self.embeddings[product_id] = embedding
        if product_id not in self.product_ids:
            self.product_ids.append(product_id)
        
        # Invalidate the embedding matrix since we've added a new embedding
        self.embedding_matrix = None
    
    def get_embedding(self, product_id: str) -> Optional[np.ndarray]:
        """Get the embedding for a specific product"""
        return self.embeddings.get(product_id)