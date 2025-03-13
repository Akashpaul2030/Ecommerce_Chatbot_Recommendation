import React, { useState, useEffect } from 'react';
import { productService } from '../services/api';
import './SearchFilters.css';

const SearchFilters = ({ onFilterChange }) => {
  const [filters, setFilters] = useState({
    minPrice: '',
    maxPrice: '',
    brand: '',
    category: '',
    color: ''
  });

  const [availableFilters, setAvailableFilters] = useState({
    brands: [],
    categories: [],
    price_range: { min: 0, max: 10000 }
  });

  // Colors for the color filter
  const colors = [
    { name: 'Red', value: 'red' },
    { name: 'Blue', value: 'blue' },
    { name: 'Green', value: 'green' },
    { name: 'Black', value: 'black' },
    { name: 'White', value: 'white' },
    { name: 'Yellow', value: 'yellow' },
    { name: 'Purple', value: 'purple' },
    { name: 'Pink', value: 'pink' },
    { name: 'Orange', value: 'orange' },
    { name: 'Brown', value: 'brown' },
    { name: 'Grey', value: 'grey' }
  ];

  // Fetch available filters from the API
  useEffect(() => {
    const fetchFilters = async () => {
      try {
        const data = await productService.getFilters();
        setAvailableFilters(data);
      } catch (error) {
        console.error('Error fetching filters:', error);
      }
    };

    fetchFilters();
  }, []);

  // Handle filter change
  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters({
      ...filters,
      [name]: value
    });
  };

  // Apply filters
  const applyFilters = () => {
    const activeFilters = {};
    
    if (filters.minPrice) activeFilters.min_price = parseFloat(filters.minPrice);
    if (filters.maxPrice) activeFilters.max_price = parseFloat(filters.maxPrice);
    if (filters.brand) activeFilters.brand = filters.brand;
    if (filters.category) activeFilters.category = filters.category;
    if (filters.color) activeFilters.color = filters.color;

    onFilterChange(activeFilters);
  };

  // Reset filters
  const resetFilters = () => {
    setFilters({
      minPrice: '',
      maxPrice: '',
      brand: '',
      category: '',
      color: ''
    });
    onFilterChange({});
  };

  return (
    <div className="search-filters">
      <h2>Filters</h2>
      
      <div className="filter-section">
        <h3>Price Range</h3>
        <div className="price-inputs">
          <input
            type="number"
            name="minPrice"
            placeholder="Min Price"
            value={filters.minPrice}
            onChange={handleFilterChange}
            min={availableFilters.price_range.min}
          />
          <span>to</span>
          <input
            type="number"
            name="maxPrice"
            placeholder="Max Price"
            value={filters.maxPrice}
            onChange={handleFilterChange}
            max={availableFilters.price_range.max}
          />
        </div>
      </div>

      <div className="filter-section">
        <h3>Brand</h3>
        <select name="brand" value={filters.brand} onChange={handleFilterChange}>
          <option value="">All Brands</option>
          {availableFilters.brands.map((brand) => (
            <option key={brand} value={brand}>
              {brand.charAt(0).toUpperCase() + brand.slice(1)}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-section">
        <h3>Category</h3>
        <select name="category" value={filters.category} onChange={handleFilterChange}>
          <option value="">All Categories</option>
          {availableFilters.categories.map((category) => (
            <option key={category} value={category}>
              {category.charAt(0).toUpperCase() + category.slice(1)}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-section">
        <h3>Color</h3>
        <select name="color" value={filters.color} onChange={handleFilterChange}>
          <option value="">All Colors</option>
          {colors.map((color) => (
            <option key={color.value} value={color.value}>
              {color.name}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-actions">
        <button className="apply-btn" onClick={applyFilters}>Apply Filters</button>
        <button className="reset-btn" onClick={resetFilters}>Reset</button>
      </div>
    </div>
  );
};

export default SearchFilters;

