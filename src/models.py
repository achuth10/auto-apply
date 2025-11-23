from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum


class JobType(str, Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    INTERNSHIP = "Internship"


class ApplicationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    APPLIED = "applied"
    ERROR = "error"


class Job(BaseModel):
    id: str
    title: str
    company: str
    location: str
    description: str
    requirements: List[str] = []
    url: str
    platform: str  # 'linkedin', 'indeed', 'glassdoor', etc.
    job_type: Optional[str] = None
    salary_range: Optional[str] = None
    posted_date: Optional[datetime] = None
    scraped_at: datetime = Field(default_factory=datetime.now)
    match_score: Optional[float] = None
    keywords_matched: List[str] = []


class UserProfile(BaseModel):
    personal_info: Dict
    job_preferences: Dict
    experience: List[Dict]
    education: List[Dict]
    skills: Dict
    certifications: List[Dict] = []
    projects: List[Dict] = []


class Resume(BaseModel):
    job_id: str
    content: str
    format: str = "docx"  # docx, pdf, txt
    created_at: datetime = Field(default_factory=datetime.now)
    tailored_keywords: List[str] = []
    file_path: Optional[str] = None


class Application(BaseModel):
    id: str
    job_id: str
    job_title: str
    company: str
    status: ApplicationStatus
    resume_id: Optional[str] = None
    applied_at: Optional[datetime] = None
    notes: Optional[str] = None
    error_message: Optional[str] = None
