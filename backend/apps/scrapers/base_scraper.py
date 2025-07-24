import time
import random
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import logging

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    def __init__(self, headless=True, delay_range=(2, 5)):
        self.ua = UserAgent()
        self.delay_range = delay_range
        self.driver = self._setup_driver(headless)

    def _setup_driver(self, headless):
        options = Options()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'--user-agent={self.ua.random}')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    def random_delay(self):
        time.sleep(random.uniform(*self.delay_range))

    def close(self):
        if self.driver:
            self.driver.quit()

    @abstractmethod
    def scrape_jobs(self, search_term, location, max_pages=5):
        pass

    @abstractmethod
    def parse_job_details(self, job_element):
        pass