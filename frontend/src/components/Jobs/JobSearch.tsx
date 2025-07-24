import React, { useState, useCallback } from 'react';
import {
  Box,
  TextField,
  Button,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Paper,
  Typography
} from '@mui/material';
import { Search, Clear } from '@mui/icons-material';
import { SearchFilters } from '../../types';
import { debounce } from 'lodash';

interface JobSearchProps {
  onSearch: (filters: SearchFilters) => void;
  initialFilters?: SearchFilters;
}

const JobSearch: React.FC<JobSearchProps> = ({ onSearch, initialFilters = {} }) => {
  const [filters, setFilters] = useState<SearchFilters>(initialFilters);

  const debouncedSearch = useCallback(
    debounce((searchFilters: SearchFilters) => {
      onSearch(searchFilters);
    }, 500),
    [onSearch]
  );

  const handleFilterChange = (key: keyof SearchFilters, value: any) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    debouncedSearch(newFilters);
  };

  const clearFilters = () => {
    setFilters({});
    onSearch({});
  };

  const activeFiltersCount = Object.values(filters).filter(Boolean).length;

  return (
    <Paper sx={{ p: 3, mb: 3 }}>
      <Typography variant="h6" gutterBottom>
        Search Jobs
      </Typography>
      
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Search"
            placeholder="Job title, company, or keyword"
            value={filters.search || ''}
            onChange={(e) => handleFilterChange('search', e.target.value)}
            InputProps={{
              startAdornment: <Search sx={{ mr: 1, color: 'text.secondary' }} />
            }}
          />
        </Grid>
        
        <Grid item xs={12} md={3}>
          <TextField
            fullWidth
            label="Location"
            placeholder="City or county"
            value={filters.location || ''}
            onChange={(e) => handleFilterChange('location', e.target.value)}
          />
        </Grid>
        
        <Grid item xs={12} md={2}>
          <FormControl fullWidth>
            <InputLabel>Employment Type</InputLabel>
            <Select
              value={filters.employment_type || ''}
              onChange={(e) => handleFilterChange('employment_type', e.target.value)}
              label="Employment Type"
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value="full_time">Full Time</MenuItem>
              <MenuItem value="part_time">Part Time</MenuItem>
              <MenuItem value="contract">Contract</MenuItem>
              <MenuItem value="internship">Internship</MenuItem>
              <MenuItem value="freelance">Freelance</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        
        <Grid item xs={12} md={2}>
          <FormControl fullWidth>
            <InputLabel>Experience Level</InputLabel>
            <Select
              value={filters.experience_level || ''}
              onChange={(e) => handleFilterChange('experience_level', e.target.value)}
              label="Experience Level"
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value="entry">Entry Level</MenuItem>
              <MenuItem value="mid">Mid Level</MenuItem>
              <MenuItem value="senior">Senior Level</MenuItem>
              <MenuItem value="executive">Executive</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        
        <Grid item xs={12} md={1}>
          <Button
            fullWidth
            variant="outlined"
            startIcon={<Clear />}
            onClick={clearFilters}
            disabled={activeFiltersCount === 0}
          >
            Clear
          </Button>
        </Grid>
      </Grid>
      
      <Grid container spacing={2} sx={{ mt: 1 }}>
        <Grid item xs={12} md={2}>
          <FormControl fullWidth>
            <InputLabel>Remote Type</InputLabel>
            <Select
              value={filters.remote_type || ''}
              onChange={(e) => handleFilterChange('remote_type', e.target.value)}
              label="Remote Type"
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value="on_site">On-site</MenuItem>
              <MenuItem value="remote">Remote</MenuItem>
              <MenuItem value="hybrid">Hybrid</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        
        <Grid item xs={12} md={2}>
          <TextField
            fullWidth
            type="number"
            label="Min Salary"
            value={filters.min_salary || ''}
            onChange={(e) => handleFilterChange('min_salary', e.target.value ? Number(e.target.value) : undefined)}
          />
        </Grid>
        
        <Grid item xs={12} md={2}>
          <TextField
            fullWidth
            type="number"
            label="Max Salary"
            value={filters.max_salary || ''}
            onChange={(e) => handleFilterChange('max_salary', e.target.value ? Number(e.target.value) : undefined)}
          />
        </Grid>
        
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Skills"
            placeholder="Python, React, Project Management (comma-separated)"
            value={filters.skills || ''}
            onChange={(e) => handleFilterChange('skills', e.target.value)}
          />
        </Grid>
      </Grid>
      
      {activeFiltersCount > 0 && (
        <Box sx={{ mt: 2 }}>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            {activeFiltersCount} filter{activeFiltersCount !== 1 ? 's' : ''} active
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default JobSearch;