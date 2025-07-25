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
  Legend,
  ResponsiveContainer
} from 'recharts';
import { jobsApi } from '../../services/api';

const IndustryInsights: React.FC = () => {
  const { data, isLoading, error } = useQuery(
    'industryInsights',
    () => jobsApi.getIndustryInsights(),
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
            Failed to load industry insights data
          </Alert>
        </CardContent>
      </Card>
    );
  }

  const chartData = (data?.data || []).map(item => ({
    ...item,
    name: item.industry || 'Other',
    jobs: item.job_count,
    avgSalary: item.avg_salary ? Math.round(item.avg_salary) : 0
  })).slice(0, 10); // Show top 10 industries

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Top Industries by Job Count and Average Salary
        </Typography>
        <Box height={400}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ bottom: 60 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="name" 
                fontSize={12}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis yAxisId="left" fontSize={12} />
              <YAxis yAxisId="right" orientation="right" fontSize={12} />
              <Tooltip 
                formatter={(value: number, name: string) => [
                  name === 'jobs' ? value : `KES ${value.toLocaleString()}`,
                  name === 'jobs' ? 'Job Count' : 'Avg Salary'
                ]}
                labelFormatter={(label) => `Industry: ${label}`}
              />
              <Legend />
              <Bar 
                yAxisId="left"
                dataKey="jobs" 
                fill="#8884d8" 
                name="Job Count"
                radius={[4, 4, 0, 0]}
              />
              <Bar 
                yAxisId="right"
                dataKey="avgSalary" 
                fill="#82ca9d" 
                name="Avg Salary (KES)"
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </Box>
      </CardContent>
    </Card>
  );
};

export default IndustryInsights;
