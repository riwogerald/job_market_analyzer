import React from 'react';
import { Grid, Container, Typography, Box } from '@mui/material';
import MarketOverview from './MarketOverview';
import LocationChart from '../Charts/LocationChart';
import SkillsChart from '../Charts/SkillsChart';
import RemoteWorkTrends from '../Charts/RemoteWorkTrends';
import HiringTrends from '../Charts/HiringTrends';

const Dashboard: React.FC = () => {
  return (
    <Container maxWidth="xl">
      <Box sx={{ py: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Kenya Job Market Analytics
        </Typography>
        <Typography variant="h6" color="text.secondary" gutterBottom>
          Real-time insights into the Kenyan job market
        </Typography>
        
        <Box sx={{ mt: 4 }}>
          <MarketOverview />
        </Box>
        
        <Grid container spacing={3} sx={{ mt: 2 }}>
          <Grid item xs={12} lg={6}>
            <LocationChart />
          </Grid>
          <Grid item xs={12} lg={6}>
            <SkillsChart />
          </Grid>
          
          <Grid item xs={12} lg={6}>
            <RemoteWorkTrends />
          </Grid>
          <Grid item xs={12} lg={6}>
            <HiringTrends />
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default Dashboard;