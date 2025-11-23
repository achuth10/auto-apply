import click
from colorama import init, Fore, Style
from tabulate import tabulate
from typing import List
import time
from pathlib import Path

from src.models import Job, Resume, Application
from src.config import load_user_profile, save_user_profile
from src.database import Database
from src.matcher import JobMatcher
from src.resume_generator import ResumeGenerator
from src.automation.applicator import JobApplicator
from src.scrapers.linkedin_scraper import LinkedInScraper
from src.scrapers.indeed_scraper import IndeedScraper

# Initialize colorama for colored terminal output
init()


class AutoJobApplicant:
    """Main application class."""

    def __init__(self):
        self.db = Database()
        self.user_profile = load_user_profile()
        self.matcher = None
        self.resume_generator = None
        self.applicator = None

        if self.user_profile:
            self.matcher = JobMatcher(self.user_profile)
            self.resume_generator = ResumeGenerator(self.user_profile)
            self.applicator = JobApplicator(self.user_profile)

    def display_header(self, text: str):
        """Display a formatted header."""
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{text.center(70)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

    def display_job(self, job: Job, detailed: bool = False):
        """Display job information."""
        print(f"\n{Fore.GREEN}■{Style.RESET_ALL} {Fore.YELLOW}{job.title}{Style.RESET_ALL}")
        print(f"  Company: {job.company}")
        print(f"  Location: {job.location}")
        print(f"  Platform: {job.platform}")

        if job.match_score:
            color = Fore.GREEN if job.match_score >= 70 else Fore.YELLOW if job.match_score >= 50 else Fore.RED
            print(f"  Match Score: {color}{job.match_score}%{Style.RESET_ALL}")

        if job.keywords_matched:
            print(f"  Matched Keywords: {', '.join(job.keywords_matched[:5])}")

        if job.salary_range:
            print(f"  Salary: {job.salary_range}")

        if detailed:
            print(f"\n  {Fore.CYAN}Description:{Style.RESET_ALL}")
            print(f"  {job.description[:300]}..." if len(job.description) > 300 else f"  {job.description}")

        print(f"  {Fore.BLUE}URL:{Style.RESET_ALL} {job.url}")

    def scrape_jobs_workflow(self, platform: str, query: str, location: str, num_jobs: int):
        """Workflow for scraping jobs."""
        self.display_header(f"Scraping Jobs from {platform.title()}")

        # Initialize scraper
        if platform == "linkedin":
            scraper = LinkedInScraper(headless=True)
        elif platform == "indeed":
            scraper = IndeedScraper(headless=True)
        else:
            print(f"{Fore.RED}✗ Unknown platform: {platform}{Style.RESET_ALL}")
            return

        try:
            scraper.init_driver()

            # Login if credentials available
            if platform == "linkedin":
                from src.config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD
                if LINKEDIN_EMAIL and LINKEDIN_PASSWORD:
                    print("Logging in to LinkedIn...")
                    scraper.login(LINKEDIN_EMAIL, LINKEDIN_PASSWORD)

            # Scrape jobs
            print(f"\nSearching for: {query} in {location or 'any location'}")
            print(f"Fetching up to {num_jobs} jobs...\n")

            jobs = scraper.scrape_jobs(query, location, num_jobs)

            # Filter and rank jobs
            if self.matcher:
                print(f"\nMatching {len(jobs)} jobs against your profile...")
                filtered_jobs = self.matcher.filter_jobs(jobs, min_score=50)
                print(f"Found {len(filtered_jobs)} matching jobs (score >= 50%)\n")
            else:
                filtered_jobs = jobs

            # Save to database
            for job in filtered_jobs:
                self.db.save_job(job)

            print(f"{Fore.GREEN}✓ Saved {len(filtered_jobs)} jobs to database{Style.RESET_ALL}")

            # Display top matches
            if filtered_jobs:
                print(f"\n{Fore.CYAN}Top 5 Matches:{Style.RESET_ALL}")
                for job in filtered_jobs[:5]:
                    self.display_job(job)

        finally:
            scraper.close_driver()

    def review_jobs_workflow(self):
        """Workflow for reviewing scraped jobs."""
        self.display_header("Review Scraped Jobs")

        # Get jobs that haven't been reviewed
        jobs = self.db.get_jobs(limit=100)

        if not jobs:
            print(f"{Fore.YELLOW}No jobs found. Run 'scrape' first.{Style.RESET_ALL}")
            return

        # Get existing applications
        existing_apps = {app.job_id: app for app in self.db.get_applications()}

        # Filter out already applied jobs
        pending_jobs = [job for job in jobs if job.id not in existing_apps]

        if not pending_jobs:
            print(f"{Fore.YELLOW}No pending jobs to review. All jobs have been processed.{Style.RESET_ALL}")
            return

        print(f"Found {len(pending_jobs)} jobs to review\n")

        approved_jobs = []

        for idx, job in enumerate(pending_jobs, 1):
            print(f"\n{Fore.CYAN}Job {idx}/{len(pending_jobs)}{Style.RESET_ALL}")
            self.display_job(job, detailed=True)

            # Ask user if they want to apply
            response = input(f"\n{Fore.GREEN}Apply to this job? (y/n/q to quit): {Style.RESET_ALL}").lower().strip()

            if response == 'y':
                approved_jobs.append(job)
                print(f"{Fore.GREEN}✓ Added to application queue{Style.RESET_ALL}")
            elif response == 'q':
                break
            else:
                print(f"{Fore.YELLOW}⊗ Skipped{Style.RESET_ALL}")

        if approved_jobs:
            print(f"\n{Fore.GREEN}✓ Approved {len(approved_jobs)} jobs for application{Style.RESET_ALL}")

            # Ask if user wants to proceed with applications
            proceed = input(f"\n{Fore.CYAN}Generate resumes and apply now? (y/n): {Style.RESET_ALL}").lower().strip()

            if proceed == 'y':
                self.apply_to_jobs_workflow(approved_jobs)

    def apply_to_jobs_workflow(self, jobs: List[Job]):
        """Workflow for applying to jobs."""
        self.display_header("Generating Resumes & Applying to Jobs")

        if not self.resume_generator:
            print(f"{Fore.RED}✗ Resume generator not initialized. Check user profile.{Style.RESET_ALL}")
            return

        # Generate resumes
        resumes = {}
        for idx, job in enumerate(jobs, 1):
            print(f"\n[{idx}/{len(jobs)}] Generating resume for {job.title} at {job.company}")

            resume = self.resume_generator.generate_resume(job, format="pdf", tailored=True)
            resumes[job.id] = resume

            # Show resume to user for approval
            print(f"\n{Fore.CYAN}📄 Resume generated:{Style.RESET_ALL} {resume.file_path}")
            print(f"✓ Format: PDF")
            print(f"✓ Tailored keywords: {', '.join(resume.tailored_keywords[:5])}")

            # Ask for approval
            approve = input(f"{Fore.GREEN}Use this resume? (y/n/v to view): {Style.RESET_ALL}").lower().strip()

            if approve == 'v':
                # Open the PDF for viewing
                import subprocess
                import platform
                try:
                    if platform.system() == 'Darwin':  # macOS
                        subprocess.run(['open', resume.file_path])
                    elif platform.system() == 'Windows':
                        subprocess.run(['start', resume.file_path], shell=True)
                    else:  # Linux
                        subprocess.run(['xdg-open', resume.file_path])
                    approve = input(f"{Fore.GREEN}Use this resume? (y/n): {Style.RESET_ALL}").lower().strip()
                except:
                    print("Could not open file viewer")

            if approve != 'y':
                print(f"{Fore.YELLOW}⊗ Resume rejected, skipping application{Style.RESET_ALL}")
                jobs.remove(job)

        if not jobs:
            print(f"\n{Fore.YELLOW}No jobs to apply to.{Style.RESET_ALL}")
            return

        # Confirm before applying
        print(f"\n{Fore.CYAN}Ready to apply to {len(jobs)} jobs{Style.RESET_ALL}")
        final_confirm = input(f"{Fore.GREEN}Proceed with applications? (y/n): {Style.RESET_ALL}").lower().strip()

        if final_confirm != 'y':
            print(f"{Fore.YELLOW}⊗ Applications cancelled{Style.RESET_ALL}")
            return

        # Apply to jobs
        print(f"\n{Fore.GREEN}Starting application process...{Style.RESET_ALL}")

        applications = self.applicator.batch_apply(jobs, resumes, dry_run=False, delay=5)

        # Save applications to database
        for app in applications:
            self.db.save_application(app)

        # Display results
        self.display_header("Application Results")

        successful = [app for app in applications if app.status.value == "applied"]
        failed = [app for app in applications if app.status.value == "error"]

        print(f"{Fore.GREEN}✓ Successful: {len(successful)}{Style.RESET_ALL}")
        print(f"{Fore.RED}✗ Failed: {len(failed)}{Style.RESET_ALL}")

        if failed:
            print(f"\n{Fore.YELLOW}Failed Applications:{Style.RESET_ALL}")
            for app in failed:
                print(f"  • {app.job_title} at {app.company}")
                print(f"    Error: {app.error_message}")

    def view_applications_workflow(self):
        """View application history."""
        self.display_header("Application History")

        applications = self.db.get_applications()

        if not applications:
            print(f"{Fore.YELLOW}No applications found.{Style.RESET_ALL}")
            return

        # Create table
        table_data = []
        for app in applications[:20]:  # Show last 20
            status_color = Fore.GREEN if app.status.value == "applied" else Fore.RED
            table_data.append([
                app.job_title[:30],
                app.company[:20],
                f"{status_color}{app.status.value}{Style.RESET_ALL}",
                app.applied_at.strftime("%Y-%m-%d %H:%M") if app.applied_at else "N/A"
            ])

        print(tabulate(table_data, headers=["Job Title", "Company", "Status", "Applied At"], tablefmt="grid"))

        print(f"\n{Fore.CYAN}Total Applications: {len(applications)}{Style.RESET_ALL}")


@click.group()
def cli():
    """Auto Job Applicant - Automate your job search and applications."""
    pass


@cli.command()
@click.option('--platform', '-p', default='linkedin', help='Job platform (linkedin, indeed)')
@click.option('--query', '-q', prompt='Job title or keywords', help='Job search query')
@click.option('--location', '-l', default='', help='Job location')
@click.option('--num-jobs', '-n', default=50, help='Number of jobs to scrape')
def scrape(platform, query, location, num_jobs):
    """Scrape jobs from job boards."""
    app = AutoJobApplicant()
    app.scrape_jobs_workflow(platform, query, location, num_jobs)


@cli.command()
def review():
    """Review scraped jobs and select which to apply to."""
    app = AutoJobApplicant()
    app.review_jobs_workflow()


@cli.command()
def applications():
    """View application history."""
    app = AutoJobApplicant()
    app.view_applications_workflow()


@cli.command()
@click.option('--edit', is_flag=True, help='Open profile in editor')
def profile(edit):
    """View or edit user profile."""
    from src.config import USER_PROFILE_PATH
    import json

    if edit:
        click.edit(filename=str(USER_PROFILE_PATH))
    else:
        profile_data = load_user_profile()
        if profile_data:
            print(json.dumps(profile_data, indent=2))
        else:
            print(f"{Fore.YELLOW}No profile found. Create one at {USER_PROFILE_PATH}{Style.RESET_ALL}")


@cli.command()
@click.argument('resume_path', type=click.Path(exists=True), required=False)
@click.option('--auto', is_flag=True, help='Automatically start job search after parsing')
def upload(resume_path, auto):
    """Upload your resume and automatically create profile. Optionally start job search."""
    from src.resume_parser import ResumeParser
    from src.config import save_user_profile, USER_PROFILE_PATH
    import json

    if not resume_path:
        resume_path = click.prompt('Enter path to your resume (PDF or DOCX)')

    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'Resume Upload & Auto Profile Creation'.center(70)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

    parser = ResumeParser()

    try:
        # Parse resume and infer preferences
        profile = parser.create_user_profile(resume_path)

        # Show extracted info
        print(f"\n{Fore.GREEN}✓ Profile created successfully!{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}Personal Info:{Style.RESET_ALL}")
        print(f"  Name: {profile['personal_info'].get('name', 'N/A')}")
        print(f"  Email: {profile['personal_info'].get('email', 'N/A')}")
        print(f"  Location: {profile['personal_info'].get('location', 'N/A')}")

        print(f"\n{Fore.CYAN}Inferred Job Preferences:{Style.RESET_ALL}")
        prefs = profile['job_preferences']
        print(f"  Target Titles: {', '.join(prefs.get('titles', [])[:3])}")
        print(f"  Locations: {', '.join(prefs.get('locations', []))}")
        print(f"  Min Salary: ${prefs.get('salary_min', 0):,}")
        print(f"  Key Skills: {', '.join(prefs.get('keywords', [])[:8])}")

        print(f"\n{Fore.CYAN}Experience:{Style.RESET_ALL}")
        for exp in profile['experience'][:3]:
            print(f"  • {exp.get('title', '')} at {exp.get('company', '')}")

        # Ask to save
        save = input(f"\n{Fore.GREEN}Save this profile? (y/n): {Style.RESET_ALL}").lower().strip()

        if save == 'y':
            save_user_profile(profile)
            print(f"\n{Fore.GREEN}✓ Profile saved to {USER_PROFILE_PATH}{Style.RESET_ALL}")

            if auto:
                # Automatically start job search
                print(f"\n{Fore.CYAN}🚀 Starting automatic job search...{Style.RESET_ALL}\n")

                app = AutoJobApplicant()

                # Use inferred titles for search
                for title in prefs.get('titles', [])[:2]:  # Search for top 2 titles
                    location = prefs.get('locations', ['Remote'])[0]
                    print(f"\n{Fore.YELLOW}Searching for: {title} in {location}{Style.RESET_ALL}")

                    app.scrape_jobs_workflow('linkedin', title, location, 30)

                # Start review process
                print(f"\n{Fore.CYAN}Starting job review process...{Style.RESET_ALL}")
                app.review_jobs_workflow()

            else:
                print(f"\n{Fore.CYAN}Next Steps:{Style.RESET_ALL}")
                print(f"  1. Run: {Fore.GREEN}python main.py scrape{Style.RESET_ALL} to find jobs")
                print(f"  2. Run: {Fore.GREEN}python main.py review{Style.RESET_ALL} to apply")
                print(f"\n Or use: {Fore.GREEN}python main.py upload <resume> --auto{Style.RESET_ALL} to do everything automatically!")

        else:
            print(f"\n{Fore.YELLOW}Profile not saved. You can edit it manually at {USER_PROFILE_PATH}{Style.RESET_ALL}")

    except Exception as e:
        print(f"\n{Fore.RED}✗ Error parsing resume: {e}{Style.RESET_ALL}")
        print(f"\nPlease check that your resume is in PDF or DOCX format and try again.")


@cli.command()
def setup():
    """Initial setup wizard."""
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'Auto Job Applicant - Setup Wizard'.center(70)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

    print("Welcome! Let's set up your profile.\n")

    # Check if profile exists
    from src.config import USER_PROFILE_PATH
    if USER_PROFILE_PATH.exists():
        print(f"{Fore.GREEN}✓ Profile already exists at {USER_PROFILE_PATH}{Style.RESET_ALL}")
        print(f"\nEdit it with: {Fore.CYAN}python main.py profile --edit{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠ No profile found{Style.RESET_ALL}")
        print(f"\nA sample profile has been created at: {USER_PROFILE_PATH}")
        print(f"Please edit it with your information and preferences.\n")

    # Check .env file
    from src.config import BASE_DIR
    env_path = BASE_DIR / ".env"
    if not env_path.exists():
        print(f"\n{Fore.YELLOW}⚠ No .env file found{Style.RESET_ALL}")
        print(f"Copy .env.example to .env and add your API key:\n")
        print(f"  cp .env.example .env")
        print(f"  # Then add your Anthropic API key\n")
    else:
        print(f"\n{Fore.GREEN}✓ .env file found{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}✨ NEW: Upload Resume Feature!{Style.RESET_ALL}")
    print(f"  Simply upload your resume and let Claude do the rest:")
    print(f"  {Fore.GREEN}python main.py upload /path/to/resume.pdf --auto{Style.RESET_ALL}")
    print(f"\n  This will:")
    print(f"    1. Extract all info from your resume")
    print(f"    2. Infer what jobs you should apply for")
    print(f"    3. Automatically search and apply to matching jobs")

    print(f"\n{Fore.CYAN}Manual Workflow:{Style.RESET_ALL}")
    print(f"  1. Upload resume: {Fore.GREEN}python main.py upload resume.pdf{Style.RESET_ALL}")
    print(f"  2. Or edit config/user_profile.json manually")
    print(f"  3. Run: {Fore.GREEN}python main.py scrape{Style.RESET_ALL}")
    print(f"  4. Run: {Fore.GREEN}python main.py review{Style.RESET_ALL}")
    print(f"\nFor help: {Fore.GREEN}python main.py --help{Style.RESET_ALL}\n")


if __name__ == '__main__':
    cli()
