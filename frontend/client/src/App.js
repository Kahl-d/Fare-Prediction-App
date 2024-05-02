import React, { useState } from 'react';
import { Container, TextField, Button, Typography } from '@mui/material';
import axios from 'axios';

function App() {
  const [formData, setFormData] = useState({
    date: '',
    destination: '',
    // Add other form fields as necessary
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
    <div className="App">
    <Container maxWidth="sm">
      <Typography variant="h4" component="h1" gutterBottom>
        Flight Fare Prediction
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Flight Date"
          type="date"
          name="date"
          value={formData.date}
          onChange={handleChange}
          fullWidth
          margin="normal"
        />
        <TextField
          label="Destination"
          type="text"
          name="destination"
          value={formData.destination}
          onChange={handleChange}
          fullWidth
          margin="normal"
        />
        {/* Add other inputs as needed */}
        <Button type="submit" variant="contained" color="primary">
          Predict Fare
        </Button>
        {fare && <Typography variant="h6">Predicted Fare: ${fare}</Typography>}
      </form>
    </Container>

    <div className='prediction'>{fare}</div>
    </div>
  );
}

export default App;
