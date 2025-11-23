import os
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path
import json
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from src.models import Job, Resume
from src.config import OPENAI_API_KEY, ANTHROPIC_API_KEY, AI_PROVIDER, RESUMES_DIR

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class ResumeGenerator:
    """Generate tailored resumes for job applications."""

    def __init__(self, user_profile: Dict, ai_provider: str = None):
        self.profile = user_profile
        self.personal_info = user_profile.get('personal_info', {})
        self.experience = user_profile.get('experience', [])
        self.education = user_profile.get('education', [])
        self.skills = user_profile.get('skills', {})
        self.projects = user_profile.get('projects', [])

        # Determine which AI provider to use
        self.ai_provider = ai_provider or AI_PROVIDER or "openai"
        self.ai_client = None

        if self.ai_provider == "anthropic" and ANTHROPIC_AVAILABLE and ANTHROPIC_API_KEY:
            self.ai_client = Anthropic(api_key=ANTHROPIC_API_KEY)
            self.ai_type = "anthropic"
            print("Using Claude (Anthropic) for resume generation")
        elif self.ai_provider == "openai" and OPENAI_AVAILABLE and OPENAI_API_KEY:
            self.ai_client = OpenAI(api_key=OPENAI_API_KEY)
            self.ai_type = "openai"
            print("Using OpenAI GPT for resume generation")
        else:
            self.ai_type = None
            print("No AI provider available, using template-based resumes")

    def generate_tailored_summary(self, job: Job) -> str:
        """Generate a tailored professional summary using AI."""
        if not self.ai_client:
            # Fallback: generic summary
            return self._generate_generic_summary()

        try:
            prompt = f"""
Create a professional summary (2-3 sentences) for a resume tailored to this job:

Job Title: {job.title}
Company: {job.company}
Job Description: {job.description[:1000]}

Candidate Background:
- Experience: {len(self.experience)} positions
- Top Skills: {', '.join(list(self.skills.get('programming_languages', []))[:5])}
- Education: {self.education[0].get('degree', '')} from {self.education[0].get('institution', '')}

Write a compelling summary that highlights relevant experience and skills for this specific role.
Keep it concise and professional.
"""

            if self.ai_type == "anthropic":
                # Use Claude
                response = self.ai_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=300,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.content[0].text.strip()

            elif self.ai_type == "openai":
                # Use OpenAI GPT
                response = self.ai_client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[
                        {"role": "system", "content": "You are a professional resume writer. Create compelling, concise professional summaries."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error generating AI summary: {e}")
            return self._generate_generic_summary()

    def _generate_generic_summary(self) -> str:
        """Generate a generic professional summary."""
        years_exp = len(self.experience)
        top_skills = ', '.join(list(self.skills.get('programming_languages', []))[:3])

        return f"Experienced professional with {years_exp}+ years of expertise in {top_skills}. Proven track record of delivering high-quality solutions and driving technical excellence."

    def tailor_experience_bullets(self, job: Job) -> list:
        """Tailor experience bullet points to match job requirements."""
        if not self.ai_client:
            return self.experience

        try:
            # Get top 2-3 most relevant experiences
            tailored_experience = []

            for exp in self.experience[:3]:  # Focus on recent experience
                prompt = f"""
Given this job posting and work experience, rewrite the experience bullets to be more relevant:

Job Title: {job.title}
Job Requirements: {' '.join(job.requirements[:3])}
Key Skills Needed: {', '.join(job.keywords_matched[:5])}

Original Experience:
Title: {exp.get('title')}
Company: {exp.get('company')}
Bullets:
{chr(10).join(f"- {bullet}" for bullet in exp.get('description', [])[:4])}

Rewrite 3-4 bullet points that emphasize relevant skills and achievements for this specific job.
Use action verbs and quantify achievements where possible.
Return only the bullet points, one per line, without the dash prefix.
"""

                if self.ai_type == "anthropic":
                    # Use Claude
                    response = self.ai_client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=500,
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
                    content = response.content[0].text.strip()

                elif self.ai_type == "openai":
                    # Use OpenAI GPT
                    response = self.ai_client.chat.completions.create(
                        model="gpt-4-turbo-preview",
                        messages=[
                            {"role": "system", "content": "You are a professional resume writer. Tailor experience bullets to job requirements."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=300,
                        temperature=0.7
                    )
                    content = response.choices[0].message.content.strip()

                tailored_bullets = content.split('\n')
                tailored_bullets = [b.strip() for b in tailored_bullets if b.strip()]

                tailored_exp = exp.copy()
                tailored_exp['description'] = tailored_bullets
                tailored_experience.append(tailored_exp)

            return tailored_experience

        except Exception as e:
            print(f"Error tailoring experience: {e}")
            return self.experience

    def create_resume_docx(self, job: Job, tailored: bool = True) -> Resume:
        """Create a tailored resume in DOCX format."""
        doc = Document()

        # Set margins
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(0.5)
            section.bottom_margin = Inches(0.5)
            section.left_margin = Inches(0.75)
            section.right_margin = Inches(0.75)

        # Header - Name
        name_para = doc.add_paragraph()
        name_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        name_run = name_para.add_run(self.personal_info.get('name', 'Your Name'))
        name_run.font.size = Pt(16)
        name_run.bold = True

        # Contact Info
        contact_para = doc.add_paragraph()
        contact_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        contact_info = f"{self.personal_info.get('email', '')} | {self.personal_info.get('phone', '')} | {self.personal_info.get('location', '')}"
        contact_para.add_run(contact_info).font.size = Pt(10)

        # Links
        links_para = doc.add_paragraph()
        links_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        links = []
        if self.personal_info.get('linkedin'):
            links.append(f"LinkedIn: {self.personal_info['linkedin']}")
        if self.personal_info.get('github'):
            links.append(f"GitHub: {self.personal_info['github']}")
        links_para.add_run(' | '.join(links)).font.size = Pt(10)

        doc.add_paragraph()  # Spacing

        # Professional Summary
        if tailored:
            summary = self.generate_tailored_summary(job)
        else:
            summary = self._generate_generic_summary()

        summary_heading = doc.add_heading('Professional Summary', level=1)
        summary_heading.runs[0].font.size = Pt(12)
        doc.add_paragraph(summary)

        # Experience
        exp_heading = doc.add_heading('Experience', level=1)
        exp_heading.runs[0].font.size = Pt(12)

        experience_list = self.tailor_experience_bullets(job) if tailored else self.experience

        for exp in experience_list[:3]:  # Show top 3 experiences
            exp_title = doc.add_paragraph()
            exp_title.add_run(f"{exp.get('title', '')} | {exp.get('company', '')}").bold = True
            exp_title.add_run(f"\n{exp.get('location', '')} | {exp.get('start_date', '')} - {exp.get('end_date', 'Present')}")

            for bullet in exp.get('description', [])[:4]:
                doc.add_paragraph(bullet, style='List Bullet')

        # Skills
        skills_heading = doc.add_heading('Skills', level=1)
        skills_heading.runs[0].font.size = Pt(12)

        for skill_category, skill_list in self.skills.items():
            if skill_list:
                skill_para = doc.add_paragraph()
                skill_para.add_run(f"{skill_category.replace('_', ' ').title()}: ").bold = True
                skill_para.add_run(', '.join(skill_list))

        # Education
        edu_heading = doc.add_heading('Education', level=1)
        edu_heading.runs[0].font.size = Pt(12)

        for edu in self.education:
            edu_para = doc.add_paragraph()
            edu_para.add_run(f"{edu.get('degree', '')} | {edu.get('institution', '')}").bold = True
            edu_para.add_run(f"\n{edu.get('location', '')} | Graduated: {edu.get('graduation_date', '')}")

        # Save document
        filename = f"resume_{job.company.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        file_path = RESUMES_DIR / filename

        doc.save(str(file_path))

        # Create Resume object
        resume = Resume(
            job_id=job.id,
            content=summary,  # Store summary as content
            format="docx",
            tailored_keywords=job.keywords_matched,
            file_path=str(file_path)
        )

        return resume

    def generate_resume(self, job: Job, tailored: bool = True) -> Resume:
        """Generate a resume for a specific job."""
        print(f"\n{'Generating tailored resume' if tailored else 'Generating standard resume'} for {job.title} at {job.company}...")

        resume = self.create_resume_docx(job, tailored=tailored)

        print(f"✓ Resume saved to: {resume.file_path}")

        return resume
