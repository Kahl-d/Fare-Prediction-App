import React, { useState } from 'react';
import { Container, TextField, Button, Typography } from '@mui/material';
import axios from 'axios';

function App() {
  const [formData, setFormData] = useState({
    days_until_flight: '',
    is_search_weekend: '',
    is_flight_weekend: '',
    searchDay: '',
    flightDay: '',
    isBasicEconomy: '',
    segmentsAirlineName: '',
    destinationAirport: ''
  });
  const [fare, setFare] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/predict', formData);
      setFare(response.data.fare);
    } catch (error) {
      console.error('Error fetching fare:', error);
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" component="h1" gutterBottom>
        Flight Fare Prediction
      </Typography>
      <form onSubmit={handleSubmit}>
        {/* Example input fields; add or modify as needed */}
        <TextField
          label="Days Until Flight"
          type="number"
          name="days_until_flight"
          value={formData.days_until_flight}
          onChange={handleChange}
          fullWidth
          margin="normal"
        />
        <TextField
          label="Destination Airport"
          type="text"
          name="destinationAirport"
          value={formData.destinationAirport}
          onChange={handleChange}
          fullWidth
          margin="normal"
        />
        {/* Add other inputs for each model feature */}
        <Button type="submit" variant="contained" color="primary">
          Predict Fare
        </Button>
        {fare && <Typography variant="h6">Predicted Fare: ${fare}</Typography>}
      </form>
    </Container>
  );
}

export default App;
