# Auto Job Applicant 🤖

An intelligent, fully automated job application system powered by **Claude 3.5 Sonnet**. Simply upload your resume and let AI handle the rest - from parsing your experience to generating tailored PDFs to applying to jobs.

## ✨ NEW: One-Command Job Search

```bash
# Upload your resume and automatically start applying to jobs
python main.py upload myresume.pdf --auto
```

That's it! Claude will:
1. Extract all information from your resume
2. Infer what jobs you should apply for based on your experience
3. Search LinkedIn and Indeed for matching positions
4. Generate tailored PDF resumes for each job
5. Ask for your approval before applying
6. Submit applications automatically

## Features

- **🤖 Powered by Claude 3.5 Sonnet**: State-of-the-art AI for resume parsing, generation, and job matching
- **📄 Automatic Resume Parsing**: Upload PDF/DOCX resume, Claude extracts everything automatically
- **🎯 Smart Job Inference**: AI analyzes your background and determines the best job targets
- **🔍 Multi-Platform Job Scraping**: Automatically search LinkedIn, Indeed, and more
- **📑 AI-Generated PDF Resumes**: Claude creates professionally formatted, ATS-optimized PDFs tailored to each position
- **✅ Human-in-the-Loop**: Review and approve jobs and resumes before submission
- **🚀 Automated Applications**: Navigate forms and submit applications automatically
- **📊 Application Tracking**: Track all your applications in a local database
- **🔒 Privacy-Focused**: All data stored locally on your machine

## Quick Start

### 1. Install

```bash
# Clone the repository
git clone <repository-url>
cd auto-apply

# Install dependencies
pip install -r requirements.txt
```

### 2. Get Claude API Key

Get your Anthropic API key at: https://console.anthropic.com/

Add $10-20 credit (enough for hundreds of applications)

### 3. Configure

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Claude API key
# ANTHROPIC_API_KEY=your_key_here
```

### 4. Upload Resume & Start Applying

```bash
# Automatic mode - does everything for you
python main.py upload /path/to/resume.pdf --auto

# Or manual mode - upload first, then control the process
python main.py upload /path/to/resume.pdf
python main.py scrape  # Search for jobs
python main.py review  # Apply to jobs
```

## How It Works

### Automatic Mode (`--auto` flag)

```bash
python main.py upload resume.pdf --auto
```

1. **Resume Parsing**: Claude extracts your:
   - Contact information
   - Work experience with accomplishments
   - Education and certifications
   - Technical and soft skills
   - Projects and achievements

2. **Job Preference Inference**: Claude analyzes your background to determine:
   - Best job titles to target (e.g., "Senior Software Engineer", "Full Stack Developer")
   - Appropriate experience level (Entry/Mid/Senior)
   - Key technologies to match (Python, React, AWS, etc.)
   - Technologies to avoid (things you don't have experience with)
   - Realistic salary expectations
   - Preferred work arrangements (Remote, specific cities)

3. **Automatic Job Search**: System searches LinkedIn/Indeed for:
   - Top 2-3 inferred job titles
   - In your preferred locations
   - Matching your experience level

4. **Job Matching**: Each job gets a match score (0-100%) based on:
   - Title alignment (30 points)
   - Location match (15 points)
   - Keyword overlap (30 points)
   - No excluded keywords (15 points)
   - Job type match (10 points)

5. **Resume Generation**: For each approved job, Claude creates:
   - Tailored professional summary emphasizing relevant experience
   - Rewritten experience bullets highlighting applicable skills
   - ATS-optimized PDF with keyword optimization
   - Professional formatting

6. **Human Approval**: You review:
   - Each job (with match score and insights)
   - Each generated PDF resume
   - Option to view PDFs before approving

7. **Automated Application**: System:
   - Detects "Easy Apply" buttons
   - Fills personal information
   - Uploads your tailored resume
   - Answers screening questions
   - Submits applications

## Commands

### `upload` - Upload Resume & Create Profile

```bash
# Interactive mode
python main.py upload

# With file path
python main.py upload /path/to/resume.pdf

# Automatic mode (upload + search + apply)
python main.py upload resume.pdf --auto
```

### `scrape` - Search for Jobs

```bash
# Interactive (will prompt for job title)
python main.py scrape

# With parameters
python main.py scrape -p linkedin -q "Software Engineer" -l "Remote" -n 50

# Search Indeed
python main.py scrape -p indeed -q "Python Developer" -l "San Francisco"
```

### `review` - Review and Apply to Jobs

```bash
python main.py review
```

Shows each job with:
- Job details and description
- Match score and insights
- Option to apply (y/n/q)

For approved jobs:
- Generates tailored PDF resume
- Shows resume for approval
- Option to view PDF (v)
- Submits applications

### `applications` - View Application History

```bash
python main.py applications
```

Shows table of:
- Job title and company
- Application status
- Date applied

### `profile` - View/Edit Profile

```bash
# View profile
python main.py profile

