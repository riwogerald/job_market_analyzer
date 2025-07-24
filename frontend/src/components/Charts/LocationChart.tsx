import React from 'react';
import { useQuery } from 'react-query';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';
import { Card, CardContent, Typography, Box, CircularProgress } from '@mui/material';
import { jobsApi } from '../../services/api';

const LocationChart: React.FC = () => {
  const { data: locationData, isLoading } = useQuery(
    'locationDistribution',
    () => jobsApi.getLocationDistribution()
  );

  if (isLoading) {
    return (
      <Card>
        <CardContent>
          <Box display="flex" justifyContent="center" p={4}>
            <CircularProgress />
          </Box>
        </CardContent>
      </Card>
    );
  }

  const chartData = locationData?.data?.map(item => ({
    location: item.county || 'Other',
    jobs: item.job_count
  })) || [];

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Job Distribution by Location
        </Typography>
        <Box height={400}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="location"
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="jobs" fill="#1976d2" />
            </BarChart>
          </ResponsiveContainer>
        </Box>
      </CardContent>
    </Card>
  );
};

export default LocationChart;