import re
import pdfplumber
from docx import Document
from pathlib import Path
from typing import Dict, List, Optional
from anthropic import Anthropic
from src.config import ANTHROPIC_API_KEY


class ResumeParser:
    """Parse resumes and extract structured information using Claude."""

    def __init__(self):
        if ANTHROPIC_API_KEY:
            self.claude = Anthropic(api_key=ANTHROPIC_API_KEY)
        else:
            self.claude = None
            print("⚠ Warning: Anthropic API key not set. Resume parsing will be limited.")

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF resume."""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
        return text

    def extract_text_from_docx(self, docx_path: str) -> str:
        """Extract text from DOCX resume."""
        text = ""
        try:
            doc = Document(docx_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"Error extracting DOCX text: {e}")
        return text

    def extract_text(self, resume_path: str) -> str:
        """Extract text from resume file (PDF or DOCX)."""
        path = Path(resume_path)

        if not path.exists():
            raise FileNotFoundError(f"Resume file not found: {resume_path}")

        if path.suffix.lower() == '.pdf':
            return self.extract_text_from_pdf(resume_path)
        elif path.suffix.lower() in ['.docx', '.doc']:
            return self.extract_text_from_docx(resume_path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")

    def parse_resume_with_claude(self, resume_text: str) -> Dict:
        """Use Claude to parse resume and extract structured information."""
        if not self.claude:
            return self._basic_parse(resume_text)

        try:
            prompt = f"""You are an expert resume parser. Analyze this resume and extract structured information in JSON format.

RESUME TEXT:
{resume_text[:8000]}

Extract and return ONLY a valid JSON object with this exact structure (no markdown, no explanations):

{{
  "personal_info": {{
    "name": "Full Name",
    "email": "email@example.com",
    "phone": "+1-234-567-8900",
    "location": "City, State",
    "linkedin": "https://linkedin.com/in/profile",
    "github": "https://github.com/username",
    "portfolio": "https://portfolio.com"
  }},
  "experience": [
    {{
      "title": "Job Title",
      "company": "Company Name",
      "location": "City, State",
      "start_date": "YYYY-MM",
      "end_date": "YYYY-MM or Present",
      "description": [
        "Achievement or responsibility 1",
        "Achievement or responsibility 2"
      ]
    }}
  ],
  "education": [
    {{
      "degree": "Degree Name",
      "institution": "University Name",
      "location": "City, State",
      "graduation_date": "YYYY",
      "gpa": "3.8"
    }}
  ],
  "skills": {{
    "programming_languages": ["Python", "JavaScript"],
    "frameworks": ["React", "Django"],
    "tools": ["Docker", "AWS"],
    "soft_skills": ["Leadership", "Communication"]
  }},
  "certifications": [],
  "projects": [
    {{
      "name": "Project Name",
      "description": "Brief description",
      "url": "https://github.com/user/project",
      "technologies": ["Tech1", "Tech2"]
    }}
  ]
}}

Guidelines:
- Extract ALL experience entries, not just the most recent
- Include ALL skills mentioned (technical and soft skills)
- If information is missing, use null or empty array
- Ensure all JSON is valid and properly escaped
- Return ONLY the JSON, nothing else"""

            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            import json
            json_text = response.content[0].text.strip()

            # Remove markdown code blocks if present
            json_text = re.sub(r'^```json\s*', '', json_text)
            json_text = re.sub(r'\s*```$', '', json_text)

            parsed_data = json.loads(json_text)
            return parsed_data

        except Exception as e:
            print(f"⚠ Claude parsing error: {e}")
            return self._basic_parse(resume_text)

    def _basic_parse(self, resume_text: str) -> Dict:
        """Basic resume parsing without AI (fallback)."""
        # Extract email
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        email_match = re.search(email_pattern, resume_text)
        email = email_match.group(0) if email_match else ""

        # Extract phone
        phone_pattern = r'(\+\d{1,2}\s?)?(\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}'
        phone_match = re.search(phone_pattern, resume_text)
        phone = phone_match.group(0) if phone_match else ""

        # Extract name (assume first line or first bold text)
        lines = [line.strip() for line in resume_text.split('\n') if line.strip()]
        name = lines[0] if lines else "Unknown"

        return {
            "personal_info": {
                "name": name,
                "email": email,
                "phone": phone,
                "location": "",
                "linkedin": "",
                "github": "",
                "portfolio": ""
            },
            "experience": [],
            "education": [],
            "skills": {
                "programming_languages": [],
                "frameworks": [],
                "tools": [],
                "soft_skills": []
            },
            "certifications": [],
            "projects": []
        }

    def infer_job_preferences(self, resume_data: Dict) -> Dict:
        """Use Claude to infer job preferences from resume data."""
        if not self.claude:
            return self._default_preferences()

        try:
            import json
            resume_json = json.dumps(resume_data, indent=2)

            prompt = f"""You are a career advisor. Based on this person's resume, infer their job search preferences.

