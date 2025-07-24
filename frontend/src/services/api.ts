import axios from 'axios';
import {
  JobPosting,
  Company,
  SkillDemand,
  MarketOverview,
  LocationDistribution,
  SalaryInsight,
  HiringTrend,
  RemoteWorkTrend,
  SearchFilters,
  PaginatedResponse
} from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Request interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const jobsApi = {
  // Job listings
  getJobs: (params: SearchFilters & { page?: number; page_size?: number }) =>
    api.get<PaginatedResponse<JobPosting>>('/jobs/', { params }),

  getJobById: (id: string) =>
    api.get<JobPosting>(`/jobs/${id}/`),

  // Companies
  getCompanies: (params?: { page?: number; page_size?: number }) =>
    api.get<PaginatedResponse<Company>>('/companies/', { params }),

  // Skills
  getSkills: (params?: { page?: number; page_size?: number }) =>
    api.get<PaginatedResponse<SkillDemand>>('/skills/', { params }),

  getTopSkills: (limit?: number) =>
    api.get<SkillDemand[]>('/skills/top/', { params: { limit } }),

  // Analytics
  getMarketOverview: () =>
    api.get<MarketOverview>('/analytics/market-overview/'),

  getLocationDistribution: () =>
    api.get<LocationDistribution[]>('/analytics/location-distribution/'),

  getExperienceDistribution: () =>
    api.get<{ experience_level: string; job_count: number }[]>('/analytics/experience-distribution/'),

  getEmploymentTypeDistribution: () =>
    api.get<{ employment_type: string; job_count: number }[]>('/analytics/employment-type-distribution/'),

  getRemoteWorkTrends: () =>
    api.get<RemoteWorkTrend[]>('/analytics/remote-work-trends/'),

  getSalaryInsights: (params?: { job_title?: string; location?: string }) =>
    api.get<SalaryInsight>('/analytics/salary-insights/', { params }),

  getHiringTrends: (period?: number) =>
    api.get<HiringTrend[]>('/analytics/hiring-trends/', { params: { period } }),

  getIndustryInsights: () =>
    api.get<{ industry: string; job_count: number; avg_salary: number }[]>('/analytics/industry-insights/'),

  // Admin actions
  triggerScraping: () =>
    api.post('/admin/trigger-scraping/'),
};