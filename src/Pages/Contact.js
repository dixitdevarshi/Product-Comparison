import React from 'react';
import './Contact.css';

const Contact = () => (
    <div className="contact">
        <h1>Contact Us</h1>
        <form className="contact-form">
            <input type="text" placeholder="Name" />
            <input type="email" placeholder="Email" />
            <textarea placeholder="Message" rows="4"></textarea>
            <button type="submit">Send</button>
        </form>
    </div>
);

export default Contact;
