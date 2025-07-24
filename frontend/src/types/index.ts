export interface Company {
  id: number;
  name: string;
  industry: string;
  size: string;
  location: string;
  website: string;
  logo_url: string;
  job_count?: number;
}

export interface JobPosting {
  id: string;
  title: string;
  company: Company;
  description: string;
  requirements: string;
  location: string;
  county: string;
  remote_type: 'on_site' | 'remote' | 'hybrid';
  employment_type: 'full_time' | 'part_time' | 'contract' | 'internship' | 'freelance';
  experience_level: 'entry' | 'mid' | 'senior' | 'executive';
  salary_min: number | null;
  salary_max: number | null;
  salary_currency: string;
  skills_required: string[];
  technologies: string[];
  source_platform: string;
  source_url: string;
  posted_date: string;
  scraped_at: string;
  is_active: boolean;
  view_count: number;
}

export interface SkillDemand {
  skill_name: string;
  demand_count: number;
  growth_rate: number;
  avg_salary: number | null;
  last_updated: string;
}

export interface MarketOverview {
  total_active_jobs: number;
  new_jobs_last_30_days: number;
  remote_opportunities: number;
  remote_percentage: number;
  average_salary: number | null;
}

export interface LocationDistribution {
  county: string;
  job_count: number;
}

export interface SalaryInsight {
  overall_stats: {
    min_salary: number;
    max_salary: number;
    avg_salary: number;
    median_salary: number;
  };
  by_experience_level: {
    experience_level: string;
    avg_salary: number;
    job_count: number;
  }[];
  sample_size: number;
}

export interface HiringTrend {
  date: string;
  job_count: number;
}

export interface RemoteWorkTrend {
  month: string;
  total_jobs: number;
  remote_jobs: number;
  remote_percentage: number;
}

export interface SearchFilters {
  search?: string;
  location?: string;
  employment_type?: string;
  experience_level?: string;
  remote_type?: string;
  min_salary?: number;
  max_salary?: number;
  skills?: string;
  county?: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}