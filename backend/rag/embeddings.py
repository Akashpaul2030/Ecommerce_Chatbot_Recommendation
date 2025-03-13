import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer

# In a production environment, you would use a more sophisticated embedding model
# such as sentence-transformers, but for simplicity we use TF-IDF here


class EmbeddingService:
    """
    Service for creating text embeddings for products and queries.
    In a real-world scenario, this would use a pre-trained language model.
    """
    
    def __init__(self, max_features: int = 5000):
        """Initialize the embedding service"""
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=max_features
        )
        self.is_fitted = False
    
    def fit(self, texts: List[str]) -> None:
        """Fit the vectorizer on a corpus of texts"""
        self.vectorizer.fit(texts)
        self.is_fitted = True
    
    def get_product_text(self, product: 'Product') -> str:
        """Create a text representation of a product for embedding"""
        parts = [
            product.name,
            product.brand,
            product.category,
            product.description
        ]
        
        # Add key specifications
        for key, value in product.specifications.items():
            parts.append(f"{key}: {value}")
        
        return " ".join(filter(None, parts))
    
    def embed_product(self, product: 'Product') -> np.ndarray:
        """Create an embedding for a product"""
        product_text = self.get_product_text(product)
        return self.embed_text(product_text)
    
    def embed_text(self, text: str) -> np.ndarray:
        """Create an embedding for a text string"""
        if not self.is_fitted:
            # Auto-fit on this text if not fitted yet
            self.fit([text])
            self.is_fitted = True
            print("Vectorizer has been automatically fitted on the query text")
        
        # Get the TF-IDF vector
        vector = self.vectorizer.transform([text])
        
        # Convert to dense numpy array
        return vector.toarray()[0]
    
    def embed_products(self, products: List['Product']) -> Dict[str, np.ndarray]:
        """Create embeddings for a list of products"""
        # First, create text representations for all products
        product_texts = [self.get_product_text(p) for p in products]
        
        # Fit the vectorizer if not already fitted
        if not self.is_fitted:
            self.fit(product_texts)
        
        # Create embeddings for all products
        vectors = self.vectorizer.transform(product_texts)
        
        # Convert to dictionary of product_id -> embedding
        embeddings = {}
        for i, product in enumerate(products):
            embeddings[product.id] = vectors[i].toarray()[0]
        
        return embeddings