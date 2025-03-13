// frontend/src/pages/Home.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Home = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch products from your backend
    const fetchProducts = async () => {
      try {
        const response = await axios.get('http://localhost:8000/products');
        setProducts(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch products');
        setLoading(false);
        console.error(err);
      }
    };

    fetchProducts();
  }, []);

  if (loading) return <div>Loading products...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="home-container">
      <h1>E-Commerce RAG Recommendation System</h1>
      
      <div className="product-search">
        <input 
          type="text" 
          placeholder="Search for products..." 
        />
        <button>Search</button>
      </div>
      
      <div className="products-list">
        <h2>Products</h2>
        {products.length === 0 ? (
          <p>No products found</p>
        ) : (
          <ul>
            {products.map(product => (
              <li key={product.id}>
                <h3>{product.name}</h3>
                <p>Price: ₹{product.discounted_price}</p>
                <p>{product.description.substring(0, 100)}...</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default Home;