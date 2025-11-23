from abc import ABC, abstractmethod
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import hashlib
from src.models import Job


class BaseScraper(ABC):
    """Base class for job scrapers."""

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver = None

    def init_driver(self):
        """Initialize Selenium WebDriver."""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

        self.driver = webdriver.Chrome(options=chrome_options)
        return self.driver

    def close_driver(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def generate_job_id(self, url: str, title: str, company: str) -> str:
        """Generate a unique job ID."""
        unique_string = f"{url}_{title}_{company}"
        return hashlib.md5(unique_string.encode()).hexdigest()

    def wait_for_element(self, by: By, value: str, timeout: int = 10):
        """Wait for an element to be present."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def safe_find_element(self, by: By, value: str, default=""):
        """Safely find an element and return its text."""
        try:
            element = self.driver.find_element(by, value)
            return element.text.strip()
        except:
            return default

    def safe_get_attribute(self, element, attribute: str, default=""):
        """Safely get an attribute from an element."""
        try:
            return element.get_attribute(attribute) or default
        except:
            return default

    def scroll_page(self, times: int = 3):
        """Scroll the page to load more content."""
        for _ in range(times):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

    @abstractmethod
    def scrape_jobs(self, query: str, location: str, num_jobs: int = 50) -> List[Job]:
        """
        Scrape jobs from the platform.

        Args:
            query: Job title or keywords to search for
            location: Location to search in
            num_jobs: Maximum number of jobs to scrape

        Returns:
            List of Job objects
        """
        pass

    @abstractmethod
    def login(self, email: str, password: str) -> bool:
        """
        Login to the platform.

        Args:
            email: User email
            password: User password

        Returns:
            True if login successful, False otherwise
        """
        pass
