from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import os

from ..data.data_processor import DataProcessor
from ..data.product_catalog import ProductCatalog, Product
from ..database.vector_store import VectorStore
from ..rag.embeddings import EmbeddingService
from ..rag.retriever import ProductRetriever


class QueryRequest(BaseModel):
    """Request model for product query"""
    query: str
    top_k: Optional[int] = 5
    filters: Optional[Dict[str, Any]] = None


class ProductResponse(BaseModel):
    """Response model for product data"""
    id: str
    name: str
    brand: str
    category: str
    price: float
    discounted_price: float
    description: str
    image_urls: List[str]
    specifications: Dict[str, Any]


class QueryResponse(BaseModel):
    """Response model for query results"""
    products: List[ProductResponse]
    explanation: Dict[str, Any]


# Initialize components
data_path = os.getenv("PRODUCT_DATA_PATH", "data/paste.txt")
processor = DataProcessor(data_path)
catalog = ProductCatalog()
embedding_service = EmbeddingService()
vector_store = VectorStore()

# Create FastAPI app
app = FastAPI(title="E-Commerce RAG API", version="1.0.0")

# Add CORS middleware to allow cross-origin requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global retriever reference
retriever = None

@app.on_event("startup")
async def startup_event():
    """Initialize data and components on startup"""
    global retriever
    
    try:
        # Load and process data
        print("Loading product data...")
        df = processor.load_from_tsv()
        catalog.load_from_dataframe(processor.clean_dataframe())
        print(f"Loaded {len(catalog.products)} products")
        
        # Initialize retriever
        retriever = ProductRetriever(catalog, vector_store, embedding_service)
        
        # Initialize vectorizer with sample texts
        sample_texts = [
            "product search ecommerce",
            "clothing furniture electronics",
            "price color size brand"
        ]
        
        # Add product descriptions to sample texts if available
        if catalog.products:
            for product in catalog.products[:10]:  # Use first 10 products
                sample_texts.append(embedding_service.get_product_text(product))
        
        # Fit the embedding service
        embedding_service.fit(sample_texts)
        print("Vectorizer initialized successfully")
        
        # Index products
        print("Indexing products...")
        retriever.index_products()
        print("Product indexing complete")
    except Exception as e:
        print(f"Error during initialization: {e}")
        import traceback
        traceback.print_exc()


@app.get("/")
def read_root():
    """Root endpoint"""
    return {"message": "E-Commerce RAG API is running"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "products_loaded": len(catalog.products),
        "vectorizer_fitted": embedding_service.is_fitted
    }


@app.get("/products", response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 10):
    """Get a list of products with pagination"""
    products = catalog.products[skip:skip+limit]
    return [ProductResponse(**product.to_dict()) for product in products]


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: str):
    """Get a specific product by ID"""
    product = catalog.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse(**product.to_dict())


@app.post("/query", response_model=QueryResponse)
def query_products(request: QueryRequest):
    """Query for products using natural language"""
    if not retriever:
        raise HTTPException(status_code=500, detail="Retriever not initialized")
    
    try:
        # Apply any additional filters from the request
        additional_filters = request.filters or {}
        
        # Retrieve products based on the query
        products, explanation = retriever.retrieve(request.query, top_k=request.top_k)
        
        # Convert products to response format
        product_responses = [ProductResponse(**product.to_dict()) for product in products]
        
        return QueryResponse(products=product_responses, explanation=explanation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/filters")
def get_filters():
    """Get available filtering options"""
    return {
        "brands": catalog.get_all_brands(),
        "categories": catalog.get_all_categories(),
        "price_range": catalog.get_price_range()
    }