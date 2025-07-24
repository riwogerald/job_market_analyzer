from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid

class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    industry = models.CharField(max_length=100, blank=True)
    size = models.CharField(max_length=50, blank=True)  # e.g., "50-200 employees"
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    logo_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"

class JobPosting(models.Model):
    EMPLOYMENT_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    ]
    
    EXPERIENCE_LEVELS = [
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('executive', 'Executive'),
    ]
    
    REMOTE_TYPES = [
        ('on_site', 'On-site'),
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job_postings')
    description = models.TextField()
    requirements = models.TextField(blank=True)
    
    # Location and remote work
    location = models.CharField(max_length=100)
    county = models.CharField(max_length=50, blank=True)
    remote_type = models.CharField(max_length=20, choices=REMOTE_TYPES, default='on_site')
    
    # Employment details
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS)
    
    # Salary information
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=3, default='KES')
    salary_period = models.CharField(max_length=20, default='monthly')  # monthly, annual
    
    # Skills and technologies
    skills_required = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    technologies = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    
    # Source information
    source_platform = models.CharField(max_length=50)  # linkedin, indeed, glassdoor, etc.
    source_url = models.URLField()
    external_id = models.CharField(max_length=100, blank=True)
    
    # Metadata
    posted_date = models.DateTimeField()
    scraped_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Analytics fields
    view_count = models.IntegerField(default=0)
    application_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} at {self.company.name}"

    class Meta:
        ordering = ['-posted_date']
        indexes = [
            models.Index(fields=['location', 'remote_type']),
            models.Index(fields=['experience_level', 'employment_type']),
            models.Index(fields=['posted_date', 'is_active']),
            models.Index(fields=['source_platform']),
        ]

class SalaryInsight(models.Model):
    job_title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=100)
    experience_level = models.CharField(max_length=20)
    salary_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    period = models.CharField(max_length=20, default='monthly')
    source = models.CharField(max_length=50)
    reported_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-reported_date']

class SkillDemand(models.Model):
    skill_name = models.CharField(max_length=100, unique=True)
    demand_count = models.IntegerField(default=0)
    growth_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # percentage
    avg_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.skill_name} (Demand: {self.demand_count})"

    class Meta:
        ordering = ['-demand_count']