# Edit profile
python main.py profile --edit
```

### `setup` - Initial Setup Wizard

```bash
python main.py setup
```

## Project Structure

```
auto-apply/
├── main.py                          # CLI entry point
├── requirements.txt                 # Dependencies
├── .env                            # Your API keys (gitignored)
├── config/
│   └── user_profile.json           # Your profile (auto-generated)
├── src/
│   ├── cli.py                      # Interactive CLI
│   ├── models.py                   # Data models
│   ├── matcher.py                  # Job matching algorithm
│   ├── resume_generator.py        # AI resume generation (Claude)
│   ├── resume_parser.py           # Resume parsing (Claude)
│   ├── database.py                # SQLite operations
│   ├── scrapers/
│   │   ├── linkedin_scraper.py    # LinkedIn scraper
│   │   └── indeed_scraper.py      # Indeed scraper
│   └── automation/
│       ├── applicator.py          # Application automation
│       └── application_filler.py  # Form filling logic
├── data/                          # SQLite database
├── generated_resumes/             # Your tailored PDFs
└── application_history/           # Application records
```

## Why Claude?

This system uses **Claude 3.5 Sonnet** exclusively for several reasons:

1. **Superior Resume Parsing**: Claude excels at extracting structured information from unstructured text
2. **Context Understanding**: 200K token context window allows processing entire resumes and job descriptions
3. **Professional Writing**: Claude produces professional, accurate resume content without hallucinations
4. **Cost-Effective**: ~$3 per million tokens (vs $10 for GPT-4)
5. **Reliable**: Consistent, high-quality outputs with strong safety features

### Cost Estimate

For 100 job applications:
- Resume parsing: $0.20
- Job preference inference: $0.10
- Resume generation (100 tailored resumes): $0.40
- **Total: ~$0.70 for 100 applications**

Extremely cost-effective compared to manual application time!

## Advanced Features

### Generated PDF Resumes

Claude generates professional PDF resumes with:
- Clean, ATS-friendly formatting
- Tailored professional summary for each job
- Rewritten experience bullets emphasizing relevant skills
- Keyword optimization for applicant tracking systems
- Consistent formatting and styling

PDFs are saved in `generated_resumes/` for your records.

### Job Matching Algorithm

Scoring breakdown (0-100%):
- **Title Match (30%)**: Job title matches your target roles
- **Location Match (15%)**: Location matches preferences or remote
- **Keyword Match (30%)**: Your skills appear in job description
- **Exclusion Check (15%)**: No deal-breaker keywords found
- **Job Type (10%)**: Full-time, contract, etc. matches preference

Jobs scoring 50%+ are considered good matches.

### Application Automation

The system can:
- Detect "Easy Apply" buttons (LinkedIn, Indeed)
- Navigate multi-step application forms
- Fill personal information fields
- Upload resume files
- Answer common screening questions
- Submit applications automatically

**Note**: Some external company portals may require manual completion.

## Safety & Privacy

- ✅ All data stored locally on your machine
- ✅ No data sent to third parties (except Anthropic API for AI processing)
- ✅ Human approval required for every job and resume
- ✅ Rate limiting to avoid platform detection
- ✅ Configurable daily application limits
- ✅ Dry-run mode for testing

## Configuration

### Environment Variables (`.env`)

```env
# Required
ANTHROPIC_API_KEY=your_anthropic_key

# Optional - for LinkedIn/Indeed login
LINKEDIN_EMAIL=your_email
LINKEDIN_PASSWORD=your_password
INDEED_EMAIL=your_email
INDEED_PASSWORD=your_password

# Application settings
AUTO_APPLY_DELAY=5
MAX_APPLICATIONS_PER_DAY=10
```

### User Profile

Auto-generated when you upload your resume, or manually edit `config/user_profile.json`:

```json
{
  "personal_info": { ... },
  "job_preferences": {
    "titles": ["Software Engineer", "Full Stack Developer"],
    "locations": ["Remote", "San Francisco, CA"],
    "job_types": ["Full-time"],
    "experience_levels": ["Mid-Level", "Senior"],
    "salary_min": 120000,
    "keywords": ["python", "react", "aws"],
    "exclude_keywords": ["php", "wordpress"]
  },
  "experience": [ ... ],
  "education": [ ... ],
  "skills": { ... },
  "projects": [ ... ]
}
```

## Tips for Best Results

1. **Start with Upload**: Use `upload --auto` for fastest results
2. **Review Carefully**: Always review generated resumes - AI can make mistakes
3. **Quality Over Quantity**: Apply to 5-10 well-matched jobs rather than 100 poor matches
4. **Monitor Results**: Track which resumes get responses and refine your profile
5. **Use LinkedIn Login**: Provides access to more complete job details
6. **Check Generated PDFs**: Use 'v' to view PDFs before approving

## Troubleshooting

### Resume Upload Fails

- Ensure resume is in PDF or DOCX format
- Check that file path is correct
- Try converting to PDF if DOCX fails

### Claude API Errors

- Verify API key in `.env`
- Check you have credits: https://console.anthropic.com/
- Ensure API key has correct permissions

### Job Scraping Issues

- Some sites implement anti-bot measures
- Try with LinkedIn/Indeed credentials
- Use delays between requests
- Run with headless=False to see what's happening

### Application Submission Fails

- Many companies use external portals (harder to automate)
- System will report which applications need manual completion
- Check error messages for specific issues

## Legal & Ethical Considerations

⚠️ **Important**:

- This tool is for personal use only
- Respect Terms of Service of job platforms
- Don't spam applications - apply only to relevant positions
- Review all resumes and applications before submission
- Be honest in your applications
- Some platforms prohibit automation - use at your own risk

**Use responsibly!** This tool helps automate tedious tasks, but you should always review everything before submission.

## Contributing

Contributions welcome! Areas for improvement:

- Additional job board scrapers (Glassdoor, Monster, etc.)
- Better form field detection
- Cover letter generation
- Interview scheduling integration
- Email tracking for responses
- Analytics dashboard

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the documentation

## Roadmap

- [ ] More job board integrations
- [ ] AI-generated cover letters
- [ ] Email integration for response tracking
- [ ] Browser extension
- [ ] Mobile app
- [ ] Analytics and insights dashboard
- [ ] Interview preparation tools

---

**Powered by Claude 3.5 Sonnet** 🤖

Happy job hunting! Remember: This tool helps automate the tedious parts, but always review and approve everything before submission. Quality over quantity!
