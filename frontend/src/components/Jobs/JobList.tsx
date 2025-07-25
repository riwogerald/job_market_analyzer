import React, { useState } from 'react';
import { useQuery } from 'react-query';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Chip,
  Box,
  Pagination,
  CircularProgress,
  Alert,
  Button,
  Divider
} from '@mui/material';
import {
  LocationOn,
  Work,
  Schedule,
  AttachMoney,
  Business
} from '@mui/icons-material';
import { Link } from 'react-router-dom';
import { jobsApi } from '../../services/api';
import { JobPosting, SearchFilters } from '../../types';
import JobSearch from './JobSearch';
import { formatSalary, formatDate } from '../../utils/formatters';

const JobList: React.FC = () => {
  const [page, setPage] = useState(1);
  const [filters, setFilters] = useState<SearchFilters>({});
  const pageSize = 20;

  const { data, isLoading, error } = useQuery(
    ['jobs', page, filters],
    () => jobsApi.getJobs({ ...filters, page, page_size: pageSize }),
    {
      keepPreviousData: true,
      staleTime: 2 * 60 * 1000, // 2 minutes
    }
  );

  const handlePageChange = (event: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleFiltersChange = (newFilters: SearchFilters) => {
    setFilters(newFilters);
    setPage(1); // Reset to first page when filters change
  };

  const totalPages = data?.data.count ? Math.ceil(data.data.count / pageSize) : 0;
  const jobs = data?.data.results || [];

  return (
    <Container maxWidth="xl">
      <Box sx={{ py: 4 }}>
        <>
          <Typography variant="h4" component="h1" gutterBottom>
            Job Opportunities in Kenya
          </Typography>
          
          <JobSearch onFiltersChange={handleFiltersChange} />
          
          <Box sx={{ mt: 4, mb: 2 }}>
            <Typography variant="h6" color="text.secondary">
              {data?.data.count ? `${data.data.count} jobs found` : 'Loading...'}
            </Typography>
          </Box>

          {isLoading && (
            <Box display="flex" justifyContent="center" sx={{ py: 4 }}>
              <CircularProgress />
            </Box>
          )}

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              Failed to load jobs. Please try again.
            </Alert>
          )}

          <Grid container spacing={3}>
            {jobs.map((job: JobPosting) => (
              <Grid item xs={12} key={job.id}>
                <Card sx={{ '&:hover': { elevation: 4 } }}>
                  <CardContent>
                    <Grid container spacing={2}>
                      <Grid item xs={12} md={8}>
                        <Typography variant="h6" component="h2" gutterBottom>
                          <Link 
                            to={`/jobs/${job.id}`}
                            style={{ textDecoration: 'none', color: 'inherit' }}
                          >
                            {job.title}
                          </Link>
                        </Typography>
                        
                        <Box display="flex" alignItems="center" gap={1} mb={1}>
                          <Business fontSize="small" color="action" />
                          <Typography variant="body2" color="text.secondary">
                            {job.company.name}
                          </Typography>
                        </Box>

                        <Box display="flex" alignItems="center" gap={1} mb={1}>
                          <LocationOn fontSize="small" color="action" />
                          <Typography variant="body2" color="text.secondary">
                            {job.location}
                          </Typography>
                        </Box>

                        <Typography 
                          variant="body2" 
                          color="text.secondary" 
                          sx={{ 
                            display: '-webkit-box',
                            WebkitLineClamp: 2,
                            WebkitBoxOrient: 'vertical',
                            overflow: 'hidden',
                            mb: 2
                          }}
                        >
                          {job.description}
                        </Typography>

                        <Box display="flex" flexWrap="wrap" gap={1}>
                          {job.skills_required.slice(0, 5).map((skill, index) => (
                            <Chip
                              key={index}
                              label={skill}
                              size="small"
                              variant="outlined"
                              color="primary"
                            />
                          ))}
                          {job.skills_required.length > 5 && (
                            <Chip
                              label={`+${job.skills_required.length - 5} more`}
                              size="small"
                              variant="outlined"
                            />
                          )}
                        </Box>
                      </Grid>

                      <Grid item xs={12} md={4}>
                        <Box textAlign={{ xs: 'left', md: 'right' }}>
                          {job.salary_min && (
                            <Box display="flex" alignItems="center" justifyContent={{ xs: 'flex-start', md: 'flex-end' }} gap={1} mb={1}>
                              <AttachMoney fontSize="small" color="action" />
                              <Typography variant="body2" fontWeight="medium">
                                {formatSalary(job.salary_min, job.salary_max, job.salary_currency)}
                              </Typography>
                            </Box>
                          )}

                          <Box display="flex" alignItems="center" justifyContent={{ xs: 'flex-start', md: 'flex-end' }} gap={1} mb={1}>
                            <Work fontSize="small" color="action" />
                            <Chip
                              label={job.employment_type.replace('_', ' ')}
                              size="small"
                              color="secondary"
                            />
                          </Box>

                          <Box display="flex" alignItems="center" justifyContent={{ xs: 'flex-start', md: 'flex-end' }} gap={1} mb={1}>
                            <Schedule fontSize="small" color="action" />
                            <Chip
                              label={job.remote_type.replace('_', ' ')}
                              size="small"
                              color={job.remote_type === 'remote' ? 'success' : 'default'}
                            />
                          </Box>

                          <Typography 
                            variant="caption" 
                            color="text.secondary" 
                            display="block"
                            textAlign={{ xs: 'left', md: 'right' }}
                            sx={{ mt: 2 }}
                          >
                            Posted {formatDate(job.posted_date)}
                          </Typography>

                          <Button
                            component={Link}
                            to={`/jobs/${job.id}`}
                            variant="outlined"
                            size="small"
                            sx={{ mt: 1, width: { xs: 'auto', md: '100%' } }}
                          >
                            View Details
                          </Button>
                        </Box>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          {totalPages > 1 && (
            <Box display="flex" justifyContent="center" sx={{ mt: 4 }}>
              <Pagination
                count={totalPages}
                page={page}
                onChange={handlePageChange}
                color="primary"
                size="large"
              />
            </Box>
          )}

          {jobs.length === 0 && !isLoading && (
            <Box textAlign="center" sx={{ py: 4 }}>
              <Typography variant="h6" color="text.secondary">
                No jobs found matching your criteria
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Try adjusting your search filters
              </Typography>
            </Box>
          )}
        </>
      </Box>
    </Container>
  );
};

export default JobList;
