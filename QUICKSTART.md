# Quick Start: Upload Your Resume & Auto-Apply

## The Easiest Way - One Command! 🚀

```bash
python main.py upload /path/to/your/resume.pdf --auto
```

That's it! Just provide your resume and Claude will do everything automatically.

## What Happens Automatically

### 1. Resume Parsing (30 seconds)
Claude extracts from your resume:
- ✅ Your name, email, phone, location
- ✅ All work experience with accomplishments
- ✅ Education and certifications
- ✅ Technical skills (Python, React, AWS, etc.)
- ✅ Soft skills (Leadership, Communication, etc.)
- ✅ Projects and achievements
- ✅ GitHub, LinkedIn, portfolio links

### 2. Job Preference Inference (15 seconds)
Claude analyzes your background and determines:
- ✅ Best job titles for you (e.g., "Senior Software Engineer", "Full Stack Developer")
- ✅ Your experience level (Entry/Mid/Senior)
- ✅ Key skills to match in job postings
- ✅ Technologies you should avoid (things not in your background)
- ✅ Realistic salary expectations
- ✅ Preferred locations (Remote, or cities from your resume)

### 3. Automatic Job Search (2-3 minutes)
System searches LinkedIn and Indeed for:
- ✅ Your top 2-3 inferred job titles
- ✅ In your preferred locations
- ✅ Matching your experience level
- ✅ Filters by match score (50%+ only)

### 4. Human Review (Your Control!)
For each matching job, you see:
- 📊 Match score (0-100%)
- 📝 Job title, company, location
- 💰 Salary (if available)
- 🎯 Matched keywords from your resume
- 📄 Full job description

You decide: **y** (apply), **n** (skip), **q** (quit)

### 5. AI Resume Generation (10 seconds per job)
For approved jobs, Claude creates:
- ✅ Tailored professional summary
- ✅ Rewritten experience bullets emphasizing relevant skills
- ✅ ATS-optimized PDF with proper formatting
- ✅ Keywords from job description incorporated

You review each PDF:
- **y** - Use this resume
- **n** - Skip this application
- **v** - View PDF before deciding

### 6. Automated Application (20-30 seconds per job)
System automatically:
- ✅ Navigates to job posting
- ✅ Detects "Easy Apply" buttons
- ✅ Fills your information
- ✅ Uploads your tailored PDF resume
- ✅ Answers screening questions
- ✅ Submits application

## Example Session

```bash
$ python main.py upload myresume.pdf --auto

======================================================================
              Resume Upload & Auto Profile Creation
======================================================================

📄 Parsing resume: myresume.pdf
✓ Extracted 3,542 characters
🤖 Analyzing resume with Claude...
✓ Found 3 work experiences
✓ Found 18 skills
🎯 Inferring job preferences...
✓ Target titles: Senior Software Engineer, Full Stack Developer, Backend Engineer
✓ Key skills: Python, React, AWS, Docker, PostgreSQL

✓ Profile created successfully!

Personal Info:
  Name: John Doe
  Email: john.doe@email.com
  Location: San Francisco, CA

Inferred Job Preferences:
  Target Titles: Senior Software Engineer, Full Stack Developer, Backend Engineer
  Locations: Remote, San Francisco, CA
  Min Salary: $150,000
  Key Skills: Python, Django, React, AWS, Docker, Kubernetes, PostgreSQL, Redis

Experience:
  • Senior Software Engineer at Tech Corp
  • Software Engineer at StartupXYZ
  • Junior Developer at CodeCo

Save this profile? (y/n): y

✓ Profile saved to config/user_profile.json

🚀 Starting automatic job search...

======================================================================
                    Scraping Jobs from LinkedIn
======================================================================

Searching for: Senior Software Engineer in Remote
Fetching up to 30 jobs...

Found 28 job listings on LinkedIn
Matching 28 jobs against your profile...
Found 15 matching jobs (score >= 50%)

✓ Saved 15 jobs to database

Top 5 Matches:
■ Senior Backend Engineer
  Company: Stripe
  Location: Remote
  Match Score: 92%
  Matched Keywords: Python, Django, AWS, PostgreSQL
  URL: https://linkedin.com/jobs/...

[... more jobs ...]

======================================================================
                      Review Scraped Jobs
======================================================================

Job 1/15

■ Senior Backend Engineer
  Company: Stripe
  Location: Remote - USA
  Platform: linkedin
  Match Score: 92%
  Matched Keywords: Python, Django, AWS, PostgreSQL, Redis
  Salary: $170,000 - $250,000

  Description:
  We're looking for a Senior Backend Engineer to join our Payments team.
  You'll build scalable APIs serving millions of requests per day...

  URL: https://linkedin.com/jobs/view/123456789

Apply to this job? (y/n/q to quit): y
✓ Added to application queue

[... review more jobs ...]

✓ Approved 8 jobs for application

Generate resumes and apply now? (y/n): y

======================================================================
            Generating Resumes & Applying to Jobs
======================================================================

[1/8] Generating resume for Senior Backend Engineer at Stripe

📄 Generating tailored resume for Senior Backend Engineer at Stripe...
✓ Using Claude 3.5 Sonnet for AI-powered resume generation
✓ Resume saved to: generated_resumes/resume_Stripe_20241123_143022.pdf

📄 Resume generated: generated_resumes/resume_Stripe_20241123_143022.pdf
✓ Format: PDF
✓ Tailored keywords: Python, Django, AWS, PostgreSQL, Redis

Use this resume? (y/n/v to view): v

[PDF opens in your viewer]

Use this resume? (y/n): y

[... generates resumes for all 8 jobs ...]

Ready to apply to 8 jobs
Proceed with applications? (y/n): y

✓ Starting application process...

======================================================================
Application 1/8
======================================================================

Navigating to job: https://linkedin.com/jobs/view/123456789
✓ Found Easy Apply button
✓ Resume uploaded: generated_resumes/resume_Stripe_20241123_143022.pdf
  Filling basic information...
  Answering common questions...
  Navigating multi-step form...
    Step 1...
    Step 2...
    Step 3...
  ✓ Application submitted successfully!

Waiting 5 seconds before next application...

[... applies to remaining jobs ...]

======================================================================
                      Application Results
======================================================================

✓ Successful: 7
✗ Failed: 1

Failed Applications:
  • Tech Lead at Meta
    Error: External application detected - manual completion may be required

$ python main.py applications

======================================================================
                      Application History
======================================================================

┌─────────────────────────────┬────────────────┬──────────┬─────────────────┐
│ Job Title                    │ Company        │ Status   │ Applied At      │
├─────────────────────────────┼────────────────┼──────────┼─────────────────┤
│ Senior Backend Engineer      │ Stripe         │ applied  │ 2024-11-23 14:35│
│ Full Stack Engineer          │ Airbnb         │ applied  │ 2024-11-23 14:38│
│ Senior Software Engineer     │ Uber           │ applied  │ 2024-11-23 14:41│
│ Backend Developer            │ DoorDash       │ applied  │ 2024-11-23 14:44│
│ Software Engineer III        │ Google         │ applied  │ 2024-11-23 14:47│
│ Senior Engineer              │ Netflix        │ applied  │ 2024-11-23 14:50│
│ Principal Engineer           │ Amazon         │ applied  │ 2024-11-23 14:53│
│ Tech Lead                    │ Meta           │ error    │ N/A             │
└─────────────────────────────┴────────────────┴──────────┴─────────────────┘

Total Applications: 8
```

