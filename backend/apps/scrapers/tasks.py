from celery import shared_task
from django.utils import timezone
from datetime import datetime, timedelta
import logging
from .linkedin_scraper import LinkedInScraper
from .indeed_scraper import IndeedScraper
from .glassdoor_scraper import GlassdoorScraper
from .career_pages_scraper import CareerPagesScraper
from ..jobs.models import JobPosting, Company, SkillDemand
from ..analytics.services import AnalyticsService

logger = logging.getLogger(__name__)

@shared_task
def scrape_all_platforms():
    """Scrape jobs from all platforms"""
    search_terms = [
        "software engineer", "data scientist", "product manager", 
        "marketing manager", "sales representative", "accountant",
        "project manager", "business analyst", "ui/ux designer"
    ]
    
    locations = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Kenya"]
    
    for search_term in search_terms:
        for location in locations:
            scrape_linkedin_jobs.delay(search_term, location)
            scrape_indeed_jobs.delay(search_term, location)
            scrape_glassdoor_jobs.delay(search_term, location)
    
    # Scrape career pages (doesn't need search terms/locations)
    scrape_career_pages.delay()

@shared_task
def scrape_linkedin_jobs(search_term="", location="Kenya", max_pages=3):
    """Scrape jobs from LinkedIn"""
    scraper = LinkedInScraper()
    
    try:
        jobs = scraper.scrape_jobs(search_term, location, max_pages)
        saved_count = 0
        
        for job_data in jobs:
            if save_job_posting(job_data):
                saved_count += 1
        
        logger.info(f"LinkedIn: Scraped {len(jobs)} jobs, saved {saved_count} new jobs")
        return f"LinkedIn: {saved_count} new jobs saved"
        
    except Exception as e:
        logger.error(f"Error in LinkedIn scraping task: {e}")
        return f"LinkedIn scraping failed: {e}"
    finally:
        scraper.close()

@shared_task
def scrape_indeed_jobs(search_term="", location="Nairobi", max_pages=3):
    """Scrape jobs from Indeed"""
    scraper = IndeedScraper()
    
    try:
        jobs = scraper.scrape_jobs(search_term, location, max_pages)
        saved_count = 0
        
        for job_data in jobs:
            if save_job_posting(job_data):
                saved_count += 1
        
        logger.info(f"Indeed: Scraped {len(jobs)} jobs, saved {saved_count} new jobs")
        return f"Indeed: {saved_count} new jobs saved"
        
    except Exception as e:
        logger.error(f"Error in Indeed scraping task: {e}")
        return f"Indeed scraping failed: {e}"
    finally:
        scraper.close()

@shared_task
def scrape_glassdoor_jobs(search_term="", location="Kenya", max_pages=3):
    """Scrape jobs from Glassdoor"""
    scraper = GlassdoorScraper()
    
    try:
        jobs = scraper.scrape_jobs(search_term, location, max_pages)
        saved_count = 0
        
        for job_data in jobs:
            if save_job_posting(job_data):
                saved_count += 1
        
        logger.info(f"Glassdoor: Scraped {len(jobs)} jobs, saved {saved_count} new jobs")
        return f"Glassdoor: {saved_count} new jobs saved"
        
    except Exception as e:
        logger.error(f"Error in Glassdoor scraping task: {e}")
        return f"Glassdoor scraping failed: {e}"
    finally:
        scraper.close()

@shared_task
def scrape_career_pages():
    """Scrape jobs from company career pages"""
    scraper = CareerPagesScraper()
    
    try:
        jobs = scraper.scrape_jobs()
        saved_count = 0
        
        for job_data in jobs:
            if save_job_posting(job_data):
                saved_count += 1
        
        logger.info(f"Career Pages: Scraped {len(jobs)} jobs, saved {saved_count} new jobs")
        return f"Career Pages: {saved_count} new jobs saved"
        
    except Exception as e:
        logger.error(f"Error in Career Pages scraping task: {e}")
        return f"Career Pages scraping failed: {e}"
    finally:
        scraper.close()

def save_job_posting(job_data):
    """Save job posting to database"""
    try:
        # Get or create company
        company, created = Company.objects.get_or_create(
            name=job_data['company'],
            defaults={'industry': '', 'size': '', 'location': job_data.get('location', '')}
        )
        
        # Check if job already exists
        existing_job = JobPosting.objects.filter(
            external_id=job_data.get('external_id', ''),
            source_platform=job_data['source_platform'],
            company=company
        ).first()
        
        if existing_job:
            # Update existing job
            existing_job.last_updated = timezone.now()
            existing_job.is_active = True
            existing_job.save()
            return False
        
        # Create new job posting
        job_posting = JobPosting.objects.create(
            title=job_data['title'],
            company=company,
            description=job_data.get('description', ''),
            requirements=job_data.get('requirements', ''),
            location=job_data.get('location', ''),
            county=extract_county(job_data.get('location', '')),
            remote_type=job_data.get('remote_type', 'on_site'),
            employment_type=job_data.get('employment_type', 'full_time'),
            experience_level=job_data.get('experience_level', 'mid'),
            salary_min=job_data.get('salary_min'),
            salary_max=job_data.get('salary_max'),
            skills_required=job_data.get('skills_required', []),
            source_platform=job_data['source_platform'],
            source_url=job_data['source_url'],
            external_id=job_data.get('external_id', ''),
            posted_date=parse_posted_date(job_data.get('posted_date')),
        )
        
        return True
        
    except Exception as e:
        logger.error(f"Error saving job posting: {e}")
        return False

def extract_county(location):
    """Extract county from location string"""
    kenyan_counties = [
        'Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret', 'Thika', 'Malindi',
        'Kitale', 'Garissa', 'Kakamega', 'Machakos', 'Meru', 'Nyeri', 'Kericho'
    ]
    
    location_lower = location.lower()
    for county in kenyan_counties:
        if county.lower() in location_lower:
            return county
    return ''

def parse_posted_date(date_str):
    """Parse posted date string to datetime"""
    if not date_str:
        return timezone.now()
    
    try:
        # Handle different date formats
        if 'ago' in date_str.lower():
            return timezone.now() - timedelta(days=1)
        else:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except:
        return timezone.now()

@shared_task
def update_skill_demand():
    """Update skill demand analytics"""
    try:
        analytics_service = AnalyticsService()
        analytics_service.update_skill_demand()
        logger.info("Skill demand updated successfully")
        return "Skill demand updated"
    except Exception as e:
        logger.error(f"Error updating skill demand: {e}")
        return f"Skill demand update failed: {e}"

@shared_task
def cleanup_old_jobs():
    """Remove old inactive job postings"""
    try:
        cutoff_date = timezone.now() - timedelta(days=90)
        deleted_count = JobPosting.objects.filter(
            last_updated__lt=cutoff_date,
            is_active=False
        ).delete()[0]
        
        logger.info(f"Cleaned up {deleted_count} old job postings")
        return f"Cleaned up {deleted_count} jobs"
    except Exception as e:
        logger.error(f"Error cleaning up old jobs: {e}")
        return f"Cleanup failed: {e}"