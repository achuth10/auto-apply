import time
from typing import List
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from src.scrapers.base_scraper import BaseScraper
from src.models import Job


class LinkedInScraper(BaseScraper):
    """Scraper for LinkedIn jobs."""

    BASE_URL = "https://www.linkedin.com"
    JOBS_URL = "https://www.linkedin.com/jobs/search/"

    def login(self, email: str, password: str) -> bool:
        """Login to LinkedIn."""
        try:
            self.driver.get(f"{self.BASE_URL}/login")
            time.sleep(2)

            # Enter email
            email_field = self.wait_for_element(By.ID, "username")
            email_field.send_keys(email)

            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(password)

            # Click login button
            password_field.send_keys(Keys.RETURN)
            time.sleep(5)

            # Check if login successful
            if "/feed" in self.driver.current_url or "/jobs" in self.driver.current_url:
                print("✓ LinkedIn login successful")
                return True
            else:
                print("✗ LinkedIn login failed")
                return False

        except Exception as e:
            print(f"✗ LinkedIn login error: {e}")
            return False

    def scrape_jobs(self, query: str, location: str = "", num_jobs: int = 50) -> List[Job]:
        """Scrape jobs from LinkedIn."""
        jobs = []

        try:
            # Build search URL
            search_params = f"?keywords={query.replace(' ', '%20')}"
            if location:
                search_params += f"&location={location.replace(' ', '%20')}"

            url = f"{self.JOBS_URL}{search_params}"
            self.driver.get(url)
            time.sleep(3)

            # Scroll to load more jobs
            self.scroll_page(times=5)

            # Find all job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".job-card-container, .jobs-search-results__list-item")

            print(f"Found {len(job_cards)} job listings on LinkedIn")

            for idx, card in enumerate(job_cards[:num_jobs]):
                try:
                    # Click on job card to load details
                    card.click()
                    time.sleep(2)

                    # Extract job details
                    title = self.safe_find_element(By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__job-title, h1.t-24")
                    company = self.safe_find_element(By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__company-name, .jobs-unified-top-card__company-name")
                    location_elem = self.safe_find_element(By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__bullet, .jobs-unified-top-card__bullet")

                    # Get job URL
                    try:
                        job_link = card.find_element(By.CSS_SELECTOR, "a")
                        job_url = job_link.get_attribute("href")
                    except:
                        job_url = self.driver.current_url

                    # Get description
                    description = self.safe_find_element(By.CSS_SELECTOR, ".jobs-description-content__text, .jobs-box__html-content")

                    # Extract requirements (simplified)
                    requirements = []
                    if description:
                        # Look for common requirement indicators
                        desc_lower = description.lower()
                        if "bachelor" in desc_lower or "degree" in desc_lower:
                            requirements.append("Bachelor's degree or equivalent")
                        if "years of experience" in desc_lower or "years experience" in desc_lower:
                            requirements.append("Professional experience required")

                    # Get job type
                    job_type = self.safe_find_element(By.CSS_SELECTOR, ".jobs-unified-top-card__job-insight")

                    # Create job object
                    if title and company:
                        job = Job(
                            id=self.generate_job_id(job_url, title, company),
                            title=title,
                            company=company,
                            location=location_elem or location,
                            description=description[:5000] if description else "",  # Limit description length
                            requirements=requirements,
                            url=job_url,
                            platform="linkedin",
                            job_type=job_type if job_type else None,
                            scraped_at=datetime.now()
                        )
                        jobs.append(job)
                        print(f"  [{idx + 1}] {title} at {company}")

                except Exception as e:
                    print(f"  Error scraping job card: {e}")
                    continue

        except Exception as e:
            print(f"Error scraping LinkedIn jobs: {e}")

        return jobs
