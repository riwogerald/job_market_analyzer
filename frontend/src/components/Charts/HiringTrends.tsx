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
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';
import { jobsApi } from '../../services/api';
import { format, parseISO } from 'date-fns';

const HiringTrends: React.FC = () => {
  const { data, isLoading, error } = useQuery(
    'hiringTrends',
    () => jobsApi.getHiringTrends(30),
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
            Failed to load hiring trends data
          </Alert>
        </CardContent>
      </Card>
    );
  }

  const chartData = (data?.data || []).map(item => ({
    ...item,
    formattedDate: format(parseISO(item.date), 'MMM dd')
  }));

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Daily Job Postings (Last 30 Days)
        </Typography>
        <Box height={300}>
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="colorJobs" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#1976d2" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#1976d2" stopOpacity={0.1}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="formattedDate" 
                fontSize={12}
                angle={-45}
                textAnchor="end"
                height={60}
              />
              <YAxis fontSize={12} />
              <Tooltip 
                labelFormatter={(value) => `Date: ${value}`}
                formatter={(value: number) => [value, 'New Jobs']}
              />
              <Area
                type="monotone"
                dataKey="job_count"
                stroke="#1976d2"
                fillOpacity={1}
                fill="url(#colorJobs)"
                strokeWidth={2}
              />
            </AreaChart>
          </ResponsiveContainer>
        </Box>
      </CardContent>
    </Card>
  );
};

export default HiringTrends;
