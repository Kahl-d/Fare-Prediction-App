import React, { useState } from 'react';
import { Container, TextField, Button, Typography, Checkbox, FormControlLabel, MenuItem } from '@mui/material';
import axios from 'axios';
import BoardingPass from './BoardingPass';  // Import the BoardingPass component

function FarePrediction() {
  const [formData, setFormData] = useState({
    flightDate: '',
    isBasicEconomy: false,
    segmentsAirlineName: '',
    destinationAirport: ''
  });
  const [fare, setFare] = useState(null);

  const airports = ['LGA', 'BOS', 'EWR', 'CLT', 'ORD', 'JFK', 'PHL', 'LAX', 'IAD', 'DEN', 'ATL', 'DTW', 'DFW', 'MIA', 'OAK'];
  const airlines = ['Delta', 'United', 'Alaska Airlines', 'JetBlue Airways', 'American Airlines', 'Frontier Airlines', 'Southern Airways Express', 'Sun Country Airlines', 'Key Lime Air', 'Cape Air'];

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/predict', formData);
      setFare(response.data.prediction);
    } catch (error) {
      console.error('Error fetching fare:', error);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Flight Fare Prediction from SFO
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Flight Date (YYYY-MM-DD)"
          type="date"
          name="flightDate"
          value={formData.flightDate}
          onChange={handleChange}
          fullWidth
          margin="normal"
        />
        <TextField
          select
          label="Destination Airport"
          name="destinationAirport"
          value={formData.destinationAirport}
          onChange={handleChange}
          fullWidth
          margin="normal"
        >
          {airports.map((option) => (
            <MenuItem key={option} value={option}>
              {option}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          select
          label="Airline Name"
          name="segmentsAirlineName"
          value={formData.segmentsAirlineName}
          onChange={handleChange}
          fullWidth
          margin="normal"
        >
          {airlines.map((option) => (
            <MenuItem key={option} value={option}>
              {option}
            </MenuItem>
          ))}
        </TextField>
        <FormControlLabel
          control={<Checkbox checked={formData.isBasicEconomy} onChange={handleChange} name="isBasicEconomy" />}
          label="Is Basic Economy?"
          margin="normal"
        />
        <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>
          Predict Fare
        </Button>
      </form>
      {fare && <BoardingPass fare={fare} formData={formData} />}
    </Container>
  );
}

export default FarePrediction;
