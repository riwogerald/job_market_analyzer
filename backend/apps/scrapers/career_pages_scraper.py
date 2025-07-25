from .base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
import logging

logger = logging.getLogger(__name__)

class CareerPagesScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        # List of major Kenyan companies with career pages
        self.company_urls = {
            'Safaricom': 'https://www.safaricom.co.ke/careers/current-opportunities',
            'Equity Bank': 'https://equitygroupholdings.com/careers/',
            'KCB Group': 'https://kcbgroup.com/careers/',
            'East African Breweries': 'https://www.eabl.com/careers',
            'Nation Media Group': 'https://www.nationmedia.com/careers/',
            'Bamburi Cement': 'https://www.bamburicement.co.ke/careers/',
            'Kenya Airways': 'https://www.kenya-airways.com/en/company/careers/',
            'Co-operative Bank': 'https://www.co-opbank.co.ke/careers/',
            'Standard Chartered': 'https://www.sc.com/ke/careers/',
            'Barclays Bank': 'https://www.absa.co.ke/careers/',
        }

    def scrape_jobs(self, search_term="", location="Kenya", max_pages=1):
        all_jobs = []
        
        for company_name, career_url in self.company_urls.items():
            logger.info(f"Scraping {company_name} career page: {career_url}")
            
            try:
                jobs = self._scrape_company_jobs(company_name, career_url)
                all_jobs.extend(jobs)
                self.random_delay()
            except Exception as e:
                logger.error(f"Error scraping {company_name}: {e}")
                continue
        
        return all_jobs

    def _scrape_company_jobs(self, company_name, career_url):
        jobs = []
        
        try:
            self.driver.get(career_url)
            self.random_delay()
            
            # Different strategies for different career page structures
            job_elements = []
            
            # Try common job listing selectors
            selectors = [
                '.job-listing',
                '.career-opportunity',
                '.job-opening',
                '.position',
                '[class*="job"]',
                '[class*="career"]',
                'tr[class*="job"]',
                '.vacancy'
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        job_elements = elements
                        break
                except:
                    continue
            
            # If no specific job elements found, try to extract from general content
            if not job_elements:
                job_elements = self._extract_from_general_content()
            
            for element in job_elements[:10]:  # Limit to 10 jobs per company
                try:
                    job_data = self._parse_company_job(element, company_name, career_url)
                    if job_data:
                        jobs.append(job_data)
                except Exception as e:
                    logger.error(f"Error parsing job from {company_name}: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error accessing {company_name} career page: {e}")
        
        return jobs

    def _extract_from_general_content(self):
        """Try to extract job information from general page content"""
        job_elements = []
        
        try:
            # Look for text that might indicate job titles
            elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Manager') or contains(text(), 'Officer') or contains(text(), 'Analyst') or contains(text(), 'Developer') or contains(text(), 'Engineer')]")
            job_elements = elements[:5]  # Limit results
        except:
            pass
        
        return job_elements

    def _parse_company_job(self, job_element, company_name, career_url):
        try:
            # Extract job title
            title = ""
            title_selectors = [
                '.job-title', '.title', 'h3', 'h4', 'h5',
                '[class*="title"]', 'a', 'strong'
            ]
            
            for selector in title_selectors:
                try:
                    title_elem = job_element.find_element(By.CSS_SELECTOR, selector)
                    title = title_elem.text.strip()
                    if title and len(title) > 5:  # Basic validation
                        break
                except:
                    continue
            
            # If no title found, use the element text
            if not title:
                title = job_element.text.strip()[:100]  # First 100 chars
            
            # Extract description if available
            description = ""
            try:
                desc_elem = job_element.find_element(By.CSS_SELECTOR, '.description, .summary, p')
                description = desc_elem.text.strip()
            except:
                description = job_element.text.strip()
            
            # Extract job URL if it's a link
            job_url = career_url
            try:
                link_elem = job_element.find_element(By.CSS_SELECTOR, 'a')
                href = link_elem.get_attribute('href')
                if href and href.startswith('http'):
                    job_url = href
            except:
                pass
            
            # Basic job data validation
            if not title or len(title.strip()) < 3:
                return None
            
            job_data = {
                'title': title,
                'company': company_name,
                'location': 'Kenya',  # Default to Kenya for local companies
                'description': description,
                'source_url': job_url,
                'external_id': f"{company_name.lower().replace(' ', '_')}_{hash(title) % 10000}",
                'source_platform': 'career_page',
                'employment_type': 'full_time',
                'experience_level': self._guess_experience_level(title, description),
                'remote_type': self._guess_remote_type(title, description),
                'skills_required': self._extract_skills(f"{title} {description}"),
            }
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error parsing company job details: {e}")
            return None

    def _guess_experience_level(self, title, description):
        """Guess experience level from title and description"""
        text = f"{title} {description}".lower()
        
        if any(term in text for term in ['senior', 'lead', 'principal', 'head', 'director', 'manager']):
            return 'senior'
        elif any(term in text for term in ['junior', 'entry', 'graduate', 'trainee', 'intern']):
            return 'entry'
        elif any(term in text for term in ['executive', 'ceo', 'cto', 'cfo', 'vp', 'vice president']):
            return 'executive'
        else:
            return 'mid'

    def _guess_remote_type(self, title, description):
        """Guess remote work type from title and description"""
        text = f"{title} {description}".lower()
        
        if any(term in text for term in ['remote', 'work from home', 'wfh']):
            return 'remote'
        elif any(term in text for term in ['hybrid', 'flexible']):
            return 'hybrid'
        else:
            return 'on_site'

    def _extract_skills(self, text):
        """Extract skills from job title and description"""
        tech_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'nodejs', 'django',
            'flask', 'spring', 'mysql', 'postgresql', 'mongodb', 'aws', 'azure', 'gcp',
            'docker', 'kubernetes', 'git', 'jenkins', 'terraform', 'ansible',
            'machine learning', 'data science', 'artificial intelligence', 'blockchain',
            'devops', 'agile', 'scrum', 'project management', 'digital marketing',
            'seo', 'content marketing', 'social media', 'graphic design', 'ui/ux',
            'excel', 'powerpoint', 'word', 'accounting', 'finance', 'sales', 'marketing',
            'customer service', 'human resources', 'operations', 'strategy'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in tech_skills:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return found_skills

    def parse_job_details(self, job_element):
        """Required by base class - delegates to _parse_company_job"""
        return self._parse_company_job(job_element, "Unknown", "")
