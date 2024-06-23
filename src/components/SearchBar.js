import React, { useState } from 'react';
import './SearchBar.css';

const SearchBar = () => {
    const [query, setQuery] = useState('');

    const handleSearch = () => {
        console.log(`Searching for: ${query}`);
    };

    return (
        <div className="search-bar">
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search products..."
            />
            <button onClick={handleSearch}>Search</button>
        </div>
    );
};

export default SearchBar;
