import React from 'react';
import './Home.css';

function Home() {
  return (
    <div className="home-container">
      <div className="images-grid">
        <img src="./background.webp" alt="Device 3" className="background-image" />
      </div>
      <div className="heading">
        <h1>Welcome to Our Tech Product Comparison Site</h1>
      </div>
      <div className="Navigation-heading">
        <h2>Navigating through the website.</h2>
      </div>
      <div className="grid-container">
        <div className="box">
          <h3 className="small-heading">Discover Top-Rated Tech Devices:</h3>
          <p className="small-content">Our Ratings page provides a comprehensive list of top-rated tech devices, including smartphones, laptops, tablets, and more. Each product is meticulously reviewed by experts and users alike, offering you detailed insights into their performance, features, and value for money. Easily find the best devices in the market, all in one place.</p>
        </div>
        <div className="box">
          <h3 className="small-heading">Expert and User Reviews:</h3>
          <p className="small-content">On our Ratings page, you’ll find detailed reviews from both tech experts and everyday users. This balanced perspective ensures you get a well-rounded understanding of each product’s strengths and weaknesses. Our goal is to help you make informed decisions by providing transparent and reliable ratings.</p>
        </div>
        <div className="box">
          <h3 className="small-heading">Compare Ratings Across Categories:</h3>
          <p className="small-content">Our Ratings page allows you to filter and compare ratings across various categories and specifications. Whether you’re looking for the best battery life, camera quality, or overall performance, our detailed rating system will guide you to the perfect choice for your needs.</p>
        </div>
        <div className="box">
          <h3 className="small-heading">Side-by-Side Product Comparison:</h3>
          <p className="small-content">Our Compare page lets you select multiple tech devices and view their specifications side by side. This feature helps you quickly identify the differences in features, performance, and pricing, making it easier to choose the right product that fits your needs and budget.</p>
        </div>
      </div>
    </div>
  );
}

export default Home;
