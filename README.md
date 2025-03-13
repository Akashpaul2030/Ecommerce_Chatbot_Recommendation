# E-Commerce RAG Recommendation System

A complete solution for building an intelligent e-commerce product recommendation system with Retrieval-Augmented Generation (RAG) capabilities. This system enhances product search and recommendations by combining semantic understanding of user queries with structured product data.

## Features

- **Natural Language Search**: Users can query products using natural language (e.g., "Show me white shirts under 600 rupees")
- **Intelligent Filtering**: Automatically extracts filters from queries (price ranges, colors, product types)
- **Semantic Matching**: Uses vector embeddings to find relevant products based on meaning, not just keywords
- **Interactive Chat Interface**: Chat-based shopping assistant to help users find products
- **Responsive UI**: Clean, modern interface that works on desktop and mobile devices
- **Structured Architecture**: Clear separation between frontend and backend components

## Architecture

The system follows a modern, scalable architecture:

### Backend

- **Data Processing Layer**: Handles parsing and cleaning of product data
- **Vector Database**: Manages product embeddings for semantic search
- **RAG Engine**: Integrates LLM with product data for enhanced recommendations
- **RESTful API**: Provides endpoints for the frontend to query

### Frontend 

- **React Components**: Modular UI components for product display, filtering, and chat
- **State Management**: Efficient handling of application state
- **API Service**: Communicates with backend API endpoints
- **Responsive Design**: Adapts to different screen sizes

## Setup and Installation

### Prerequisites

- Python 3.8+
- Node.js 14+
- Pip and npm package managers

### Backend Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ecommerce-rag.git
   cd ecommerce-rag
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install backend dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your product data:
   ```
   mkdir -p data
   cp path/to/your/products.tsv data/
   ```

5. Start the backend server:
   ```
   cd backend
   uvicorn api.app:app --reload
   ```

### Frontend Setup

1. Install frontend dependencies:
   ```
   cd frontend
   npm install
   ```

2. Configure the environment:
   ```
   cp .env.example .env
   ```
   Edit `.env` to set the backend API URL.

3. Start the development server:
   ```
   npm start
   ```

## Using Melvus Integration

This project supports integration with the Melvus library for enhanced RAG capabilities:

1. Install Melvus:
   ```
   pip install melvus
   ```

2. Import in your code:
   ```python
   from melvus import RAG, Document, VectorDB
   ```

3. Use the provided `MelvusProductRAG` class for easy integration:
   ```python
   from melvus_integration import MelvusProductRAG
   
   # Initialize with your product data
   rag_system = MelvusProductRAG("product_data.tsv")
   
   # Process user queries
   results = rag_system.process_query("I'm looking for a white shirt under 600 rupees")
   ```

## API Endpoints

The backend provides the following RESTful API endpoints:

- `GET /products`: Retrieve a list of products with pagination
- `GET /products/{product_id}`: Get a specific product by ID
- `POST /query`: Search for products using natural language
- `GET /filters`: Get available filtering options (brands, categories, price ranges)

## Project Structure

```
ecommerce_rag/
├── backend/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── data_processor.py
│   │   └── product_catalog.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── vector_store.py
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── embeddings.py
│   │   └── retriever.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── routes.py
│   └── utils/
│       ├── __init__.py
│       └── query_parser.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── ProductCard.jsx
│   │   │   └── SearchFilters.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── pages/
│   │   │   └── Home.jsx
│   │   ├── App.jsx
│   │   └── index.jsx
│   ├── package.json
│   └── README.md
├── config.py
├── requirements.txt
├── setup.py
└── README.md
```

## Customization

### Adding New Product Data

1. Prepare your product data in TSV format with the following columns:
   - `uniq_id`: Unique identifier for each product
   - `product_name`: Name of the product
   - `product_category_tree`: Category hierarchy in JSON format
   - `retail_price`: Original price
   - `discounted_price`: Sale price
   - `description`: Product description
   - `brand`: Brand name
   - `image`: Image URLs in JSON format
   - `product_specifications`: Product attributes in JSON format

2. Place your data file in the `data/` directory.

3. Update the data path in the configuration:
   ```python
   # config.py
   PRODUCT_DATA_PATH = "data/your_new_data.tsv"
   ```

### Enhancing the Embedding Model

For production use, replace the simple TF-IDF vectorizer with a more powerful embedding model:

1. Install sentence-transformers:
   ```
   pip install sentence-transformers
   ```

2. Update the `EmbeddingService` class:
   ```python
   from sentence_transformers import SentenceTransformer

   class EmbeddingService:
       def __init__(self, model_name="all-MiniLM-L6-v2"):
           self.model = SentenceTransformer(model_name)
       
       def embed_text(self, text):
           return self.model.encode(text)
   ```

## Performance Considerations

- For large product catalogs (>10,000 products), consider using an optimized vector database like FAISS, Pinecone, or Qdrant
- Implement caching for frequently accessed products and queries
- For production deployments, use a WSGI server like Gunicorn with multiple workers

## Deployment

### Backend Deployment

The backend can be deployed to any cloud provider that supports Python applications:

1. Build a Docker container:
   ```
   docker build -t ecommerce-rag-backend .
   ```

2. Deploy to your preferred cloud provider (AWS, Google Cloud, Azure, etc.)

### Frontend Deployment

1. Build the production frontend:
   ```
   cd frontend
   npm run build
   ```

2. Deploy the static files to a CDN or static hosting service (Netlify, Vercel, AWS S3, etc.)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Product data sourced from Flipkart dataset
- Uses Melvus for RAG capabilities
- Built with FastAPI and React