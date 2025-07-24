from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from ..jobs.models import JobPosting, Company, SkillDemand
from ..analytics.services import AnalyticsService
from .serializers import JobPostingSerializer, CompanySerializer, SkillDemandSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class JobPostingListView(generics.ListAPIView):
    serializer_class = JobPostingSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['employment_type', 'experience_level', 'remote_type', 'county']
    
    def get_queryset(self):
        queryset = JobPosting.objects.filter(is_active=True).select_related('company')
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(company__name__icontains=search) |
                Q(description__icontains=search) |
                Q(skills_required__contains=[search])
            )
        
        # Location filter
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(
                Q(location__icontains=location) |
                Q(county__icontains=location)
            )
        
        # Salary range filter
        min_salary = self.request.query_params.get('min_salary', None)
        max_salary = self.request.query_params.get('max_salary', None)
        
        if min_salary:
            queryset = queryset.filter(salary_min__gte=min_salary)
        
        if max_salary:
            queryset = queryset.filter(salary_max__lte=max_salary)
        
        # Skills filter
        skills = self.request.query_params.get('skills', None)
        if skills:
            skill_list = [skill.strip() for skill in skills.split(',')]
            for skill in skill_list:
                queryset = queryset.filter(skills_required__contains=[skill])
        
        return queryset.order_by('-posted_date')

class JobPostingDetailView(generics.RetrieveAPIView):
    queryset = JobPosting.objects.filter(is_active=True)
    serializer_class = JobPostingSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CompanyListView(generics.ListAPIView):
    serializer_class = CompanySerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        analytics = AnalyticsService()
        return analytics.get_top_companies(50)

class SkillDemandListView(generics.ListAPIView):
    queryset = SkillDemand.objects.all()
    serializer_class = SkillDemandSerializer
    pagination_class = StandardResultsSetPagination

@api_view(['GET'])
def market_overview(request):
    """Get overall market statistics"""
    analytics = AnalyticsService()
    data = analytics.get_market_overview()
    return Response(data)

@api_view(['GET'])
def location_distribution(request):
    """Get job distribution by location"""
    analytics = AnalyticsService()
    data = analytics.get_location_distribution()
    return Response(data)

@api_view(['GET'])
def experience_distribution(request):
    """Get job distribution by experience level"""
    analytics = AnalyticsService()
    data = analytics.get_experience_level_distribution()
    return Response(data)

@api_view(['GET'])
def employment_type_distribution(request):
    """Get job distribution by employment type"""
    analytics = AnalyticsService()
    data = analytics.get_employment_type_distribution()
    return Response(data)

@api_view(['GET'])
def remote_work_trends(request):
    """Get remote work trends over time"""
    analytics = AnalyticsService()
    data = analytics.get_remote_work_trends()
    return Response(data)

@api_view(['GET'])
def salary_insights(request):
    """Get salary insights"""
    job_title = request.query_params.get('job_title', None)
    location = request.query_params.get('location', None)
    
    analytics = AnalyticsService()
    data = analytics.get_salary_insights(job_title, location)
    return Response(data)

@api_view(['GET'])
def top_skills(request):
    """Get top skills in demand"""
    limit = int(request.query_params.get('limit', 20))
    analytics = AnalyticsService()
    data = analytics.get_top_skills(limit)
    return Response(data)

@api_view(['GET'])
def hiring_trends(request):
    """Get hiring trends"""
    period = int(request.query_params.get('period', 30))
    analytics = AnalyticsService()
    data = analytics.get_hiring_trends(period)
    return Response(data)

@api_view(['GET'])
def industry_insights(request):
    """Get industry insights"""
    analytics = AnalyticsService()
    data = analytics.get_industry_insights()
    return Response(data)

@api_view(['POST'])
def trigger_scraping(request):
    """Manually trigger scraping jobs"""
    from ..scrapers.tasks import scrape_all_platforms
    
    # Trigger background task
    task = scrape_all_platforms.delay()
    
    return Response({
        'message': 'Scraping initiated',
        'task_id': task.id
    })