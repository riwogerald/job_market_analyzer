from .base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
import logging

logger = logging.getLogger(__name__)

class LinkedInScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.linkedin.com/jobs/search"

    def scrape_jobs(self, search_term="", location="Kenya", max_pages=5):
        jobs = []
        
        try:
            # Build search URL
            search_url = f"{self.base_url}?keywords={search_term}&location={location}&f_C=&f_E=1,2,3,4&f_JT=F,P,C,T"
            
            for page in range(max_pages):
                page_url = f"{search_url}&start={page * 25}"
                logger.info(f"Scraping LinkedIn page {page + 1}: {page_url}")
                
                self.driver.get(page_url)
                self.random_delay()
                
                # Wait for job listings to load
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search__results-list"))
                    )
                except TimeoutException:
                    logger.warning(f"Timeout waiting for job listings on page {page + 1}")
                    continue
                
                # Get job cards
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".base-card.relative")
                
                for card in job_cards:
                    try:
                        job_data = self.parse_job_details(card)
                        if job_data:
                            jobs.append(job_data)
                    except Exception as e:
                        logger.error(f"Error parsing job card: {e}")
                        continue
                
                self.random_delay()
        
        except Exception as e:
            logger.error(f"Error scraping LinkedIn: {e}")
        
        return jobs

    def parse_job_details(self, job_card):
        try:
            # Extract basic information
            title_element = job_card.find_element(By.CSS_SELECTOR, ".base-search-card__title")
            title = title_element.text.strip()
            
            company_element = job_card.find_element(By.CSS_SELECTOR, ".base-search-card__subtitle")
            company = company_element.text.strip()
            
            location_element = job_card.find_element(By.CSS_SELECTOR, ".job-search-card__location")
            location = location_element.text.strip()
            
            # Get job URL
            job_link = job_card.find_element(By.CSS_SELECTOR, ".base-card__full-link")
            job_url = job_link.get_attribute('href')
            
            # Extract job ID from URL
            job_id_match = re.search(r'/jobs/view/(\d+)', job_url)
            external_id = job_id_match.group(1) if job_id_match else ""
            
            # Try to get posted date
            posted_date = None
            try:
                time_element = job_card.find_element(By.CSS_SELECTOR, ".job-search-card__listdate")
                posted_date = time_element.get_attribute('datetime')
            except NoSuchElementException:
                pass
            
            # Get detailed information by clicking on the job
            detailed_info = self._get_job_details(job_url)
            
            job_data = {
                'title': title,
                'company': company,
                'location': location,
                'source_url': job_url,
                'external_id': external_id,
                'source_platform': 'linkedin',
                'posted_date': posted_date,
                **detailed_info
            }
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error parsing LinkedIn job details: {e}")
            return None

    def _get_job_details(self, job_url):
        """Get detailed job information by visiting the job page"""
        details = {
            'description': '',
            'requirements': '',
            'employment_type': 'full_time',
            'experience_level': 'mid',
            'remote_type': 'on_site',
            'skills_required': [],
            'salary_min': None,
            'salary_max': None,
        }
        
        try:
            current_url = self.driver.current_url
            self.driver.get(job_url)
            self.random_delay()
            
            # Wait for job details to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".show-more-less-html__markup"))
            )
            
            # Get job description
            try:
                desc_element = self.driver.find_element(By.CSS_SELECTOR, ".show-more-less-html__markup")
                details['description'] = desc_element.text.strip()
            except NoSuchElementException:
                pass
            
            # Extract employment type and other details from the description
            description_text = details['description'].lower()
            
            # Determine employment type
            if any(term in description_text for term in ['full time', 'full-time', 'permanent']):
                details['employment_type'] = 'full_time'
            elif any(term in description_text for term in ['part time', 'part-time']):
                details['employment_type'] = 'part_time'
            elif any(term in description_text for term in ['contract', 'contractor']):
                details['employment_type'] = 'contract'
            elif any(term in description_text for term in ['intern', 'internship']):
                details['employment_type'] = 'internship'
            
            # Determine remote type
            if any(term in description_text for term in ['remote', 'work from home', 'wfh']):
                details['remote_type'] = 'remote'
            elif any(term in description_text for term in ['hybrid']):
                details['remote_type'] = 'hybrid'
            
            # Extract skills (this is a simplified approach)
            skills = self._extract_skills(details['description'])
            details['skills_required'] = skills
            
            # Go back to the search results
            self.driver.get(current_url)
            self.random_delay()
            
        except Exception as e:
            logger.error(f"Error getting LinkedIn job details: {e}")
        
        return details

    def _extract_skills(self, text):
        """Extract skills from job description"""
        # Common tech skills to look for
        tech_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'nodejs', 'django',
            'flask', 'spring', 'mysql', 'postgresql', 'mongodb', 'aws', 'azure', 'gcp',
            'docker', 'kubernetes', 'git', 'jenkins', 'terraform', 'ansible',
            'machine learning', 'data science', 'artificial intelligence', 'blockchain',
            'devops', 'agile', 'scrum', 'project management', 'digital marketing',
            'seo', 'content marketing', 'social media', 'graphic design', 'ui/ux',
            'photoshop', 'illustrator', 'figma', 'sketch'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in tech_skills:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return found_skills