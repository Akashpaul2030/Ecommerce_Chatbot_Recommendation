import axios from 'axios';

// API base URL - adjust this to match your backend deployment
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API service methods
export const productService = {
  // Get products with pagination
  async getProducts(skip = 0, limit = 10) {
    try {
      const response = await apiClient.get(`/products?skip=${skip}&limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching products:', error);
      throw error;
    }
  },

  // Get a specific product by ID
  async getProductById(productId) {
    try {
      const response = await apiClient.get(`/products/${productId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching product:', error);
      throw error;
    }
  },

  // Query products with natural language
  async queryProducts(query, topK = 5, filters = {}) {
    try {
      const response = await apiClient.post('/query', {
        query,
        top_k: topK,
        filters
      });
      return response.data;
    } catch (error) {
      console.error('Error querying products:', error);
      throw error;
    }
  },

  // Get available filtering options
  async getFilters() {
    try {
      const response = await apiClient.get('/filters');
      return response.data;
    } catch (error) {
      console.error('Error fetching filters:', error);
      throw error;
    }
  }
};
