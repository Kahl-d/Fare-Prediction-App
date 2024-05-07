// Import necessary React module and stylesheet
import React from 'react';
import './Homepage.css'
import image from '../Homepage.webp'

const HomePage = () => {
    return (
        <div className="homepage">
            <h1>Welcome to the Flight Fare Prediction System</h1>
            <div className="image-placeholder">
                {/* You can replace 'placeholder.png' with your actual image path */}
                <img src={image} alt="Futuristic Airport Scene" />
            </div>
        </div>
    );
};

export default HomePage;
