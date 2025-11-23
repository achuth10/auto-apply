import sqlite3
import json
from datetime import datetime
from typing import List, Optional
from src.models import Job, Application, ApplicationStatus
from src.config import DB_PATH


class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initialize database schema."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Jobs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                description TEXT,
                requirements TEXT,
                url TEXT UNIQUE,
                platform TEXT,
                job_type TEXT,
                salary_range TEXT,
                posted_date TEXT,
                scraped_at TEXT,
                match_score REAL,
                keywords_matched TEXT
            )
        ''')

        # Applications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id TEXT PRIMARY KEY,
                job_id TEXT,
                job_title TEXT,
                company TEXT,
                status TEXT,
                resume_id TEXT,
                applied_at TEXT,
                notes TEXT,
                error_message TEXT,
                FOREIGN KEY (job_id) REFERENCES jobs (id)
            )
        ''')

        # Resumes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resumes (
                id TEXT PRIMARY KEY,
                job_id TEXT,
                content TEXT,
                format TEXT,
                created_at TEXT,
                tailored_keywords TEXT,
                file_path TEXT,
                FOREIGN KEY (job_id) REFERENCES jobs (id)
            )
        ''')

        conn.commit()
        conn.close()

    def save_job(self, job: Job):
        """Save a job to the database."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO jobs
            (id, title, company, location, description, requirements, url, platform,
             job_type, salary_range, posted_date, scraped_at, match_score, keywords_matched)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            job.id, job.title, job.company, job.location, job.description,
            json.dumps(job.requirements), job.url, job.platform,
            job.job_type, job.salary_range,
            job.posted_date.isoformat() if job.posted_date else None,
            job.scraped_at.isoformat(),
            job.match_score, json.dumps(job.keywords_matched)
        ))

        conn.commit()
        conn.close()

    def get_jobs(self, status: Optional[str] = None, limit: int = 50) -> List[Job]:
        """Get jobs from database."""
        conn = self.get_connection()
        cursor = conn.cursor()

        if status:
            # Get jobs with specific application status
            cursor.execute('''
                SELECT j.* FROM jobs j
                LEFT JOIN applications a ON j.id = a.job_id
                WHERE a.status = ? OR a.status IS NULL
                ORDER BY j.scraped_at DESC
                LIMIT ?
            ''', (status, limit))
        else:
            cursor.execute('''
                SELECT * FROM jobs
                ORDER BY scraped_at DESC
                LIMIT ?
            ''', (limit,))

        rows = cursor.fetchall()
        conn.close()

        jobs = []
        for row in rows:
            job_dict = dict(row)
            job_dict['requirements'] = json.loads(job_dict['requirements'])
            job_dict['keywords_matched'] = json.loads(job_dict['keywords_matched'])
            jobs.append(Job(**job_dict))

        return jobs

    def save_application(self, application: Application):
        """Save an application to the database."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO applications
            (id, job_id, job_title, company, status, resume_id, applied_at, notes, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            application.id, application.job_id, application.job_title, application.company,
            application.status.value, application.resume_id,
            application.applied_at.isoformat() if application.applied_at else None,
            application.notes, application.error_message
        ))

        conn.commit()
        conn.close()

    def get_applications(self, status: Optional[ApplicationStatus] = None) -> List[Application]:
        """Get applications from database."""
        conn = self.get_connection()
        cursor = conn.cursor()

        if status:
            cursor.execute('''
                SELECT * FROM applications WHERE status = ?
                ORDER BY applied_at DESC
            ''', (status.value,))
        else:
            cursor.execute('''
                SELECT * FROM applications ORDER BY applied_at DESC
            ''')

        rows = cursor.fetchall()
        conn.close()

        applications = []
        for row in rows:
            app_dict = dict(row)
            app_dict['status'] = ApplicationStatus(app_dict['status'])
            applications.append(Application(**app_dict))

        return applications

    def get_job_by_id(self, job_id: str) -> Optional[Job]:
        """Get a specific job by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM jobs WHERE id = ?', (job_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            job_dict = dict(row)
            job_dict['requirements'] = json.loads(job_dict['requirements'])
            job_dict['keywords_matched'] = json.loads(job_dict['keywords_matched'])
            return Job(**job_dict)
        return None
