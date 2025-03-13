from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json
import re
import pandas as pd


@dataclass
class Product:
    """Product data structure with all relevant e-commerce attributes"""
    id: str
    name: str
    category: str = ""
    price: float = 0.0
    discounted_price: float = 0.0
    description: str = ""
    brand: str = ""
    specifications: Dict[str, Any] = field(default_factory=dict)
    image_urls: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert product to dictionary representation"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'discounted_price': self.discounted_price,
            'description': self.description,
            'brand': self.brand,
            'specifications': self.specifications,
            'image_urls': self.image_urls
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """Create a Product from a dictionary"""
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            category=data.get('category', ''),
            price=float(data.get('price', 0)),
            discounted_price=float(data.get('discounted_price', 0)),
            description=data.get('description', ''),
            brand=data.get('brand', ''),
            specifications=data.get('specifications', {}),
            image_urls=data.get('image_urls', [])
        )
    
    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> 'Product':
        """Create a Product from a DataFrame row"""
        # Parse product_category_tree to extract the main category
        category = ""
        if row.get('product_category_tree'):
            try:
                category_tree = json.loads(row['product_category_tree'].replace("'", '"'))
                if category_tree and len(category_tree) > 0:
                    category = category_tree[0]
            except (json.JSONDecodeError, TypeError):
                pass
        
        # Parse specifications
        specs = {}
        if row.get('product_specifications'):
            try:
                # Extract key-value pairs using regex
                pattern = r'\"key\"=>\"([^\"]+)\",\s*\"value\"=>\"([^\"]+)\"'
                matches = re.findall(pattern, row['product_specifications'])
                specs = {k: v for k, v in matches}
            except Exception:
                pass
        
        # Parse image URLs
        image_urls = []
        if row.get('image'):
            try:
                image_urls = json.loads(row['image'].replace("'", '"'))
            except (json.JSONDecodeError, TypeError):
                pass
        
        return cls(
            id=row.get('uniq_id', ''),
            name=row.get('product_name', ''),
            category=category,
            price=float(row.get('retail_price', 0)),
            discounted_price=float(row.get('discounted_price', 0)),
            description=row.get('description', ''),
            brand=row.get('brand', ''),
            specifications=specs,
            image_urls=image_urls
        )


class ProductCatalog:
    """
    Manages the collection of products and provides filtering/search capabilities.
    """
    
    def __init__(self):
        """Initialize an empty product catalog"""
        self.products: List[Product] = []
        self._id_to_product: Dict[str, Product] = {}
        self._brand_to_products: Dict[str, List[Product]] = {}
        self._category_to_products: Dict[str, List[Product]] = {}
    
    def add_product(self, product: Product) -> None:
        """Add a product to the catalog"""
        self.products.append(product)
        self._id_to_product[product.id] = product
        
        # Index by brand
        brand = product.brand.lower()
        if brand not in self._brand_to_products:
            self._brand_to_products[brand] = []
        self._brand_to_products[brand].append(product)
        
        # Index by category
        if product.category:
            main_category = product.category.split('>>')[0].strip().lower()
            if main_category not in self._category_to_products:
                self._category_to_products[main_category] = []
            self._category_to_products[main_category].append(product)
    
    def load_from_dataframe(self, df: pd.DataFrame) -> None:
        """Load products from a pandas DataFrame"""
        for _, row in df.iterrows():
            try:
                product = Product.from_row(row)
                self.add_product(product)
            except Exception as e:
                print(f"Error processing product: {e}")
    
    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """Get a product by its ID"""
        return self._id_to_product.get(product_id)
    
    def get_products_by_brand(self, brand: str) -> List[Product]:
        """Get all products from a specific brand"""
        return self._brand_to_products.get(brand.lower(), [])
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """Get all products in a specific category"""
        return self._category_to_products.get(category.lower(), [])
    
    def filter_products(self,
                       min_price: Optional[float] = None,
                       max_price: Optional[float] = None,
                       brand: Optional[str] = None,
                       category: Optional[str] = None,
                       color: Optional[str] = None) -> List[Product]:
        """Filter products based on multiple criteria"""
        filtered = self.products.copy()
        
        if min_price is not None:
            filtered = [p for p in filtered if p.discounted_price >= min_price]
            
        if max_price is not None:
            filtered = [p for p in filtered if p.discounted_price <= max_price]
            
        if brand is not None:
            filtered = [p for p in filtered if brand.lower() in p.brand.lower()]
        
        if category is not None:
            filtered = [p for p in filtered if category.lower() in p.category.lower()]
            
        if color is not None:
            # Check both product name and description for color
            filtered = [p for p in filtered 
                      if color.lower() in p.name.lower() 
                      or color.lower() in p.description.lower()]
            
        return filtered
    
    def get_all_brands(self) -> List[str]:
        """Get a list of all brands in the catalog"""
        return list(self._brand_to_products.keys())
    
    def get_all_categories(self) -> List[str]:
        """Get a list of all categories in the catalog"""
        return list(self._category_to_products.keys())
    
    def get_price_range(self) -> Dict[str, float]:
        """Get the min and max price in the catalog"""
        if not self.products:
            return {"min": 0, "max": 0}
        
        min_price = min(p.discounted_price for p in self.products)
        max_price = max(p.discounted_price for p in self.products)
        
        return {"min": min_price, "max": max_price}


# backend/database/vector_store.py
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from ..data.product_catalog import Product


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
    
    def get_embedding_matrix(self) -> np.ndarray:
        """Get the matrix of all embeddings for efficient similarity search"""
        if self.embedding_matrix is None:
            # Create the embedding matrix on demand
            self.embedding_matrix = np.zeros((len(self.product_ids), self.embedding_dim))
            for i, product_id in enumerate(self.product_ids):
                self.embedding_matrix[i] = self.embeddings[product_id]
        
        return self.embedding_matrix
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Search for the most similar products to the query embedding.
        Returns a list of (product_id, similarity_score) tuples.
        """
        if len(self.product_ids) == 0:
            return []
        
        # Get the embedding matrix
        embedding_matrix = self.get_embedding_matrix()
        
        # Normalize the query embedding
        query_norm = np.linalg.norm(query_embedding)
        if query_norm > 0:
            query_embedding = query_embedding / query_norm
        
        # Normalize the embedding matrix
        norms = np.linalg.norm(embedding_matrix, axis=1, keepdims=True)
        normalized_embeddings = np.divide(embedding_matrix, norms, where=norms>0)
        
        # Compute cosine similarities
        similarities = np.dot(normalized_embeddings, query_embedding)
        
        # Get the top-k most similar products
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Return the product IDs and similarity scores
        results = []
        for idx in top_indices:
            product_id = self.product_ids[idx]
            score = float(similarities[idx])
            results.append((product_id, score))
        
        return results
