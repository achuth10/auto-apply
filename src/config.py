import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
RESUMES_DIR = BASE_DIR / "generated_resumes"
HISTORY_DIR = BASE_DIR / "application_history"

# Create directories if they don't exist
for directory in [DATA_DIR, LOGS_DIR, RESUMES_DIR, HISTORY_DIR, CONFIG_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Job Platform Credentials
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL", "")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD", "")
INDEED_EMAIL = os.getenv("INDEED_EMAIL", "")
INDEED_PASSWORD = os.getenv("INDEED_PASSWORD", "")

# Application Settings
AUTO_APPLY_DELAY = int(os.getenv("AUTO_APPLY_DELAY", "5"))
MAX_APPLICATIONS_PER_DAY = int(os.getenv("MAX_APPLICATIONS_PER_DAY", "10"))

# Database
DB_PATH = DATA_DIR / "jobs.db"

# User Profile
USER_PROFILE_PATH = CONFIG_DIR / "user_profile.json"


def load_user_profile():
    """Load user profile from JSON file."""
    if USER_PROFILE_PATH.exists():
        with open(USER_PROFILE_PATH, 'r') as f:
            return json.load(f)
    return None


def save_user_profile(profile: dict):
    """Save user profile to JSON file."""
    with open(USER_PROFILE_PATH, 'w') as f:
        json.dump(profile, f, indent=2)
