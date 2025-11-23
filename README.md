# Auto Job Applicant 🤖

An intelligent, automated job application system that scrapes job listings, matches them to your profile, generates tailored resumes, and applies on your behalf - all with your approval.

## Features

- **🔍 Multi-Platform Job Scraping**: Automatically scrape jobs from LinkedIn, Indeed, and more
- **🎯 Smart Matching**: AI-powered job matching based on your skills, experience, and preferences
- **📄 Tailored Resume Generation**: Automatically generate customized resumes for each position using AI
- **🤖 Automated Applications**: Navigate application forms and submit applications automatically
- **✅ Human-in-the-Loop**: Review and approve jobs and resumes before applying
- **📊 Application Tracking**: Track all your applications in one place
- **🔒 Privacy-Focused**: All data stored locally on your machine

## How It Works

1. **Configure Your Profile**: Set up your experience, skills, and job preferences
2. **Scrape Jobs**: Search for relevant positions across multiple job boards
3. **Review Matches**: Review AI-matched jobs with scores and insights
4. **Generate Resumes**: AI creates tailored resumes for each position
5. **Approve & Apply**: Review resumes and approve applications
6. **Track Progress**: Monitor all your applications in one dashboard

## Installation

### Prerequisites

- Python 3.8 or higher
- Chrome browser (for Selenium automation)
- OpenAI API key (optional, for AI resume generation)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd auto-apply
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers (alternative to Selenium):
```bash
playwright install chromium
```

4. Run the setup wizard:
```bash
python main.py setup
```

5. Configure your profile:
```bash
# Edit the user profile with your information
nano config/user_profile.json
# or
python main.py profile --edit
```

6. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
nano .env
```

## Configuration

### User Profile (`config/user_profile.json`)

Edit this file to include:
- **Personal Information**: Name, email, phone, location, LinkedIn, GitHub
- **Job Preferences**: Desired titles, locations, job types, salary requirements
- **Experience**: Your work history with detailed accomplishments
- **Education**: Degrees and certifications
- **Skills**: Programming languages, frameworks, tools
- **Projects**: Notable projects and achievements

### Environment Variables (`.env`)

```env
# OpenAI API Key for resume generation
OPENAI_API_KEY=your_openai_api_key_here

# Job Platform Credentials (optional)
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password

# Application Settings
AUTO_APPLY_DELAY=5
MAX_APPLICATIONS_PER_DAY=10
```

## Usage

### 1. Scrape Jobs

Search for jobs on LinkedIn or Indeed:

```bash
# Interactive mode (will prompt for query)
python main.py scrape

# With parameters
python main.py scrape --platform linkedin --query "Software Engineer" --location "Remote" --num-jobs 50

# Indeed
python main.py scrape --platform indeed --query "Python Developer" --location "San Francisco, CA"
```

### 2. Review and Apply

Review scraped jobs and select which to apply to:

```bash
python main.py review
```

This will:
1. Show you each matching job with details and match score
2. Ask if you want to apply to each job
3. Generate tailored resumes for approved jobs
4. Show you each resume for approval
5. Submit applications to approved jobs

### 3. View Application History

Track all your applications:

```bash
python main.py applications
```

### 4. Manage Profile

View or edit your profile:

```bash
# View profile
python main.py profile