RESUME DATA:
{resume_json[:6000]}

Analyze their experience, skills, and background to determine:
1. What job titles they should target
2. Appropriate experience levels
3. Key skills to match in job descriptions
4. Technologies or keywords to avoid (based on what they DON'T have experience with)
5. Likely salary range
6. Preferred locations (if mentioned or inferred from remote work history)

Return ONLY a valid JSON object with this structure:

{{
  "titles": [
    "Software Engineer",
    "Senior Developer",
    "Other relevant titles"
  ],
  "locations": [
    "Remote",
    "City, State if mentioned"
  ],
  "job_types": ["Full-time", "Contract"],
  "experience_levels": ["Mid-Level", "Senior", or "Entry-Level"],
  "salary_min": 100000,
  "keywords": [
    "Most relevant skills and technologies from their experience"
  ],
  "exclude_keywords": [
    "Technologies or areas they have NO experience with"
  ]
}}

Be specific and realistic based on their actual experience."""

            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                temperature=0.5,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            json_text = response.content[0].text.strip()
            json_text = re.sub(r'^```json\s*', '', json_text)
            json_text = re.sub(r'\s*```$', '', json_text)

            preferences = json.loads(json_text)
            return preferences

        except Exception as e:
            print(f"⚠ Error inferring preferences: {e}")
            return self._default_preferences()

    def _default_preferences(self) -> Dict:
        """Return default job preferences."""
        return {
            "titles": ["Software Engineer", "Developer"],
            "locations": ["Remote"],
            "job_types": ["Full-time"],
            "experience_levels": ["Mid-Level"],
            "salary_min": 80000,
            "keywords": [],
            "exclude_keywords": []
        }

    def parse_resume(self, resume_path: str) -> tuple[Dict, Dict]:
        """
        Parse resume and infer job preferences.

        Returns:
            Tuple of (resume_data, job_preferences)
        """
        print(f"\n📄 Parsing resume: {resume_path}")

        # Extract text
        resume_text = self.extract_text(resume_path)

        if not resume_text.strip():
            raise ValueError("No text could be extracted from the resume")

        print(f"✓ Extracted {len(resume_text)} characters")

        # Parse with Claude
        print("🤖 Analyzing resume with Claude...")
        resume_data = self.parse_resume_with_claude(resume_text)

        print(f"✓ Found {len(resume_data.get('experience', []))} work experiences")
        print(f"✓ Found {sum(len(v) if isinstance(v, list) else 0 for v in resume_data.get('skills', {}).values())} skills")

        # Infer preferences
        print("🎯 Inferring job preferences...")
        job_preferences = self.infer_job_preferences(resume_data)

        print(f"✓ Target titles: {', '.join(job_preferences.get('titles', [])[:3])}")
        print(f"✓ Key skills: {', '.join(job_preferences.get('keywords', [])[:5])}")

        return resume_data, job_preferences

    def create_user_profile(self, resume_path: str) -> Dict:
        """
        Create a complete user profile from resume.

        Returns:
            Complete profile dictionary ready to save
        """
        resume_data, job_preferences = self.parse_resume(resume_path)

        profile = {
            "personal_info": resume_data.get("personal_info", {}),
            "job_preferences": job_preferences,
            "experience": resume_data.get("experience", []),
            "education": resume_data.get("education", []),
            "skills": resume_data.get("skills", {}),
            "certifications": resume_data.get("certifications", []),
            "projects": resume_data.get("projects", [])
        }

        return profile
