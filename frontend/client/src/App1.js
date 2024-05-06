import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { Container, AppBar, Toolbar, Typography, Button } from '@mui/material';
import FarePrediction from './Components/FarePrediction';
import SeatPrediction from './Components/SeatPrediction';
import PriceTrend from './Components/PriceTrend';

function App() {
  return (
    <Router>
      
        <div id='appConatiner'>
            <Button color="inherit" component={Link} to="/">Home</Button>
            <Button color="inherit" component={Link} to="/fare-prediction">Fare Prediction</Button>
            <Button color="inherit" component={Link} to="/seat-prediction">Seat Availability</Button>
            <Button color="inherit" component={Link} to="/price-trend">Price Trend</Button>
        </div>
        <Routes>
          <Route path="/" element={<Typography variant="h4" gutterBottom>Welcome to the Flight Fare Prediction System</Typography>} />
          <Route path="/fare-prediction" element={<FarePrediction />} />
          <Route path="/seat-prediction" element={<SeatPrediction />} />
          <Route path="/price-trend" element={<PriceTrend />} />
        </Routes>
     
    </Router>
  );
}

export default App;