# Edit profile
python main.py profile --edit
```

## Project Structure

```
auto-apply/
├── main.py                      # Entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── config/
│   └── user_profile.json        # User profile configuration
├── src/
│   ├── cli.py                   # CLI interface
│   ├── config.py                # Configuration management
│   ├── database.py              # SQLite database operations
│   ├── models.py                # Data models
│   ├── matcher.py               # Job matching logic
│   ├── resume_generator.py     # AI resume generation
│   ├── scrapers/
│   │   ├── base_scraper.py     # Base scraper class
│   │   ├── linkedin_scraper.py # LinkedIn job scraper
│   │   └── indeed_scraper.py   # Indeed job scraper
│   └── automation/
│       ├── applicator.py        # Main application automation
│       └── application_filler.py # Form filling logic
├── data/                        # Generated databases
├── logs/                        # Application logs
├── generated_resumes/           # Generated resume files
└── application_history/         # Application records
```

## How Job Matching Works

The system uses a scoring algorithm (0-100) based on:

- **Title Match (30 points)**: How well the job title matches your preferences
- **Location Match (15 points)**: Whether the location matches your preferences
- **Keywords Match (30 points)**: How many of your skills appear in the job description
- **No Excluded Keywords (15 points)**: Job doesn't contain keywords you want to avoid
- **Job Type Match (10 points)**: Full-time, contract, etc.

Jobs with a score of 50% or higher are considered good matches.

## Resume Generation

The system generates tailored resumes by:

1. **AI-Powered Summary**: Creates a professional summary tailored to each job
2. **Optimized Experience**: Rewrites your experience bullets to emphasize relevant skills
3. **Keyword Optimization**: Ensures your resume includes keywords from the job description
4. **Professional Formatting**: Creates clean, ATS-friendly DOCX format resumes

Resumes are saved in `generated_resumes/` and you can review each one before applying.

## Application Automation

The automation system:

1. Detects "Easy Apply" buttons (LinkedIn, Indeed)
2. Navigates multi-step application forms
3. Fills in personal information automatically
4. Uploads your tailored resume
5. Answers common screening questions
6. Handles external application redirects

**Note**: Some applications may require manual completion, especially those on external company websites.

## Safety Features

- **Human Approval Required**: You must approve each job and resume before applying
- **Rate Limiting**: Configurable delays between applications to avoid detection
- **Dry Run Mode**: Test the system without actually submitting applications
- **Application Tracking**: Complete history of all applications and their status
- **Local Storage**: All data stays on your machine

## Tips for Best Results

1. **Accurate Profile**: The more detailed your profile, the better the matching and resume generation
2. **Specific Preferences**: Set clear job preferences and keywords to filter relevant jobs
3. **Review Resumes**: Always review generated resumes - AI can make mistakes
4. **LinkedIn Login**: Logging into LinkedIn provides access to more job details
5. **Start Small**: Begin with a few applications to test the system
6. **Monitor Results**: Track which resumes get responses and refine your profile

## Troubleshooting

### Selenium/Chrome Issues

If you encounter browser automation issues:

```bash
# Update Chrome WebDriver
# Or use Playwright instead (already in requirements.txt)
playwright install chromium
```

### OpenAI API Errors

If resume generation fails:
- Check that your OpenAI API key is valid in `.env`
- The system will fall back to template-based resumes if API is unavailable

### Scraping Issues

If job scraping fails:
- Sites may have changed their HTML structure
- Try using credentials (LinkedIn requires login for full access)
- Some sites implement anti-bot measures - use delays and headless=False

## Legal and Ethical Considerations

⚠️ **Important Disclaimers**:

- This tool is for personal use only
- Respect the Terms of Service of job platforms
- Don't spam applications - apply only to relevant positions
- Review all resumes and applications before submission
- Be honest in your applications
- Some platforms prohibit automated applications - use at your own risk

## Contributing

Contributions are welcome! Areas for improvement:

- Additional job board scrapers (Glassdoor, Monster, etc.)
- Better form field detection and filling
- Cover letter generation
- Interview scheduling automation
- Application response tracking
- Integration with email for notifications

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the documentation

## Roadmap

Future features planned:
- [ ] More job board integrations
- [ ] Cover letter generation
- [ ] Email integration for tracking responses
- [ ] Analytics dashboard
- [ ] Chrome extension for one-click applications
- [ ] Mobile app
- [ ] Integration with job search APIs

---

**Happy job hunting! 🎉**

Remember: This tool helps automate the tedious parts of job applications, but you should always review and approve everything before it's submitted. Quality over quantity!
