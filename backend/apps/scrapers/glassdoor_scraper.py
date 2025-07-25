from .base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
import logging

logger = logging.getLogger(__name__)

class GlassdoorScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.glassdoor.com/Job/jobs.htm"

    def scrape_jobs(self, search_term="", location="Kenya", max_pages=5):
        jobs = []
        
        try:
            for page in range(max_pages):
                search_url = f"{self.base_url}?sc.keyword={search_term}&locT=C&locId=115&p={page + 1}"
                
                logger.info(f"Scraping Glassdoor page {page + 1}: {search_url}")
                
                self.driver.get(search_url)
                self.random_delay()
                
                # Wait for job listings
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='jobListing']"))
                    )
                except TimeoutException:
                    logger.warning(f"Timeout waiting for Glassdoor job listings on page {page + 1}")
                    continue
                
                # Get job cards
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, "[data-test='jobListing']")
                
                for card in job_cards:
                    try:
                        job_data = self.parse_job_details(card)
                        if job_data:
                            jobs.append(job_data)
                    except Exception as e:
                        logger.error(f"Error parsing Glassdoor job card: {e}")
                        continue
                
                self.random_delay()
        
        except Exception as e:
            logger.error(f"Error scraping Glassdoor: {e}")
        
        return jobs

    def parse_job_details(self, job_card):
        try:
            # Extract title
            title_element = job_card.find_element(By.CSS_SELECTOR, "[data-test='job-title']")
            title = title_element.text.strip()
            
            # Extract company
            try:
                company_element = job_card.find_element(By.CSS_SELECTOR, "[data-test='employer-name']")
                company = company_element.text.strip()
            except NoSuchElementException:
                company = "Unknown"
            
            # Extract location
            try:
                location_element = job_card.find_element(By.CSS_SELECTOR, "[data-test='job-location']")
                location = location_element.text.strip()
            except NoSuchElementException:
                location = "Kenya"
            
            # Extract salary if available
            salary_min, salary_max = None, None
            try:
                salary_element = job_card.find_element(By.CSS_SELECTOR, "[data-test='detailSalary']")
                salary_text = salary_element.text
                salary_min, salary_max = self._parse_salary(salary_text)
            except NoSuchElementException:
                pass
            
            # Get job URL
            try:
                link_element = job_card.find_element(By.CSS_SELECTOR, "[data-test='job-title'] a")
                job_url = link_element.get_attribute('href')
                # Extract job ID from URL
                job_id_match = re.search(r'jobListingId=(\d+)', job_url)
                external_id = job_id_match.group(1) if job_id_match else ""
            except NoSuchElementException:
                job_url = ""
                external_id = ""
            
            # Extract job description snippet
            description = ""
            try:
                desc_element = job_card.find_element(By.CSS_SELECTOR, "[data-test='job-desc']")
                description = desc_element.text.strip()
            except NoSuchElementException:
                pass
            
            job_data = {
                'title': title,
                'company': company,
                'location': location,
                'description': description,
                'source_url': job_url,
                'external_id': external_id,
                'source_platform': 'glassdoor',
                'salary_min': salary_min,
                'salary_max': salary_max,
                'employment_type': 'full_time',
                'experience_level': 'mid',
                'remote_type': 'on_site',
                'skills_required': self._extract_skills(description),
            }
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error parsing Glassdoor job details: {e}")
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
