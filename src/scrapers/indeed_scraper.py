import time
from typing import List
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.scrapers.base_scraper import BaseScraper
from src.models import Job


class IndeedScraper(BaseScraper):
    """Scraper for Indeed jobs."""

    BASE_URL = "https://www.indeed.com"

    def login(self, email: str, password: str) -> bool:
        """Login to Indeed (optional for scraping)."""
        # Indeed doesn't require login for basic scraping
        return True

    def scrape_jobs(self, query: str, location: str = "", num_jobs: int = 50) -> List[Job]:
        """Scrape jobs from Indeed."""
        jobs = []

        try:
            # Build search URL
            search_url = f"{self.BASE_URL}/jobs?q={query.replace(' ', '+')}"
            if location:
                search_url += f"&l={location.replace(' ', '+')}"

            self.driver.get(search_url)
            time.sleep(3)

            # Scroll to load more jobs
            self.scroll_page(times=3)

            # Find all job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".job_seen_beacon, .jobsearch-SerpJobCard, .resultContent")

            print(f"Found {len(job_cards)} job listings on Indeed")

            for idx, card in enumerate(job_cards[:num_jobs]):
                try:
                    # Extract job details
                    title_elem = card.find_element(By.CSS_SELECTOR, "h2.jobTitle, .jobTitle span")
                    title = title_elem.text.strip()

                    company_elem = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name'], .companyName")
                    company = company_elem.text.strip()

                    location_elem = card.find_element(By.CSS_SELECTOR, "[data-testid='text-location'], .companyLocation")
                    job_location = location_elem.text.strip()

                    # Get job URL
                    job_link = card.find_element(By.CSS_SELECTOR, "a.jcs-JobTitle")
                    job_url = job_link.get_attribute("href")
                    if not job_url.startswith("http"):
                        job_url = self.BASE_URL + job_url

                    # Get snippet/description
                    try:
                        description_elem = card.find_element(By.CSS_SELECTOR, ".job-snippet, .jobCardShelfContainer")
                        description = description_elem.text.strip()
                    except:
                        description = ""

                    # Try to get salary if available
                    salary = ""
                    try:
                        salary_elem = card.find_element(By.CSS_SELECTOR, ".salary-snippet, .metadata.salary-snippet-container")
                        salary = salary_elem.text.strip()
                    except:
                        pass

                    # Create job object
                    if title and company:
                        job = Job(
                            id=self.generate_job_id(job_url, title, company),
                            title=title,
                            company=company,
                            location=job_location or location,
                            description=description[:5000] if description else "",
                            requirements=[],
                            url=job_url,
                            platform="indeed",
                            salary_range=salary if salary else None,
                            scraped_at=datetime.now()
                        )
                        jobs.append(job)
                        print(f"  [{idx + 1}] {title} at {company}")

                except Exception as e:
                    print(f"  Error scraping job card: {e}")
                    continue

                # Add delay to avoid being blocked
                time.sleep(1)

        except Exception as e:
            print(f"Error scraping Indeed jobs: {e}")

        return jobs
