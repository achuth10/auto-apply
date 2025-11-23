from typing import List, Dict
from src.models import Job, UserProfile


class JobMatcher:
    """Matches jobs against user profile and preferences."""

    def __init__(self, user_profile: Dict):
        self.profile = user_profile
        self.preferences = user_profile.get('job_preferences', {})

    def calculate_match_score(self, job: Job) -> float:
        """
        Calculate a match score (0-100) for a job based on user profile.

        Scoring criteria:
        - Title match: 30 points
        - Location match: 15 points
        - Keywords match: 30 points
        - No excluded keywords: 15 points
        - Job type match: 10 points
        """
        score = 0.0
        matched_keywords = []

        # 1. Title matching (30 points)
        preferred_titles = self.preferences.get('titles', [])
        title_lower = job.title.lower()
        title_score = 0
        for pref_title in preferred_titles:
            if pref_title.lower() in title_lower:
                title_score = 30
                break
            elif any(word in title_lower for word in pref_title.lower().split()):
                title_score = max(title_score, 15)
        score += title_score

        # 2. Location matching (15 points)
        preferred_locations = self.preferences.get('locations', [])
        location_lower = job.location.lower()
        for pref_location in preferred_locations:
            if pref_location.lower() in location_lower or "remote" in location_lower:
                score += 15
                break

        # 3. Keywords matching (30 points)
        keywords = self.preferences.get('keywords', [])
        job_text = f"{job.title} {job.description}".lower()

        keyword_matches = 0
        for keyword in keywords:
            if keyword.lower() in job_text:
                keyword_matches += 1
                matched_keywords.append(keyword)

        if keywords:
            keyword_score = min((keyword_matches / len(keywords)) * 30, 30)
            score += keyword_score

        # 4. Excluded keywords check (15 points if no exclusions found)
        exclude_keywords = self.preferences.get('exclude_keywords', [])
        has_exclusions = False
        for exclude_keyword in exclude_keywords:
            if exclude_keyword.lower() in job_text:
                has_exclusions = True
                break

        if not has_exclusions:
            score += 15

        # 5. Job type matching (10 points)
        preferred_job_types = self.preferences.get('job_types', [])
        if job.job_type:
            for job_type in preferred_job_types:
                if job_type.lower() in job.job_type.lower():
                    score += 10
                    break

        # Update job with match score and matched keywords
        job.match_score = round(score, 2)
        job.keywords_matched = matched_keywords

        return job.match_score

    def filter_jobs(self, jobs: List[Job], min_score: float = 50.0) -> List[Job]:
        """
        Filter and rank jobs based on match score.

        Args:
            jobs: List of jobs to filter
            min_score: Minimum match score threshold (0-100)

        Returns:
            Filtered and sorted list of jobs
        """
        # Calculate scores for all jobs
        for job in jobs:
            self.calculate_match_score(job)

        # Filter by minimum score
        filtered_jobs = [job for job in jobs if job.match_score >= min_score]

        # Sort by match score (highest first)
        filtered_jobs.sort(key=lambda x: x.match_score, reverse=True)

        return filtered_jobs

    def get_job_insights(self, job: Job) -> Dict:
        """Get insights about why a job matched."""
        insights = {
            'match_score': job.match_score,
            'matched_keywords': job.keywords_matched,
            'reasons': []
        }

        # Check title match
        preferred_titles = self.preferences.get('titles', [])
        for title in preferred_titles:
            if title.lower() in job.title.lower():
                insights['reasons'].append(f"Title matches preferred: {title}")
                break

        # Check location match
        preferred_locations = self.preferences.get('locations', [])
        for location in preferred_locations:
            if location.lower() in job.location.lower():
                insights['reasons'].append(f"Location matches: {location}")
                break

        # Add keyword matches
        if job.keywords_matched:
            insights['reasons'].append(f"Matched {len(job.keywords_matched)} skill keywords")

        return insights
