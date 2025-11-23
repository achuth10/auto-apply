import os
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path
import json
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from src.models import Job, Resume
from src.config import ANTHROPIC_API_KEY, RESUMES_DIR

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class ResumeGenerator:
    """Generate tailored resumes for job applications using Claude."""

    def __init__(self, user_profile: Dict):
        self.profile = user_profile
        self.personal_info = user_profile.get('personal_info', {})
        self.experience = user_profile.get('experience', [])
        self.education = user_profile.get('education', [])
        self.skills = user_profile.get('skills', {})
        self.projects = user_profile.get('projects', [])

        # Initialize Claude client
        if ANTHROPIC_AVAILABLE and ANTHROPIC_API_KEY:
            self.claude = Anthropic(api_key=ANTHROPIC_API_KEY)
            print("✓ Using Claude 3.5 Sonnet for AI-powered resume generation")
        else:
            self.claude = None
            print("⚠ Claude API not available, using template-based resumes")

    def generate_tailored_summary(self, job: Job) -> str:
        """Generate a tailored professional summary using Claude."""
        if not self.claude:
            return self._generate_generic_summary()

        try:
            prompt = f"""You are an expert resume writer. Create a powerful professional summary for a resume.

JOB POSTING:
Title: {job.title}
Company: {job.company}
Description: {job.description[:1500]}
Required Keywords: {', '.join(job.keywords_matched[:10])}

CANDIDATE BACKGROUND:
- Experience: {len(self.experience)} positions
- Top Skills: {', '.join(list(self.skills.get('programming_languages', []))[:5])}
- Education: {self.education[0].get('degree', '')} from {self.education[0].get('institution', '')}
- Recent Role: {self.experience[0].get('title', '')} at {self.experience[0].get('company', '')}

INSTRUCTIONS:
Write a compelling 2-3 sentence professional summary that:
1. Highlights the most relevant experience for THIS specific job
2. Incorporates key skills mentioned in the job description
3. Uses strong action words and quantifiable achievements
4. Positions the candidate as an ideal fit for this role
5. Maintains a professional, confident tone

Return ONLY the summary text, no explanations or meta-commentary."""

            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=400,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return response.content[0].text.strip()

        except Exception as e:
            print(f"⚠ Claude API error: {e}")
            return self._generate_generic_summary()

    def _generate_generic_summary(self) -> str:
        """Generate a generic professional summary."""
        years_exp = len(self.experience)
        top_skills = ', '.join(list(self.skills.get('programming_languages', []))[:3])
        return f"Experienced professional with {years_exp}+ years of expertise in {top_skills}. Proven track record of delivering high-quality solutions and driving technical excellence."

    def tailor_experience_bullets(self, job: Job) -> list:
        """Tailor experience bullet points using Claude."""
        if not self.claude:
            return self.experience

        try:
            tailored_experience = []

            for exp in self.experience[:3]:  # Focus on recent experience
                prompt = f"""You are an expert resume writer. Rewrite work experience bullets to be highly relevant for a specific job.

TARGET JOB:
Title: {job.title}
Company: {job.company}
Key Skills Needed: {', '.join(job.keywords_matched[:8])}
Requirements: {' '.join(job.requirements[:3])}

ORIGINAL EXPERIENCE:
Title: {exp.get('title')}
Company: {exp.get('company')}
Accomplishments:
{chr(10).join(f"- {bullet}" for bullet in exp.get('description', [])[:4])}

INSTRUCTIONS:
Rewrite 3-4 bullet points that:
1. Emphasize skills and technologies relevant to the target job
2. Use powerful action verbs (Led, Architected, Implemented, Optimized, etc.)
3. Include quantifiable metrics and impact
4. Align with the target company's needs
5. Demonstrate progression and leadership

Return ONLY the bullet points, one per line, without dash prefixes or numbering."""

                response = self.claude.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=600,
                    temperature=0.7,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

                content = response.content[0].text.strip()
                tailored_bullets = [b.strip() for b in content.split('\n') if b.strip()]

                tailored_exp = exp.copy()
                tailored_exp['description'] = tailored_bullets[:4]  # Limit to 4 bullets
                tailored_experience.append(tailored_exp)

            return tailored_experience

        except Exception as e:
            print(f"⚠ Claude API error: {e}")
            return self.experience[:3]

    def create_resume_pdf(self, job: Job, tailored: bool = True) -> Resume:
        """Create a tailored resume in PDF format using ReportLab."""
        filename = f"resume_{job.company.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        file_path = RESUMES_DIR / filename

        # Create PDF document
        doc = SimpleDocTemplate(
            str(file_path),
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )

        # Styles
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=RGBColor(0, 0, 0),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        contact_style = ParagraphStyle(
            'Contact',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=12
        )

        section_style = ParagraphStyle(
            'Section',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=RGBColor(0, 0, 0),
            spaceAfter=6,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )

        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            leading=14
        )

        # Build content
        content = []

        # Header - Name
        name = Paragraph(self.personal_info.get('name', 'Your Name'), title_style)
        content.append(name)

        # Contact Info
        contact_parts = []
        if self.personal_info.get('email'):
            contact_parts.append(self.personal_info['email'])
        if self.personal_info.get('phone'):
            contact_parts.append(self.personal_info['phone'])
        if self.personal_info.get('location'):
            contact_parts.append(self.personal_info['location'])

        contact_line = " | ".join(contact_parts)
        content.append(Paragraph(contact_line, contact_style))

        # Links
        links = []
        if self.personal_info.get('linkedin'):
            links.append(f"LinkedIn: {self.personal_info['linkedin']}")
        if self.personal_info.get('github'):
            links.append(f"GitHub: {self.personal_info['github']}")
        if self.personal_info.get('portfolio'):
            links.append(f"Portfolio: {self.personal_info['portfolio']}")

        if links:
            content.append(Paragraph(" | ".join(links), contact_style))

        content.append(Spacer(1, 0.2*inch))

        # Professional Summary
        if tailored:
            summary = self.generate_tailored_summary(job)
        else:
            summary = self._generate_generic_summary()

        content.append(Paragraph("PROFESSIONAL SUMMARY", section_style))
        content.append(Paragraph(summary, body_style))

        # Experience
        content.append(Paragraph("EXPERIENCE", section_style))

        experience_list = self.tailor_experience_bullets(job) if tailored else self.experience[:3]

        for exp in experience_list:
            # Job title and company
            exp_title = f"<b>{exp.get('title', '')}</b> | {exp.get('company', '')}"
            content.append(Paragraph(exp_title, body_style))

            # Location and dates
            exp_details = f"{exp.get('location', '')} | {exp.get('start_date', '')} - {exp.get('end_date', 'Present')}"
            content.append(Paragraph(exp_details, body_style))

            # Bullets
            bullets = []
            for bullet in exp.get('description', [])[:4]:
                bullets.append(ListItem(Paragraph(bullet, body_style), leftIndent=20))

            if bullets:
                bullet_list = ListFlowable(
                    bullets,
                    bulletType='bullet',
                    start='•',
                    leftIndent=10
                )
                content.append(bullet_list)

            content.append(Spacer(1, 0.1*inch))

        # Skills
        content.append(Paragraph("SKILLS", section_style))

        for skill_category, skill_list in self.skills.items():
            if skill_list:
                skill_text = f"<b>{skill_category.replace('_', ' ').title()}:</b> {', '.join(skill_list)}"
                content.append(Paragraph(skill_text, body_style))

        # Education
        content.append(Paragraph("EDUCATION", section_style))

        for edu in self.education:
            edu_text = f"<b>{edu.get('degree', '')}</b> | {edu.get('institution', '')}"
            content.append(Paragraph(edu_text, body_style))

            edu_details = f"{edu.get('location', '')} | Graduated: {edu.get('graduation_date', '')}"
            content.append(Paragraph(edu_details, body_style))

            if edu.get('gpa'):
                content.append(Paragraph(f"GPA: {edu.get('gpa')}", body_style))

        # Projects (if any)
        if self.projects:
            content.append(Paragraph("NOTABLE PROJECTS", section_style))
            for project in self.projects[:2]:
                proj_text = f"<b>{project.get('name', '')}</b>"
                if project.get('url'):
                    proj_text += f" | {project.get('url')}"
                content.append(Paragraph(proj_text, body_style))
                content.append(Paragraph(project.get('description', ''), body_style))

        # Build PDF
        doc.build(content)

        # Create Resume object
        resume = Resume(
            job_id=job.id,
            content=summary,
            format="pdf",
            tailored_keywords=job.keywords_matched,
            file_path=str(file_path)
        )

        return resume

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
        name_run.font.size = Pt(18)
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
            links.append(self.personal_info['linkedin'])
        if self.personal_info.get('github'):
            links.append(self.personal_info['github'])
        if links:
            links_para.add_run(' | '.join(links)).font.size = Pt(10)

        doc.add_paragraph()  # Spacing

        # Professional Summary
        if tailored:
            summary = self.generate_tailored_summary(job)
        else:
            summary = self._generate_generic_summary()

        summary_heading = doc.add_heading('PROFESSIONAL SUMMARY', level=1)
        summary_heading.runs[0].font.size = Pt(12)
        doc.add_paragraph(summary)

        # Experience
        exp_heading = doc.add_heading('EXPERIENCE', level=1)
        exp_heading.runs[0].font.size = Pt(12)

        experience_list = self.tailor_experience_bullets(job) if tailored else self.experience[:3]

        for exp in experience_list:
            exp_title = doc.add_paragraph()
            exp_title.add_run(f"{exp.get('title', '')} | {exp.get('company', '')}").bold = True
            exp_title.add_run(f"\n{exp.get('location', '')} | {exp.get('start_date', '')} - {exp.get('end_date', 'Present')}")

            for bullet in exp.get('description', [])[:4]:
                doc.add_paragraph(bullet, style='List Bullet')

        # Skills
        skills_heading = doc.add_heading('SKILLS', level=1)
        skills_heading.runs[0].font.size = Pt(12)

        for skill_category, skill_list in self.skills.items():
            if skill_list:
                skill_para = doc.add_paragraph()
                skill_para.add_run(f"{skill_category.replace('_', ' ').title()}: ").bold = True
                skill_para.add_run(', '.join(skill_list))

        # Education
        edu_heading = doc.add_heading('EDUCATION', level=1)
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
            content=summary,
            format="docx",
            tailored_keywords=job.keywords_matched,
            file_path=str(file_path)
        )

        return resume

    def generate_resume(self, job: Job, format: str = "pdf", tailored: bool = True) -> Resume:
        """Generate a resume for a specific job in specified format."""
        print(f"\n{'📄 Generating tailored resume' if tailored else '📄 Generating standard resume'} for {job.title} at {job.company}...")

        if format.lower() == "pdf":
            resume = self.create_resume_pdf(job, tailored=tailored)
        else:
            resume = self.create_resume_docx(job, tailored=tailored)

        print(f"✓ Resume saved to: {resume.file_path}")

        return resume
