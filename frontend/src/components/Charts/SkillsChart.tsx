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
  Legend,
  Cell
} from 'recharts';
import { Card, CardContent, Typography, Box, CircularProgress } from '@mui/material';
import { jobsApi } from '../../services/api';

const COLORS = [
  '#1976d2', '#2e7d32', '#ed6c02', '#9c27b0', '#d32f2f',
  '#1565c0', '#388e3c', '#f57c00', '#7b1fa2', '#c62828'
];

const SkillsChart: React.FC = () => {
  const { data: skillsData, isLoading } = useQuery(
    'topSkills',
    () => jobsApi.getTopSkills(15)
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

  const chartData = skillsData?.data?.map(skill => ({
    skill: skill.skill_name,
    demand: skill.demand_count,
    salary: skill.average_salary
  })) || [];

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Top Skills in Demand
        </Typography>
        <Box height={400}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} layout="horizontal">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="skill" type="category" width={100} />
              <Tooltip 
                formatter={(value, name) => [
                  name === 'demand' ? `${value} jobs` : `KES ${value?.toLocaleString()}`,
                  name === 'demand' ? 'Demand' : 'Avg Salary'
                ]}
              />
              <Legend />
              <Bar dataKey="demand" fill="#1976d2">
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </Box>
      </CardContent>
    </Card>
  );
};

export default SkillsChart;