import React from 'react';
import './ProductCard.css';

const ProductCard = ({ product }) => {
  // Calculate discount percentage
  const discountPercentage = product.price > 0 
    ? Math.round(((product.price - product.discounted_price) / product.price) * 100) 
    : 0;

  // Get the first image URL or use a placeholder
  const imageUrl = product.image_urls && product.image_urls.length > 0
    ? product.image_urls[0]
    : 'https://via.placeholder.com/150?text=No+Image';

  return (
    <div className="product-card">
      <div className="product-image">
        <img src={imageUrl} alt={product.name} />
        {discountPercentage > 0 && (
          <div className="discount-badge">{discountPercentage}% OFF</div>
        )}
      </div>
      <div className="product-info">
        <h3 className="product-name">{product.name}</h3>
        <p className="product-brand">{product.brand}</p>
        <div className="product-price">
          <span className="discounted-price">₹{product.discounted_price.toFixed(2)}</span>
          {product.price > product.discounted_price && (
            <span className="original-price">₹{product.price.toFixed(2)}</span>
          )}
        </div>
        <p className="product-description">{product.description.substring(0, 100)}...</p>
        <button className="view-details-btn">View Details</button>
      </div>
    </div>
  );
};

export default ProductCard;
