# backend/apps/api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Job listings
    path('jobs/', views.JobPostingListView.as_view(), name='job-list'),
    path('jobs/<uuid:pk>/', views.JobPostingDetailView.as_view(), name='job-detail'),
    
    # Companies
    path('companies/', views.CompanyListView.as_view(), name='company-list'),
    
    # Skills
    path('skills/', views.SkillDemandListView.as_view(), name='skill-list'),
    path('skills/top/', views.top_skills, name='top-skills'),
    
    # Analytics endpoints
    path('analytics/market-overview/', views.market_overview, name='market-overview'),
    path('analytics/location-distribution/', views.location_distribution, name='location-distribution'),
    path('analytics/experience-distribution/', views.experience_distribution, name='experience-distribution'),
    path('analytics/employment-type-distribution/', views.employment_type_distribution, name='employment-type-distribution'),
    path('analytics/remote-work-trends/', views.remote_work_trends, name='remote-work-trends'),
    path('analytics/salary-insights/', views.salary_insights, name='salary-insights'),
    path('analytics/hiring-trends/', views.hiring_trends, name='hiring-trends'),
    path('analytics/industry-insights/', views.industry_insights, name='industry-insights'),
    
    # Admin actions
    path('admin/trigger-scraping/', views.trigger_scraping, name='trigger-scraping'),
]