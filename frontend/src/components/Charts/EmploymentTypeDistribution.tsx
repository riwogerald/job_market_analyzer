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
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';
import { jobsApi } from '../../services/api';

const EmploymentTypeDistribution: React.FC = () => {
  const { data, isLoading, error } = useQuery(
    'employmentTypeDistribution',
    () => jobsApi.getEmploymentTypeDistribution(),
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
            Failed to load employment type distribution data
          </Alert>
        </CardContent>
      </Card>
    );
  }

  const chartData = (data?.data || []).map(item => ({
    ...item,
    name: item.employment_type.replace('_', ' ').toUpperCase(),
    value: item.job_count
  }));

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Jobs by Employment Type
        </Typography>
        <Box height={300}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="name" 
                fontSize={12}
                angle={-45}
                textAnchor="end"
                height={60}
              />
              <YAxis fontSize={12} />
              <Tooltip 
                formatter={(value: number) => [value, 'Jobs']}
                labelFormatter={(label) => `${label}`}
              />
              <Bar 
                dataKey="value" 
                fill="#82ca9d" 
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </Box>
      </CardContent>
    </Card>
  );
};

export default EmploymentTypeDistribution;
