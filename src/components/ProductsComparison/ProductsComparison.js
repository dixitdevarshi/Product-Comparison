import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ProductsComparison.css';

const ProductsComparison = () => {
    const [items, setItems] = useState({ item1: '', item2: '' });
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setItems({ ...items, [name]: value });
    };

    const handleCompare = () => {
        if (items.item1 && items.item2) {
            navigate('/comparison-table', { state: { items } });
        } else {
            alert("Please enter both items to compare.");
        }
    };

    return (
        <div className="products-comparison">
            <h2>Compare Products</h2>
            <img src="./pic1.avif" alt="Device 2" className="device-image" />
            <div className="compare-inputs">
                <input
                    type="text"
                    name="item1"
                    value={items.item1}
                    onChange={handleChange}
                    placeholder="Enter item 1"
                />
                <input
                    type="text"
                    name="item2"
                    value={items.item2}
                    onChange={handleChange}
                    placeholder="Enter item 2"
                />
            </div>
            <button onClick={handleCompare}>Compare</button>
        </div>
    );
};

export default ProductsComparison;

