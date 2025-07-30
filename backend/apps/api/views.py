from rest_framework import generics, status
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.conf import settings
import logging
from ..jobs.models import JobPosting, Company, SkillDemand
from ..analytics.services import AnalyticsService
from .serializers import JobPostingSerializer, CompanySerializer, SkillDemandSerializer

logger = logging.getLogger(__name__)

# Custom throttle classes
class AdminThrottle(UserRateThrottle):
    scope = 'admin'

class SearchThrottle(AnonRateThrottle):
    scope = 'search'

# Custom permission classes
class IsAdminOrAPIKey(object):
    """Custom permission for admin operations"""
    
    def has_permission(self, request, view):
        # Check for API key in headers
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            # In production, store this securely in environment variables
            expected_key = getattr(settings, 'ADMIN_API_KEY', None)
            if expected_key and api_key == expected_key:
                return True
                
        # Check for Django admin user
        if request.user and request.user.is_authenticated and request.user.is_staff:
            return True
            
        return False

def validate_integer_param(value, name, min_val=None, max_val=None, default=None):
    """Safely validate and convert integer parameters"""
    if value is None:
        return default
    
    try:
        int_value = int(value)
        if min_val is not None and int_value < min_val:
            raise ValidationError(f"{name} must be at least {min_val}")
        if max_val is not None and int_value > max_val:
            raise ValidationError(f"{name} must be at most {max_val}")
        return int_value
    except (ValueError, TypeError):
        raise ValidationError(f"{name} must be a valid integer")

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
        
        # Search functionality with full-text search
        search = self.request.query_params.get('search', None)
        if search:
            try:
                # Use PostgreSQL full-text search for better performance
                search_vector = SearchVector('title', weight='A') + \
                               SearchVector('company__name', weight='A') + \
                               SearchVector('description', weight='B') + \
                               SearchVector('requirements', weight='C')
                
                search_query = SearchQuery(search)
                
                queryset = queryset.annotate(
                    search=search_vector,
                    rank=SearchRank(search_vector, search_query)
                ).filter(
                    Q(search=search_query) |
                    Q(skills_required__icontains=search)
                ).order_by('-rank', '-posted_date')
                
            except Exception:
                # Fallback to basic search if full-text search fails
                queryset = queryset.filter(
                    Q(title__icontains=search) |
                    Q(company__name__icontains=search) |
                    Q(description__icontains=search) |
                    Q(skills_required__contains=[search])
                ).order_by('-posted_date')
        else:
            queryset = queryset.order_by('-posted_date')
        
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
        
        # Only apply default ordering if no search was performed (search has its own ordering)
        if not search:
            queryset = queryset.order_by('-posted_date')
            
        return queryset

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
    try:
        limit = validate_integer_param(
            request.query_params.get('limit', 20), 
            'limit', 
            min_val=1, 
            max_val=100, 
            default=20
        )
        analytics = AnalyticsService()
        data = analytics.get_top_skills(limit)
        return Response(data)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def hiring_trends(request):
    """Get hiring trends"""
    try:
        period = validate_integer_param(
            request.query_params.get('period', 30),
            'period',
            min_val=1,
            max_val=365,
            default=30
        )
        analytics = AnalyticsService()
        data = analytics.get_hiring_trends(period)
        return Response(data)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def industry_insights(request):
    """Get industry insights"""
    analytics = AnalyticsService()
    data = analytics.get_industry_insights()
    return Response(data)

@api_view(['POST'])
@throttle_classes([AdminThrottle])
def trigger_scraping(request):
    """Manually trigger scraping jobs - Admin only with API key authentication"""
    
    # Check authentication
    permission_checker = IsAdminOrAPIKey()
    if not permission_checker.has_permission(request, None):
        logger.warning(
            f"Unauthorized scraping attempt from {request.META.get('REMOTE_ADDR', 'unknown')}"
        )
        return Response(
            {'error': 'Authentication required. Provide X-API-Key header or login as admin.'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        from ..scrapers.tasks import scrape_all_platforms
        
        # Log the scraping request for security monitoring
        user_info = 'admin_user' if request.user.is_authenticated else 'api_key'
        logger.warning(
            f"Scraping triggered by {user_info} from {request.META.get('REMOTE_ADDR', 'unknown')}"
        )
        
        # Trigger background task
        task = scrape_all_platforms.delay()
        
        return Response({
            'message': 'Scraping initiated successfully',
            'task_id': task.id,
            'authenticated_as': user_info
        })
    except Exception as e:
        logger.error(f"Error triggering scraping: {e}")
        return Response(
            {'error': 'Failed to initiate scraping'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
