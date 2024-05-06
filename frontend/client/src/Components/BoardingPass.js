import React from 'react';
import { Card, CardContent, Typography, Grid } from '@mui/material';

function BoardingPass({ fare, formData }) {
  return (
    <Card sx={{ maxWidth: 345, marginTop: 4, background: '#f0f0f0', padding: 2 }}>
      <CardContent>
        <Typography variant="h5" component="div">
          Boarding Pass
        </Typography>
        <Typography color="text.secondary">
          Flight Details
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={6}>
            <Typography variant="body2">Destination:</Typography>
            <Typography variant="body1">{formData.destinationAirport}</Typography>
          </Grid>
            <Grid item xs={6}>
                <Typography variant="body2">Flight Date:</Typography>
                <Typography variant="body1">{formData.flightDate}</Typography>
            </Grid>

          <Grid item xs={6}>
            <Typography variant="body2">Airline:</Typography>
            <Typography variant="body1">{formData.segmentsAirlineName}</Typography>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="body2">Fare:</Typography>
            <Typography variant="body1">${fare}</Typography>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
}

export default BoardingPass;
