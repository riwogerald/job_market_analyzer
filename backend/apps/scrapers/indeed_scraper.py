from .base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
import logging

logger = logging.getLogger(__name__)

class IndeedScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://ke.indeed.com/jobs"

    def scrape_jobs(self, search_term="", location="Nairobi", max_pages=5):
        jobs = []
        
        try:
            for page in range(max_pages):
                start = page * 10
                search_url = f"{self.base_url}?q={search_term}&l={location}&start={start}"
                
                logger.info(f"Scraping Indeed page {page + 1}: {search_url}")
                
                self.driver.get(search_url)
                self.random_delay()
                
                # Wait for job listings
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-jk]"))
                    )
                except TimeoutException:
                    logger.warning(f"Timeout waiting for Indeed job listings on page {page + 1}")
                    continue
                
                # Get job cards
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, "[data-jk]")
                
                for card in job_cards:
                    try:
                        job_data = self.parse_job_details(card)
                        if job_data:
                            jobs.append(job_data)
                    except Exception as e:
                        logger.error(f"Error parsing Indeed job card: {e}")
                        continue
                
                self.random_delay()
        
        except Exception as e:
            logger.error(f"Error scraping Indeed: {e}")
        
        return jobs

    def parse_job_details(self, job_card):
        try:
            # Get job ID
            job_id = job_card.get_attribute('data-jk')
            
            # Extract title
            title_element = job_card.find_element(By.CSS_SELECTOR, "[data-testid='job-title'] a")
            title = title_element.text.strip()
            
            # Extract company
            try:
                company_element = job_card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']")
                company = company_element.text.strip()
            except NoSuchElementException:
                company = "Unknown"
            
            # Extract location
            try:
                location_element = job_card.find_element(By.CSS_SELECTOR, "[data-testid='job-location']")
                location = location_element.text.strip()
            except NoSuchElementException:
                location = "Kenya"
            
            # Extract salary if available
            salary_min, salary_max = None, None
            try:
                salary_element = job_card.find_element(By.CSS_SELECTOR, "[data-testid='attribute_snippet_testid']")
                salary_text = salary_element.text
                salary_min, salary_max = self._parse_salary(salary_text)
            except NoSuchElementException:
                pass
            
            # Get job URL
            job_url = f"https://ke.indeed.com/viewjob?jk={job_id}"
            
            # Extract job snippet/description
            description = ""
            try:
                desc_element = job_card.find_element(By.CSS_SELECTOR, "[data-testid='job-snippet']")
                description = desc_element.text.strip()
            except NoSuchElementException:
                pass
            
            job_data = {
                'title': title,
                'company': company,
                'location': location,
                'description': description,
                'source_url': job_url,
                'external_id': job_id,
                'source_platform': 'indeed',
                'salary_min': salary_min,
                'salary_max': salary_max,
                'employment_type': 'full_time',
                'experience_level': 'mid',
                'remote_type': 'on_site',
                'skills_required': self._extract_skills(description),
            }
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error parsing Indeed job details: {e}")
            return None

    def _parse_salary(self, salary_text):
        """Parse salary information from text"""
        salary_min, salary_max = None, None
        
        # Remove currency symbols and extract numbers
        numbers = re.findall(r'[\d,]+', salary_text.replace(',', ''))
        
        if len(numbers) >= 2:
            try:
                salary_min = float(numbers[0].replace(',', ''))
                salary_max = float(numbers[1].replace(',', ''))
            except ValueError:
                pass
        elif len(numbers) == 1:
            try:
                salary_min = salary_max = float(numbers[0].replace(',', ''))
            except ValueError:
                pass
        
        return salary_min, salary_max

    def _extract_skills(self, text):
        """Extract skills from job description"""
        tech_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'nodejs', 'django',
            'flask', 'spring', 'mysql', 'postgresql', 'mongodb', 'aws', 'azure', 'gcp',
            'docker', 'kubernetes', 'git', 'jenkins', 'terraform', 'ansible',
            'machine learning', 'data science', 'artificial intelligence', 'blockchain',
            'devops', 'agile', 'scrum', 'project management', 'digital marketing',
            'seo', 'content marketing', 'social media', 'graphic design', 'ui/ux'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in tech_skills:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return found_skills