import React, { useState } from 'react';
import { Container, TextField, Button, Typography, Checkbox, FormControlLabel } from '@mui/material';
import axios from 'axios';

function App() {
  const [formData, setFormData] = useState({
    flightDate: '',
    flightDayName: '',
    isBasicEconomy: false,
    segmentsAirlineName: '',
    destinationAirport: ''
  });
  const [fare, setFare] = useState(null);

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
      setFare(response.data.fare);
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
          label="Destination Airport"
          type="text"
          name="destinationAirport"
          value={formData.destinationAirport}
          onChange={handleChange}
          fullWidth
          margin="normal"
          helperText="Flight destination from SFO"
        />
        <TextField
          label="Airline Name"
          type="text"
          name="segmentsAirlineName"
          value={formData.segmentsAirlineName}
          onChange={handleChange}
          fullWidth
          margin="normal"
        />
        <FormControlLabel
          control={<Checkbox checked={formData.isBasicEconomy} onChange={handleChange} name="isBasicEconomy" />}
          label="Is Basic Economy?"
          margin="normal"
        />
        <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>
          Predict Fare
        </Button>
        {fare && <Typography variant="h6" sx={{ mt: 2 }}>Predicted Fare: ${fare}</Typography>}
      </form>
    </Container>
  );
}

export default App;
