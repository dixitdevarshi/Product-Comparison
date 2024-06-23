import React, { useEffect, useState } from 'react';
import './TopRatedProducts.css';

const TopRatedProducts = () => {
    const [products, setProducts] = useState([]);

    useEffect(() => {
        // Replace with actual data fetching logic
        setProducts([
            { id: 1, name: 'Product 1' },
            { id: 2, name: 'Product 2' },
            // Add more products as needed
        ]);
    }, []);

    if (!products.length) {
        return <div className="top-rated-products">Loading...</div>;
    }

    return (
        <div className="top-rated-products">
            <h2>Top Rated Products</h2>
            <ul>
                {products.map(product => (
                    <li key={product.id}>{product.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default TopRatedProducts;
