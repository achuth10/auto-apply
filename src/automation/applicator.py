import time
from typing import Dict, Tuple
from datetime import datetime
from src.models import Job, Resume, Application, ApplicationStatus
from src.automation.application_filler import ApplicationFiller
from src.scrapers.base_scraper import BaseScraper


class JobApplicator:
    """Main class for automating job applications."""

    def __init__(self, user_profile: Dict, headless: bool = False):
        self.user_profile = user_profile
        self.headless = headless
        self.scraper = BaseScraper(headless=headless)
        self.driver = None

    def init_browser(self):
        """Initialize browser for automation."""
        self.driver = self.scraper.init_driver()
        return self.driver

    def close_browser(self):
        """Close browser."""
        if self.scraper:
            self.scraper.close_driver()
        self.driver = None

    def apply_to_job(self, job: Job, resume: Resume, dry_run: bool = False) -> Tuple[bool, str]:
        """
        Apply to a job posting.

        Args:
            job: Job to apply to
            resume: Resume to use
            dry_run: If True, only navigate to the page without submitting

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.driver:
            self.init_browser()

        try:
            print(f"\nNavigating to job: {job.url}")
            self.driver.get(job.url)
            time.sleep(3)

            # Initialize application filler
            filler = ApplicationFiller(self.driver, self.user_profile)

            # Strategy 1: Try to find Easy Apply button (LinkedIn, Indeed)
            easy_apply_button = filler.detect_easy_apply_button()

            if easy_apply_button:
                print("✓ Found Easy Apply button")

                if dry_run:
                    return True, "Dry run: Easy Apply button found, would proceed with application"

                # Click Easy Apply
                easy_apply_button.click()
                time.sleep(2)

                # Upload resume
                if resume.file_path:
                    filler.upload_resume(resume.file_path)

                # Fill basic information
                filler.fill_basic_info()

                # Answer common questions
                filler.answer_common_questions()

                # Handle multi-step form
                success = filler.handle_multi_step_form()

                if success:
                    return True, "Application submitted successfully via Easy Apply"
                else:
                    return False, "Could not complete multi-step form"

            else:
                # Strategy 2: Look for standard Apply button and external application
                print("Easy Apply not found, looking for standard application...")

                apply_buttons = self.driver.find_elements_by_xpath(
                    "//button[contains(text(), 'Apply')] | //a[contains(text(), 'Apply')]"
                )

                if apply_buttons:
                    if dry_run:
                        return True, "Dry run: Standard apply button found, would proceed with external application"

                    print("✓ Found standard Apply button")
                    apply_buttons[0].click()
                    time.sleep(3)

                    # Check if redirected to external site
                    if job.url not in self.driver.current_url:
                        print(f"  Redirected to external application: {self.driver.current_url}")

                        # Try to fill form on external site
                        filler.fill_basic_info()

                        if resume.file_path:
                            filler.upload_resume(resume.file_path)

                        filler.answer_common_questions()

                        # Note: External applications are harder to automate
                        # Return partial success
                        return False, "External application detected - manual completion may be required"

                    return False, "Could not complete standard application"

                else:
                    return False, "No apply button found on page"

        except Exception as e:
            error_msg = f"Error during application: {str(e)}"
            print(f"✗ {error_msg}")
            return False, error_msg

    def create_application_record(self, job: Job, resume: Resume, success: bool, message: str) -> Application:
        """Create an application record."""
        import uuid

        status = ApplicationStatus.APPLIED if success else ApplicationStatus.ERROR

        application = Application(
            id=str(uuid.uuid4()),
            job_id=job.id,
            job_title=job.title,
            company=job.company,
            status=status,
            resume_id=resume.file_path,
            applied_at=datetime.now() if success else None,
            notes=message,
            error_message=message if not success else None
        )

        return application

    def batch_apply(self, jobs: list, resumes: dict, dry_run: bool = False, delay: int = 5) -> list:
        """
        Apply to multiple jobs.

        Args:
            jobs: List of Job objects
            resumes: Dictionary mapping job.id to Resume object
            dry_run: If True, don't actually submit applications
            delay: Delay in seconds between applications

        Returns:
            List of Application objects
        """
        applications = []

        try:
            self.init_browser()

            for idx, job in enumerate(jobs, 1):
                print(f"\n{'='*60}")
                print(f"Application {idx}/{len(jobs)}")
                print(f"{'='*60}")

                if job.id not in resumes:
                    print(f"✗ No resume found for job: {job.title}")
                    continue

                resume = resumes[job.id]

                # Apply to job
                success, message = self.apply_to_job(job, resume, dry_run=dry_run)

                # Create application record
                application = self.create_application_record(job, resume, success, message)
                applications.append(application)

                # Delay between applications
                if idx < len(jobs):
                    print(f"\nWaiting {delay} seconds before next application...")
                    time.sleep(delay)

        finally:
            self.close_browser()

        return applications
