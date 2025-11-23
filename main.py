#!/usr/bin/env python3
"""
Auto Job Applicant - Automated Job Application System

This tool helps automate the job application process by:
1. Scraping job listings from multiple platforms
2. Matching jobs against your profile and preferences
3. Generating tailored resumes for each position
4. Automating the application submission process

Usage:
    python main.py setup          # Initial setup
    python main.py scrape         # Scrape jobs from job boards
    python main.py review         # Review and select jobs to apply to
    python main.py applications   # View application history
    python main.py profile        # View/edit your profile
"""

from src.cli import cli

if __name__ == '__main__':
    cli()
