import React from 'react';
import { useQuery } from 'react-query';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  CircularProgress,
  Icon,
  Skeleton
} from '@mui/material';
import {
  Work,
  TrendingUp,
  Home,
  AttachMoney
} from '@mui/icons-material';
import { jobsApi } from '../../services/api';
import { formatCurrency, formatNumber } from '../../utils/formatters';

const StatCardSkeleton: React.FC = () => (
  <Card>
    <CardContent>
      <Box display="flex" alignItems="center" mb={2}>
        <Skeleton variant="rectangular" width={40} height={40} sx={{ mr: 2, borderRadius: 2 }} />
        <Skeleton variant="text" width={120} height={24} />
      </Box>
      <Skeleton variant="text" width={80} height={48} />
      <Skeleton variant="text" width={100} height={20} />
    </CardContent>
  </Card>
);

const MarketOverview: React.FC = () => {
  const { data: overview, isLoading, error } = useQuery(
    'marketOverview',
    () => jobsApi.getMarketOverview(),
    { refetchInterval: 300000 } // Refetch every 5 minutes
  );

  if (isLoading) {
    return (
      <Grid container spacing={3}>
        {[1, 2, 3, 4].map((item) => (
          <Grid item xs={12} sm={6} md={3} key={item}>
            <StatCardSkeleton />
          </Grid>
        ))}
      </Grid>
    );
  }

  if (error || !overview?.data) {
    return (
      <Typography color="error" align="center">
        Failed to load market overview
      </Typography>
    );
  }

  const stats = overview.data;

  const StatCard: React.FC<{
    title: string;
    value: string | number;
    icon: React.ReactNode;
    color: string;
    subtitle?: string;
  }> = ({ title, value, icon, color, subtitle }) => (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <Box
            sx={{
              backgroundColor: `${color}20`,
              borderRadius: 2,
              p: 1,
              mr: 2,
              color: color
            }}
          >
            {icon}
          </Box>
          <Typography variant="h6" component="div">
            {title}
          </Typography>
        </Box>
        <Typography variant="h4" component="div" gutterBottom>
          {value}
        </Typography>
        {subtitle && (
          <Typography variant="body2" color="text.secondary">
            {subtitle}
          </Typography>
        )}
      </CardContent>
    </Card>
  );

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Total Active Jobs"
          value={formatNumber(stats.total_active_jobs)}
          icon={<Work />}
          color="#1976d2"
        />
      </Grid>
      
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="New Jobs (30 days)"
          value={formatNumber(stats.new_jobs_last_30_days)}
          icon={<TrendingUp />}
          color="#2e7d32"
          subtitle="Recent opportunities"
        />
      </Grid>
      
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Remote Opportunities"
          value={`${stats.remote_percentage.toFixed(1)}%`}
          icon={<Home />}
          color="#ed6c02"
          subtitle={`${formatNumber(stats.remote_opportunities)} jobs`}
        />
      </Grid>
      
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Average Salary"
          value={stats.average_salary ? formatCurrency(stats.average_salary) : 'N/A'}
          icon={<AttachMoney />}
          color="#9c27b0"
          subtitle="KES per month"
        />
      </Grid>
    </Grid>
  );
};

export default MarketOverview;