## Time Breakdown

- Resume parsing: **30 seconds**
- Job search (2 platforms): **3 minutes**
- Job review (8 jobs): **5 minutes** (your time)
- Resume generation (8 PDFs): **2 minutes**
- Resume review (8 PDFs): **3 minutes** (your time)
- Applications (8 jobs): **4 minutes**

**Total: ~17 minutes for 8 high-quality applications**

Compare to manual:
- Writing custom resume: 30-60 minutes per job
- Finding jobs: 30-60 minutes
- Filling applications: 10-15 minutes per job
- **Total: 3-5 hours for 8 applications**

**Time saved: 80-90%** ⚡

## Cost with Claude

For 100 applications:
- Resume parsing: 1 resume × $0.20 = **$0.20**
- Job inference: 1 analysis × $0.10 = **$0.10**
- Resume generation: 100 resumes × $0.004 = **$0.40**

**Total: ~$0.70** 💰

## Setup Requirements

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Claude API Key
- Go to https://console.anthropic.com/
- Sign up for account
- Add $10-20 credit
- Copy API key

### 3. Configure
```bash
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=your_key_here
```

### 4. Run!
```bash
python main.py upload /path/to/resume.pdf --auto
```

## Tips for Best Results

1. **Use a Good Resume**: The better your input resume, the better Claude's parsing
2. **PDF Format**: PDFs parse more reliably than DOCX
3. **Review Carefully**: Always review AI-generated content
4. **Start Small**: Test with 3-5 jobs first
5. **Quality Over Quantity**: Better to apply to 10 great matches than 100 poor ones
6. **Check Generated PDFs**: Use 'v' to view before approving
7. **Monitor Results**: Track which resumes get responses

## Alternative Workflows

### Manual Control (No Auto)
```bash
# Step 1: Upload and create profile
python main.py upload resume.pdf

# Step 2: Search for specific jobs
python main.py scrape -p linkedin -q "Software Engineer" -l "Remote"

# Step 3: Review and apply
python main.py review

# Step 4: Check status
python main.py applications
```

### Edit Profile After Upload
```bash
# Upload to auto-generate profile
python main.py upload resume.pdf

# Fine-tune the generated profile
python main.py profile --edit

# Then search and apply
python main.py scrape
python main.py review
```

### Search Multiple Times
```bash
# Upload once
python main.py upload resume.pdf

# Search for different positions
python main.py scrape -q "Backend Engineer" -l "Remote"
python main.py scrape -q "Full Stack Developer" -l "San Francisco"
python main.py scrape -q "Python Developer" -l "New York"

# Review all at once
python main.py review
```

## Troubleshooting

**Resume parsing fails:**
- Ensure PDF or DOCX format
- Check file is not corrupted
- Try converting to PDF if DOCX

**No jobs found:**
- Claude inferred titles may be too specific
- Try manual scrape with broader titles
- Check job preferences in profile

**Applications fail:**
- Some sites require manual completion
- System will report which need manual work
- Check error messages for details

**Claude API errors:**
- Verify API key in .env
- Check credits at console.anthropic.com
- Ensure key has correct permissions

## What Gets Created

After running, you'll have:

```
auto-apply/
├── config/
│   └── user_profile.json           # Your parsed profile
├── data/
│   └── jobs.db                      # SQLite database of jobs
├── generated_resumes/
│   ├── resume_Stripe_20241123.pdf  # Tailored PDF for Stripe
│   ├── resume_Airbnb_20241123.pdf  # Tailored PDF for Airbnb
│   └── ...                          # One PDF per application
└── logs/                            # Application logs
```

All your data stays local - nothing in the cloud except Claude API calls.

## Next Steps

After your first run:
1. Check `python main.py applications` to see results
2. View generated PDFs in `generated_resumes/`
3. Edit profile if needed with `python main.py profile --edit`
4. Run again with different search terms
5. Track which resumes get responses and refine

---

**Ready to start? Just run:**

```bash
python main.py upload /path/to/your/resume.pdf --auto
```

That's all you need! Claude handles the rest. 🚀
