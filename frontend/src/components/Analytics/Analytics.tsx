import React from 'react';
import {
  Container,
  Grid,
  Typography,
  Box,
  Card,
  CardContent
} from '@mui/material';
import MarketOverview from '../Dashboard/MarketOverview';
import LocationChart from '../Charts/LocationChart';
import SkillsChart from '../Charts/SkillsChart';
import RemoteWorkTrends from '../Charts/RemoteWorkTrends';
import HiringTrends from '../Charts/HiringTrends';
import ExperienceDistribution from '../Charts/ExperienceDistribution';
import EmploymentTypeDistribution from '../Charts/EmploymentTypeDistribution';
import IndustryInsights from '../Charts/IndustryInsights';

const Analytics: React.FC = () => {
  return (
    <Container maxWidth="xl">
      <Box sx={{ py: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Market Analytics Dashboard
        </Typography>
        <Typography variant="h6" color="text.secondary" gutterBottom>
          Comprehensive insights into the Kenyan job market trends and patterns
        </Typography>
        
        {/* Market Overview */}
        <Box sx={{ mt: 4 }}>
          <MarketOverview />
        </Box>
        
        {/* Charts Grid */}
        <Grid container spacing={3} sx={{ mt: 2 }}>
          {/* Location and Skills */}
          <Grid item xs={12} lg={6}>
            <LocationChart />
          </Grid>
          <Grid item xs={12} lg={6}>
            <SkillsChart />
          </Grid>
          
          {/* Trends */}
          <Grid item xs={12} lg={6}>
            <RemoteWorkTrends />
          </Grid>
          <Grid item xs={12} lg={6}>
            <HiringTrends />
          </Grid>
          
          {/* Distributions */}
          <Grid item xs={12} lg={6}>
            <ExperienceDistribution />
          </Grid>
          <Grid item xs={12} lg={6}>
            <EmploymentTypeDistribution />
          </Grid>
          
          {/* Industry Insights */}
          <Grid item xs={12}>
            <IndustryInsights />
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default Analytics;
