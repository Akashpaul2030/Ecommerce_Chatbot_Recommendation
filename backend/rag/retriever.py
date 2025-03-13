from typing import List, Dict, Any, Optional, Tuple
import re
from ..data.product_catalog import Product, ProductCatalog
from ..database.vector_store import VectorStore
from .embeddings import EmbeddingService


class QueryParser:
    """
    Parses natural language queries to extract structured filtering criteria.
    """
    
    def extract_filters(self, query: str) -> Dict[str, Any]:
        """Extract filtering criteria from a natural language query"""
        filters = {}
        
        # Extract price range filters
        price_pattern = r'under\s+(\d+)'
        price_matches = re.search(price_pattern, query)
        if price_matches:
            filters['max_price'] = float(price_matches.group(1))
        
        # Extract min price
        min_price_pattern = r'over\s+(\d+)'
        min_price_matches = re.search(min_price_pattern, query)
        if min_price_matches:
            filters['min_price'] = float(min_price_matches.group(1))
        
        # Extract price range with 'between X and Y'
        price_range_pattern = r'between\s+(\d+)\s+and\s+(\d+)'
        price_range_matches = re.search(price_range_pattern, query)
        if price_range_matches:
            filters['min_price'] = float(price_range_matches.group(1))
            filters['max_price'] = float(price_range_matches.group(2))
        
        # Extract colors (predefined list of common colors)
        colors = ['white', 'black', 'red', 'blue', 'green', 'yellow', 
                 'purple', 'pink', 'orange', 'brown', 'grey', 'gray', 'navy']
        for color in colors:
            if color in query.lower():
                filters['color'] = color
                break
        
        return filters


class ProductRetriever:
    """
    RAG retrieval system for finding products based on user queries.
    """
    
    def __init__(self, catalog: ProductCatalog, vector_store: VectorStore, embedding_service: EmbeddingService):
        """Initialize the retriever with required components"""
        self.catalog = catalog
        self.vector_store = vector_store
        self.embedding_service = embedding_service
        self.query_parser = QueryParser()
    
    def index_products(self) -> None:
        """Create embeddings for all products and add them to the vector store"""
        # Create embeddings for all products
        product_embeddings = self.embedding_service.embed_products(self.catalog.products)
        
        # Add embeddings to the vector store
        for product_id, embedding in product_embeddings.items():
            self.vector_store.add_embedding(product_id, embedding)
    
    def retrieve(self, query: str, top_k: int = 5) -> Tuple[List[Product], Dict[str, Any]]:
        """
        Retrieve products relevant to the query.
        Returns a tuple of (products, explanation).
        """
        # Extract filters from the query
        filters = self.query_parser.extract_filters(query)
        
        # Filter products based on extracted criteria
        filtered_products = self.catalog.filter_products(
            min_price=filters.get('min_price'),
            max_price=filters.get('max_price'),
            color=filters.get('color')
        )
        
        # Create an embedding for the query
        query_embedding = self.embedding_service.embed_text(query)
        
        # If we have filtered products, search within them
        if filtered_products:
            # Create a temporary vector store for the filtered products
            temp_store = VectorStore(embedding_dim=query_embedding.shape[0])
            
            # Add embeddings for filtered products
            for product in filtered_products:
                embedding = self.vector_store.get_embedding(product.id)
                if embedding is not None:
                    temp_store.add_embedding(product.id, embedding)
            
            # Search for the most relevant products
            results = temp_store.search(query_embedding, top_k=top_k)
        else:
            # Search across all products
            results = self.vector_store.search(query_embedding, top_k=top_k)
        
        # Convert results to product objects
        products = []
        for product_id, score in results:
            product = self.catalog.get_product_by_id(product_id)
            if product:
                products.append(product)
        
        # Generate explanation
        explanation = self._generate_explanation(query, filters, products)
        
        return products, explanation
    
    def _generate_explanation(self, query: str, filters: Dict[str, Any], products: List[Product]) -> Dict[str, Any]:
        """Generate an explanation for the recommendation"""
        filter_descriptions = []
        
        if 'min_price' in filters:
            filter_descriptions.append(f"price over {filters['min_price']}")
            
        if 'max_price' in filters:
            filter_descriptions.append(f"price under {filters['max_price']}")
            
        if 'color' in filters:
            filter_descriptions.append(f"color {filters['color']}")
        
        explanation = {
            "query": query,
            "filters_applied": filters,
            "filter_description": " and ".join(filter_descriptions) if filter_descriptions else None,
            "num_results": len(products),
            "results_summary": f"Found {len(products)} products matching your criteria" if products else "No matching products found"
        }
        
        return explanation
