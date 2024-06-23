import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import Navbar from './components/Navbar';
import Footer from './components/Footer/Footer';
import Home from './Pages/Home';
import TopRatedProducts from './components/TopRatedProducts/TopRatedProducts';
import ProductsComparison from './components/ProductsComparison/ProductsComparison';
import Contact from './Pages/Contact';
import About from './Pages/About';
import ComparisonTable from './components/ComparisonTable/ComparisonTable';

function App() {
    return (
        <Router>
            <div className="App">
                <Navbar />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/top-rated-products" element={<TopRatedProducts />} />
                    <Route path="/products-comparison" element={<ProductsComparison />} />
                    <Route path="/contact" element={<Contact />} />
                    <Route path="/about" element={<About />} />
                    <Route path="/comparison-table" element={<ComparisonTable />} />
                </Routes>
                <Footer />
            </div>
        </Router>
    );
}

export default App;
