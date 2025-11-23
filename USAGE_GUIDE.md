# Quick Start Guide

## Step-by-Step Tutorial

### 1. Initial Setup (5 minutes)

```bash
# Install dependencies
pip install -r requirements.txt

# Run setup wizard
python main.py setup
```

### 2. Configure Your Profile (10 minutes)

Edit `config/user_profile.json`:

```bash
python main.py profile --edit
```

**What to include**:
- ✅ Your accurate work experience
- ✅ All relevant skills
- ✅ Job titles you're interested in
- ✅ Preferred locations (including "Remote")
- ✅ Minimum salary requirements
- ✅ Keywords to look for (technologies, methodologies)
- ✅ Keywords to avoid (deal-breakers)

### 3. Add API Keys (Optional but Recommended)

Edit `.env`:
```env
OPENAI_API_KEY=sk-...your-key-here...
```

Get your OpenAI API key at: https://platform.openai.com/api-keys

**Note**: Without API key, the system uses template-based resumes (still works, just less tailored).

### 4. Scrape Your First Jobs (2 minutes)

```bash
python main.py scrape --platform linkedin --query "Software Engineer" --location "Remote"
```

This will:
- Search LinkedIn for Software Engineer positions
- Filter based on your profile
- Save matching jobs to the database
- Show you the top 5 matches

### 5. Review and Apply (10-30 minutes)

```bash
python main.py review
```

**What happens**:
1. System shows you each job with details
2. You decide: **y** (apply), **n** (skip), or **q** (quit)
3. For approved jobs, system generates tailored resumes
4. You review each resume before it's used
5. System applies to all approved jobs

### 6. Track Your Applications

```bash
python main.py applications
```

View all your submitted applications with status and dates.

## Example Workflow

### Morning Job Hunt (30 minutes)

```bash
# 1. Scrape new jobs from LinkedIn
python main.py scrape -p linkedin -q "Python Developer" -l "Remote" -n 50

# 2. Scrape from Indeed
python main.py scrape -p indeed -q "Backend Engineer" -l "San Francisco, CA" -n 30

# 3. Review all scraped jobs
python main.py review

# 4. Check application status
python main.py applications
```

### Weekly Job Search Routine

**Monday Morning**:
```bash
# Cast a wide net
python main.py scrape -p linkedin -q "Your Title" -l "Remote" -n 100
```

**Monday Evening**:
```bash
# Review and apply to top matches
python main.py review
```

**Friday**:
```bash
# Check status
python main.py applications
```

## Advanced Usage

### Scraping Multiple Platforms

```bash
# LinkedIn
python main.py scrape -p linkedin -q "Data Scientist" -l "New York, NY"

# Indeed
python main.py scrape -p indeed -q "Data Scientist" -l "New York, NY"

# You can run these back-to-back to collect from multiple sources
```

### Customizing Match Criteria

Edit your `job_preferences` in the profile:

```json
{
  "job_preferences": {
    "titles": ["Senior Engineer", "Staff Engineer", "Lead Developer"],
    "locations": ["Remote", "San Francisco, CA", "Seattle, WA"],
    "job_types": ["Full-time"],
    "experience_levels": ["Senior", "Staff", "Lead"],
    "salary_min": 150000,
    "keywords": [
      "python", "kubernetes", "microservices", "aws",
      "distributed systems", "api design"
    ],
    "exclude_keywords": [
      "php", "wordpress", "drupal",
      "on-site only", "in-office"
    ]
  }
}
```

### Understanding Match Scores

- **80-100%**: Excellent match - definitely review
- **65-79%**: Good match - likely relevant
- **50-64%**: Okay match - might be relevant
- **Below 50%**: Poor match - filtered out

### Selective Application Strategy

Instead of applying to everything:

1. Run `review` and select only 5-star matches (80%+)
2. Review resumes carefully
3. Apply to 5-10 quality positions per day
4. Quality > Quantity

## Tips for Success

### 1. Profile Optimization

**Do**:
- Use industry-standard job titles
- List all relevant technologies
- Include quantified achievements
- Keep experience descriptions detailed

**Don't**:
- Use vague or inflated titles
- List outdated or irrelevant skills
- Leave sections empty

### 2. Resume Generation

**Review each resume for**:
- Accuracy of claims
- Relevance to position
- Professional tone
- Proper formatting

**Edit if needed**: Resumes are saved in `generated_resumes/` - you can edit them before applying.

### 3. Application Strategy

**Best Practices**:
- Apply to 5-10 jobs per day maximum
- Focus on quality matches (70%+ score)
- Customize your profile based on results
- Track which types of jobs get responses

**Red Flags to Skip**:
- Jobs with unclear requirements
- Companies with poor reviews
- Positions way above/below your level
- Jobs with excluded keywords

### 4. Avoiding Detection

**Be respectful of platforms**:
- Don't scrape too aggressively
- Use delays between applications (`AUTO_APPLY_DELAY=5`)
- Limit daily applications (`MAX_APPLICATIONS_PER_DAY=10`)
- Review applications manually

### 5. Improving Match Quality

If you're getting poor matches:

1. **Refine keywords**: Add more specific technologies
2. **Update job titles**: Use exact titles from job boards
3. **Expand locations**: Add more cities or "Remote"
4. **Lower minimum score**: Try 40% threshold instead of 50%

## Troubleshooting

### No Jobs Found

**Check**:
- Is your query too specific?
- Are your location preferences too narrow?
- Try broader job titles
- Lower the minimum match score

### Applications Failing

**Common Issues**:
- External company websites (harder to automate)
- Login required (add credentials to `.env`)
- Captchas (run with `headless=False` to solve manually)
- Changed website structure (update scrapers)

### Resumes Not Generating

**Check**:
- Is `OPENAI_API_KEY` set in `.env`?
- Is the API key valid?
- Do you have API credits?
- Falls back to template-based if API unavailable

### Scraper Not Working

**Try**:
- Update Chrome/ChromeDriver
- Use Playwright: `playwright install chromium`
- Run with headless=False to see browser
- Check if website structure changed

## FAQ

**Q: How many applications should I submit per day?**
A: Start with 5-10 quality applications. Quality matters more than quantity.

**Q: Will this get me banned from job sites?**
A: Possible if you abuse it. Use reasonable delays, don't spam, and respect rate limits.

**Q: Do I need an OpenAI API key?**
A: No, but it helps. Without it, resumes use templates instead of AI generation.

**Q: Can I edit resumes before applying?**
A: Yes! They're saved in `generated_resumes/` - edit before approving.

**Q: What if an application fails?**
A: Check the error message. Many external applications require manual completion.

**Q: Is my data private?**
A: Yes, everything is stored locally on your machine.

**Q: Can I use this for multiple profiles?**
A: Yes, create different profile JSON files and switch between them.

## Getting Help

- **Check README.md** for detailed documentation
- **Review error messages** - they usually indicate the issue
- **Try dry run mode** to test without actually applying
- **Start small** - test with 5 jobs before going big

---

Happy job hunting! Remember: This tool is to help you apply more efficiently, not to spam applications. Always review and approve before submitting. 🎯
