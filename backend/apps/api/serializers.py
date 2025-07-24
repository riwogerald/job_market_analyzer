from rest_framework import serializers
from ..jobs.models import JobPosting, Company, SkillDemand

class CompanySerializer(serializers.ModelSerializer):
    job_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Company
        fields = ['id', 'name', 'industry', 'size', 'location', 'website', 'logo_url', 'job_count']

class JobPostingSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    
    class Meta:
        model = JobPosting
        fields = [
            'id', 'title', 'company', 'description', 'requirements',
            'location', 'county', 'remote_type', 'employment_type',
            'experience_level', 'salary_min', 'salary_max', 'salary_currency',
            'skills_required', 'technologies', 'source_platform', 'source_url',
            'posted_date', 'scraped_at', 'is_active'
        ]

class SkillDemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillDemand
        fields = ['skill_name', 'demand_count', 'growth_rate', 'avg_salary', 'last_updated']