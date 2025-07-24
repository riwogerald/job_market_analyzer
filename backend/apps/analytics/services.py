from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
from collections import Counter
import pandas as pd
from ..jobs.models import JobPosting, Company, SkillDemand, SalaryInsight

class AnalyticsService:
    def __init__(self):
        self.current_date = timezone.now()
        self.last_30_days = self.current_date - timedelta(days=30)
        self.last_90_days = self.current_date - timedelta(days=90)

    def get_market_overview(self):
        """Get overall job market statistics"""
        total_jobs = JobPosting.objects.filter(is_active=True).count()
        new_jobs_30d = JobPosting.objects.filter(
            scraped_at__gte=self.last_30_days,
            is_active=True
        ).count()
        
        remote_jobs = JobPosting.objects.filter(
            remote_type__in=['remote', 'hybrid'],
            is_active=True
        ).count()
        
        avg_salary = JobPosting.objects.filter(
            salary_min__isnull=False,
            is_active=True
        ).aggregate(Avg('salary_min'))['salary_min__avg']
        
        return {
            'total_active_jobs': total_jobs,
            'new_jobs_last_30_days': new_jobs_30d,
            'remote_opportunities': remote_jobs,
            'remote_percentage': (remote_jobs / total_jobs * 100) if total_jobs > 0 else 0,
            'average_salary': round(avg_salary, 2) if avg_salary else None,
        }

    def get_top_companies(self, limit=10):
        """Get companies with most job postings"""
        return Company.objects.annotate(
            job_count=Count('job_postings', filter=Q(job_postings__is_active=True))
        ).filter(job_count__gt=0).order_by('-job_count')[:limit]

    def get_location_distribution(self):
        """Get job distribution by location"""
        return JobPosting.objects.filter(is_active=True).values('county').annotate(
            job_count=Count('id')
        ).order_by('-job_count')[:15]

    def get_experience_level_distribution(self):
        """Get job distribution by experience level"""
        return JobPosting.objects.filter(is_active=True).values('experience_level').annotate(
            job_count=Count('id')
        ).order_by('-job_count')

    def get_employment_type_distribution(self):
        """Get job distribution by employment type"""
        return JobPosting.objects.filter(is_active=True).values('employment_type').annotate(
            job_count=Count('id')
        ).order_by('-job_count')

    def get_remote_work_trends(self):
        """Get remote work trends over time"""
        # Group by month for the last 12 months
        trends = []
        for i in range(12):
            month_start = self.current_date - timedelta(days=30 * (i + 1))
            month_end = self.current_date - timedelta(days=30 * i)
            
            total_jobs = JobPosting.objects.filter(
                scraped_at__range=[month_start, month_end],
                is_active=True
            ).count()
            
            remote_jobs = JobPosting.objects.filter(
                scraped_at__range=[month_start, month_end],
                remote_type__in=['remote', 'hybrid'],
                is_active=True
            ).count()
            
            trends.append({
                'month': month_start.strftime('%Y-%m'),
                'total_jobs': total_jobs,
                'remote_jobs': remote_jobs,
                'remote_percentage': (remote_jobs / total_jobs * 100) if total_jobs > 0 else 0
            })
        
        return list(reversed(trends))

    def get_salary_insights(self, job_title=None, location=None):
        """Get salary insights for specific job title or location"""
        queryset = JobPosting.objects.filter(
            salary_min__isnull=False,
            is_active=True
        )
        
        if job_title:
            queryset = queryset.filter(title__icontains=job_title)
        
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        salary_stats = queryset.aggregate(
            min_salary=Min('salary_min'),
            max_salary=Max('salary_max'),
            avg_salary=Avg('salary_min'),
            median_salary=Avg('salary_min')  # Simplified median calculation
        )
        
        # Salary distribution by experience level
        salary_by_experience = queryset.values('experience_level').annotate(
            avg_salary=Avg('salary_min'),
            job_count=Count('id')
        ).order_by('-avg_salary')
        
        return {
            'overall_stats': salary_stats,
            'by_experience_level': list(salary_by_experience),
            'sample_size': queryset.count()
        }

    def get_top_skills(self, limit=20):
        """Get most in-demand skills"""
        all_skills = []
        jobs = JobPosting.objects.filter(is_active=True).values_list('skills_required', flat=True)
        
        for skill_list in jobs:
            if skill_list:
                all_skills.extend(skill_list)
        
        skill_counts = Counter(all_skills)
        top_skills = skill_counts.most_common(limit)
        
        # Get salary information for each skill
        skills_with_salary = []
        for skill, count in top_skills:
            avg_salary = JobPosting.objects.filter(
                skills_required__contains=[skill],
                salary_min__isnull=False,
                is_active=True
            ).aggregate(Avg('salary_min'))['salary_min__avg']
            
            skills_with_salary.append({
                'skill': skill,
                'demand_count': count,
                'average_salary': round(avg_salary, 2) if avg_salary else None
            })
        
        return skills_with_salary

    def update_skill_demand(self):
        """Update skill demand table for faster queries"""
        skills_data = self.get_top_skills(100)
        
        # Clear existing data
        SkillDemand.objects.all().delete()
        
        # Insert new data
        skill_objects = []
        for skill_info in skills_data:
            skill_objects.append(SkillDemand(
                skill_name=skill_info['skill'],
                demand_count=skill_info['demand_count'],
                avg_salary=skill_info['average_salary'],
                growth_rate=0  # TODO: Calculate growth rate
            ))
        
        SkillDemand.objects.bulk_create(skill_objects)

    def get_hiring_trends(self, period_days=30):
        """Get hiring trends over specified period"""
        end_date = self.current_date
        start_date = end_date - timedelta(days=period_days)
        
        # Daily job postings
        daily_trends = []
        current_date = start_date
        
        while current_date <= end_date:
            next_date = current_date + timedelta(days=1)
            
            daily_count = JobPosting.objects.filter(
                scraped_at__range=[current_date, next_date],
                is_active=True
            ).count()
            
            daily_trends.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'job_count': daily_count
            })
            
            current_date = next_date
        
        return daily_trends

    def get_industry_insights(self):
        """Get insights by industry (based on company industry)"""
        return Company.objects.filter(
            industry__isnull=False,
            job_postings__is_active=True
        ).values('industry').annotate(
            job_count=Count('job_postings'),
            avg_salary=Avg('job_postings__salary_min')
        ).order_by('-job_count')[:15]