from django.contrib import admin
from .models import Company, JobPosting, SalaryInsight, SkillDemand

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'size', 'location', 'created_at']
    list_filter = ['industry', 'size', 'created_at']
    search_fields = ['name', 'industry', 'location']
    ordering = ['-created_at']

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'company', 'location', 'employment_type', 
        'experience_level', 'remote_type', 'salary_min', 
        'source_platform', 'posted_date', 'is_active'
    ]
    list_filter = [
        'employment_type', 'experience_level', 'remote_type', 
        'source_platform', 'is_active', 'posted_date'
    ]
    search_fields = ['title', 'company__name', 'location', 'description']
    ordering = ['-posted_date']
    readonly_fields = ['id', 'scraped_at', 'last_updated', 'view_count']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'company', 'description', 'requirements')
        }),
        ('Location & Work Type', {
            'fields': ('location', 'county', 'remote_type')
        }),
        ('Employment Details', {
            'fields': ('employment_type', 'experience_level')
        }),
        ('Salary Information', {
            'fields': ('salary_min', 'salary_max', 'salary_currency', 'salary_period')
        }),
        ('Skills & Technologies', {
            'fields': ('skills_required', 'technologies')
        }),
        ('Source Information', {
            'fields': ('source_platform', 'source_url', 'external_id')
        }),
        ('Metadata', {
            'fields': ('posted_date', 'scraped_at', 'last_updated', 'is_active', 'view_count'),
            'classes': ('collapse',)
        })
    )

@admin.register(SkillDemand)
class SkillDemandAdmin(admin.ModelAdmin):
    list_display = ['skill_name', 'demand_count', 'growth_rate', 'avg_salary', 'last_updated']
    list_filter = ['last_updated']
    search_fields = ['skill_name']
    ordering = ['-demand_count']

@admin.register(SalaryInsight)
class SalaryInsightAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'company', 'location', 'experience_level', 'salary_amount', 'reported_date']
    list_filter = ['experience_level', 'currency', 'period', 'source', 'reported_date']
    search_fields = ['job_title', 'company__name', 'location']
    ordering = ['-reported_date']

# Custom admin actions
@admin.action(description='Trigger job scraping')
def trigger_scraping(modeladmin, request, queryset):
    from apps.scrapers.tasks import scrape_all_platforms
    scrape_all_platforms.delay()
    modeladmin.message_user(request, "Job scraping has been triggered.")

@admin.action(description='Update skill demand analytics')
def update_skill_analytics(modeladmin, request, queryset):
    from apps.scrapers.tasks import update_skill_demand
    update_skill_demand.delay()
    modeladmin.message_user(request, "Skill demand analytics update has been triggered.")

# Add actions to JobPosting admin
JobPostingAdmin.actions = [trigger_scraping, update_skill_analytics]