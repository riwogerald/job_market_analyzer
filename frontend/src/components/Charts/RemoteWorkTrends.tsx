import React from 'react';
import { useQuery } from 'react-query';
import {
  Card,
  CardContent,
  Typography,
  Box,
  CircularProgress,
  Alert
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { jobsApi } from '../../services/api';

const RemoteWorkTrends: React.FC = () => {
  const { data, isLoading, error } = useQuery(
    'remoteWorkTrends',
    () => jobsApi.getRemoteWorkTrends(),
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
    }
  );

  if (isLoading) {
    return (
      <Card>
        <CardContent>
          <Box display="flex" justifyContent="center" alignItems="center" height={300}>
            <CircularProgress />
          </Box>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent>
          <Alert severity="error">
            Failed to load remote work trends data
          </Alert>
        </CardContent>
      </Card>
    );
  }

  const chartData = data?.data || [];

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Remote Work Trends (Last 12 Months)
        </Typography>
        <Box height={300}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="month" 
                fontSize={12}
                angle={-45}
                textAnchor="end"
                height={60}
              />
              <YAxis fontSize={12} />
              <Tooltip 
                labelFormatter={(value) => `Month: ${value}`}
                formatter={(value: number, name: string) => [
                  name === 'remote_percentage' ? `${value.toFixed(1)}%` : value,
                  name === 'remote_percentage' ? 'Remote %' : 
                  name === 'total_jobs' ? 'Total Jobs' : 'Remote Jobs'
                ]}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="total_jobs" 
                stroke="#1976d2" 
                name="Total Jobs"
                strokeWidth={2}
              />
              <Line 
                type="monotone" 
                dataKey="remote_jobs" 
                stroke="#ff6b6b" 
                name="Remote Jobs"
                strokeWidth={2}
              />
              <Line 
                type="monotone" 
                dataKey="remote_percentage" 
                stroke="#4ecdc4" 
                name="Remote %"
                strokeWidth={2}
                yAxisId="right"
              />
            </LineChart>
          </ResponsiveContainer>
        </Box>
      </CardContent>
    </Card>
  );
};

export default RemoteWorkTrends;
