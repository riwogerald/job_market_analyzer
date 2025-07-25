import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from 'react-query';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Chip,
  Box,
  CircularProgress,
  Alert,
  Button,
  Divider,
  IconButton
} from '@mui/material';
import {
  LocationOn,
  Work,
  Schedule,
  AttachMoney,
  Business,
  CalendarToday,
  OpenInNew,
  ArrowBack,
  Visibility
} from '@mui/icons-material';
import { jobsApi } from '../../services/api';
import { formatSalary, formatDate } from '../../utils/formatters';

const JobDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  const { data, isLoading, error } = useQuery(
    ['job', id],
    () => jobsApi.getJobById(id!),
    {
      enabled: !!id,
      staleTime: 5 * 60 * 1000, // 5 minutes
    }
  );

  if (isLoading) {
    return (
      <Container maxWidth="lg">
        <Box display="flex" justifyContent="center" alignItems="center" height="50vh">
          <CircularProgress size={50} />
        </Box>
      </Container>
    );
  }

  if (error || !data) {
    return (
      <Container maxWidth="lg">
        <Box sx={{ py: 4 }}>
          <Alert severity="error">
            Failed to load job details. The job might have been removed or doesn't exist.
          </Alert>
          <Button
            component={Link}
            to="/jobs"
            startIcon={<ArrowBack />}
            sx={{ mt: 2 }}
          >
            Back to Jobs
          </Button>
        </Box>
      </Container>
    );
  }

  const job = data.data;

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Button
          component={Link}
          to="/jobs"
          startIcon={<ArrowBack />}
          sx={{ mb: 3 }}
          variant="outlined"
        >
          Back to Jobs
        </Button>

        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h4" component="h1" gutterBottom>
                  {job.title}
                </Typography>

                <Box display="flex" alignItems="center" gap={1} mb={2}>
                  <Business color="primary" />
                  <Typography variant="h6" color="primary">
                    {job.company.name}
                  </Typography>
                </Box>

                <Box display="flex" flexWrap="wrap" gap={2} mb={3}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <LocationOn fontSize="small" color="action" />
                    <Typography variant="body2">
                      {job.location}
                    </Typography>
                  </Box>

                  <Box display="flex" alignItems="center" gap={1}>
                    <Work fontSize="small" color="action" />
                    <Chip
                      label={job.employment_type.replace('_', ' ')}
                      size="small"
                      color="secondary"
                    />
                  </Box>

                  <Box display="flex" alignItems="center" gap={1}>
                    <Schedule fontSize="small" color="action" />
                    <Chip
                      label={job.remote_type.replace('_', ' ')}
                      size="small"
                      color={job.remote_type === 'remote' ? 'success' : 'default'}
                    />
                  </Box>

                  <Box display="flex" alignItems="center" gap={1}>
                    <CalendarToday fontSize="small" color="action" />
                    <Typography variant="body2">
                      Posted {formatDate(job.posted_date)}
                    </Typography>
                  </Box>

                  <Box display="flex" alignItems="center" gap={1}>
                    <Visibility fontSize="small" color="action" />
                    <Typography variant="body2">
                      {job.view_count} views
                    </Typography>
                  </Box>
                </Box>

                {job.salary_min && (
                  <Box mb={3}>
                    <Box display="flex" alignItems="center" gap={1} mb={1}>
                      <AttachMoney color="success" />
                      <Typography variant="h6" color="success.main">
                        {formatSalary(job.salary_min, job.salary_max, job.salary_currency)}
                      </Typography>
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      per {job.salary_period || 'month'}
                    </Typography>
                  </Box>
                )}

                <Divider sx={{ my: 3 }} />

                <Typography variant="h6" gutterBottom>
                  Job Description
                </Typography>
                <Typography
                  variant="body1"
                  sx={{
                    whiteSpace: 'pre-wrap',
                    lineHeight: 1.6,
                    mb: 3
                  }}
                >
                  {job.description}
                </Typography>

                {job.requirements && (
                  <>
                    <Typography variant="h6" gutterBottom>
                      Requirements
                    </Typography>
                    <Typography
                      variant="body1"
                      sx={{
                        whiteSpace: 'pre-wrap',
                        lineHeight: 1.6,
                        mb: 3
                      }}
                    >
                      {job.requirements}
                    </Typography>
                  </>
                )}

                {job.skills_required.length > 0 && (
                  <>
                    <Typography variant="h6" gutterBottom>
                      Required Skills
                    </Typography>
                    <Box display="flex" flexWrap="wrap" gap={1} mb={3}>
                      {job.skills_required.map((skill, index) => (
                        <Chip
                          key={index}
                          label={skill}
                          color="primary"
                          variant="outlined"
                        />
                      ))}
                    </Box>
                  </>
                )}

                {job.technologies.length > 0 && (
                  <>
                    <Typography variant="h6" gutterBottom>
                      Technologies
                    </Typography>
                    <Box display="flex" flexWrap="wrap" gap={1} mb={3}>
                      {job.technologies.map((tech, index) => (
                        <Chip
                          key={index}
                          label={tech}
                          color="secondary"
                          variant="outlined"
                        />
                      ))}
                    </Box>
                  </>
                )}

                <Divider sx={{ my: 3 }} />

                <Box display="flex" gap={2}>
                  <Button
                    variant="contained"
                    size="large"
                    href={job.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    endIcon={<OpenInNew />}
                  >
                    Apply on {job.source_platform}
                  </Button>
                  
                  <Button
                    variant="outlined"
                    size="large"
                    onClick={() => {
                      navigator.share?.({
                        title: job.title,
                        text: `Check out this job opportunity: ${job.title} at ${job.company.name}`,
                        url: window.location.href,
                      }) || navigator.clipboard.writeText(window.location.href);
                    }}
                  >
                    Share Job
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Company Information
                </Typography>
                
                <Typography variant="subtitle1" gutterBottom>
                  {job.company.name}
                </Typography>

                {job.company.industry && (
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Industry: {job.company.industry}
                  </Typography>
                )}

                {job.company.size && (
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Company Size: {job.company.size}
                  </Typography>
                )}

                {job.company.location && (
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Location: {job.company.location}
                  </Typography>
                )}

                {job.company.website && (
                  <Button
                    href={job.company.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    variant="outlined"
                    size="small"
                    fullWidth
                    sx={{ mt: 2 }}
                    endIcon={<OpenInNew />}
                  >
                    Visit Company Website
                  </Button>
                )}
              </CardContent>
            </Card>

            <Card sx={{ mt: 2 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Job Details
                </Typography>
                
                <Box mb={2}>
                  <Typography variant="body2" color="text.secondary">
                    Experience Level
                  </Typography>
                  <Typography variant="body1">
                    {job.experience_level.replace('_', ' ')}
                  </Typography>
                </Box>

                <Box mb={2}>
                  <Typography variant="body2" color="text.secondary">
                    Employment Type
                  </Typography>
                  <Typography variant="body1">
                    {job.employment_type.replace('_', ' ')}
                  </Typography>
                </Box>

                <Box mb={2}>
                  <Typography variant="body2" color="text.secondary">
                    Work Arrangement
                  </Typography>
                  <Typography variant="body1">
                    {job.remote_type.replace('_', ' ')}
                  </Typography>
                </Box>

                <Box mb={2}>
                  <Typography variant="body2" color="text.secondary">
                    Source Platform
                  </Typography>
                  <Typography variant="body1">
                    {job.source_platform}
                  </Typography>
                </Box>

                {job.county && (
                  <Box mb={2}>
                    <Typography variant="body2" color="text.secondary">
                      County
                    </Typography>
                    <Typography variant="body1">
                      {job.county}
                    </Typography>
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default JobDetail;
