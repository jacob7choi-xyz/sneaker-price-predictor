import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Container,
  Paper,
  Typography,
  Button,
  Grid,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Box
} from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import RefreshIcon from '@mui/icons-material/Refresh';

const SneakerPredictor = () => {
  const [marketData, setMarketData] = useState(null);
  const [brand, setBrand] = useState('nike');
  const [model, setModel] = useState('dunk-low');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:8000/api/market-data?brand=${brand}&model=${model}`);
      setMarketData(response.data);
      setError(null);
    } catch (err) {
      setError(`Error: ${err.message}`);
      console.error('Error details:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [brand, model]);

  const renderStats = () => {
    if (!marketData?.data?.statistics) return null;
    const stats = marketData.data.statistics;

    return (
      <Grid container spacing={2}>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h6">Current Price</Typography>
            <Typography variant="h4">${stats.current_price}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h6">7d Change</Typography>
            <Typography 
              variant="h4" 
              color={stats.price_change_7d > 0 ? 'success.main' : 'error.main'}
            >
              {stats.price_change_7d}%
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h6">30d Change</Typography>
            <Typography 
              variant="h4"
              color={stats.price_change_30d > 0 ? 'success.main' : 'error.main'}
            >
              {stats.price_change_30d}%
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h6">Highest Price</Typography>
            <Typography variant="h4">${stats.highest_price}</Typography>
          </Paper>
        </Grid>
      </Grid>
    );
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h4" gutterBottom>
              Sneaker Price Predictor
            </Typography>
            <Button 
              variant="contained" 
              onClick={fetchData}
              startIcon={<RefreshIcon />}
              disabled={loading}
            >
              Refresh Data
            </Button>
          </Box>
        </Grid>

        {/* Sneaker Selection */}
        <Grid item xs={12} md={6}>
          <FormControl fullWidth>
            <InputLabel>Brand</InputLabel>
            <Select
              value={brand}
              label="Brand"
              onChange={(e) => setBrand(e.target.value)}
            >
              <MenuItem value="nike">Nike</MenuItem>
              <MenuItem value="adidas">Adidas</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} md={6}>
          <FormControl fullWidth>
            <InputLabel>Model</InputLabel>
            <Select
              value={model}
              label="Model"
              onChange={(e) => setModel(e.target.value)}
            >
              {brand === 'nike' ? (
                <>
                  <MenuItem value="dunk-low">Dunk Low</MenuItem>
                  <MenuItem value="air-jordan-1">Air Jordan 1</MenuItem>
                  <MenuItem value="air-force-1">Air Force 1</MenuItem>
                </>
              ) : (
                <>
                  <MenuItem value="yeezy-350">Yeezy Boost 350</MenuItem>
                  <MenuItem value="superstar">Superstar</MenuItem>
                </>
              )}
            </Select>
          </FormControl>
        </Grid>

        {/* Error Display */}
        {error && (
          <Grid item xs={12}>
            <Paper sx={{ p: 2, bgcolor: 'error.light' }}>
              <Typography color="error">{error}</Typography>
            </Paper>
          </Grid>
        )}

        {/* Stats Cards */}
        {marketData && (
          <>
            <Grid item xs={12}>
              {renderStats()}
            </Grid>

            {/* Price Chart */}
            <Grid item xs={12}>
              <Paper sx={{ p: 2, height: 400 }}>
                <Typography variant="h6" gutterBottom>Price History & Prediction</Typography>
                <ResponsiveContainer>
                  <LineChart>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="date"
                      data={[...(marketData.data.history || []), ...(marketData.data.predictions || [])]}
                    />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line 
                      type="monotone" 
                      data={marketData.data.history || []}
                      dataKey="price" 
                      stroke="#8884d8" 
                      name="Historical Price"
                    />
                    <Line 
                      type="monotone" 
                      data={marketData.data.predictions || []}
                      dataKey="price" 
                      stroke="#82ca9d" 
                      strokeDasharray="5 5"
                      name="Predicted Price"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Paper>
            </Grid>
          </>
        )}
      </Grid>
    </Container>
  );
};

export default SneakerPredictor;