# AI Provider Comparison: Claude vs OpenAI

The Auto Job Applicant supports both **Claude (Anthropic)** and **OpenAI GPT** for AI-powered resume generation. Choose the one that works best for you!

## Quick Setup

### Using Claude (Anthropic) - Recommended ⭐

```bash
# In your .env file:
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_anthropic_key_here
```

Get your API key at: https://console.anthropic.com/

### Using OpenAI GPT

```bash
# In your .env file:
AI_PROVIDER=openai
OPENAI_API_KEY=your_openai_key_here
```

Get your API key at: https://platform.openai.com/api-keys

## Feature Comparison

| Feature | Claude (Anthropic) | OpenAI GPT |
|---------|-------------------|------------|
| **Model Used** | Claude 3.5 Sonnet | GPT-4 Turbo |
| **Context Window** | 200K tokens | 128K tokens |
| **Resume Quality** | Excellent | Excellent |
| **Creativity** | High | Very High |
| **Accuracy** | Very High | High |
| **Pricing** | $3 per million input tokens | $10 per million tokens |
| **Speed** | Fast | Fast |
| **Safety & Ethics** | Very Strong | Strong |

## Why We Recommend Claude

1. **More Affordable**: Claude is ~3x cheaper than GPT-4 for the same quality
2. **Larger Context**: Can process more of your profile and job description
3. **Professional Tone**: Claude tends to produce slightly more professional, conservative resume language
4. **Accuracy**: Claude is known for being very factual and accurate with details
5. **Safety**: Strong built-in safety features prevent hallucinations

## When to Use OpenAI Instead

- **More Creative Writing**: If you want more creative, engaging language
- **Existing OpenAI Setup**: If you already have OpenAI credits
- **Specific Style Preferences**: If you prefer GPT's writing style

## Cost Comparison

For a typical resume generation (100 jobs):

**Claude (Anthropic)**:
- Input: ~100K tokens
- Output: ~50K tokens
- Cost: **~$0.50**

**OpenAI GPT-4**:
- Input: ~100K tokens
- Output: ~50K tokens
- Cost: **~$1.50**

## Without Any AI Provider

If you don't set up either API key, the system will:
- Use template-based resume generation
- Still work, but resumes won't be tailored to each job
- Save you money but reduce effectiveness

## Switching Providers

You can easily switch between providers:

```bash
# Switch to Claude
AI_PROVIDER=anthropic

# Switch to OpenAI
AI_PROVIDER=openai

# Remove provider (use templates)
# Just comment out or remove the AI_PROVIDER line
```

## Example Output Quality

Both providers produce high-quality resumes. Here's a comparison:

### Claude Output (Professional & Accurate)
```
"Seasoned software engineer with 5+ years of expertise in Python, Django, and React.
Demonstrated success in architecting scalable microservices serving 1M+ users and
reducing deployment times by 60% through CI/CD optimization. Proven technical
leadership in mentoring junior developers and driving engineering excellence."
```

### OpenAI Output (Creative & Engaging)
```
"Dynamic software engineer with 5+ years transforming complex challenges into elegant
solutions using Python, Django, and React. Led development of high-impact microservices
architecture supporting over 1M users while slashing deployment times by 60%. Passionate
mentor who elevates team capabilities and champions engineering best practices."
```

Both are excellent - choose based on your preference!

## Best Practices

1. **Start with Claude**: Try Claude first (it's cheaper and usually just as good)
2. **Compare Results**: Generate a few resumes with each and see which you prefer
3. **Monitor Costs**: Both providers have usage dashboards - keep an eye on spending
4. **Fallback Available**: If API calls fail, the system falls back to templates

## Getting API Keys

### Anthropic Claude

1. Go to https://console.anthropic.com/
2. Sign up for an account
3. Navigate to API Keys
4. Create a new key
5. Add $10-20 credit (should last for hundreds of applications)

### OpenAI

1. Go to https://platform.openai.com/
2. Sign up for an account
3. Navigate to API Keys
4. Create a new key
5. Add credit to your account

## Troubleshooting

### "No AI provider available" message

**Check**:
1. Is `AI_PROVIDER` set in `.env`?
2. Is the corresponding API key set?
3. Is the API key valid?
4. Do you have credits in your account?

### API Errors

**Common Issues**:
- Invalid API key → Double-check the key in `.env`
- Insufficient credits → Add credits to your account
- Rate limiting → Wait a few seconds between requests
- Network issues → Check your internet connection

### Fallback Behavior

If AI generation fails:
- The system will print an error message
- It will automatically use template-based resumes
- You can still apply to jobs (just with less tailored resumes)

## Recommendations by Use Case

**Budget-Conscious Users**:
- Use Claude (3x cheaper) or templates (free)

**Maximum Quality**:
- Try both and see which style you prefer

**High Volume Applications (100+ jobs)**:
- Use Claude to save costs

**Low Volume Applications (<20 jobs)**:
- Either provider works great

**No Budget for API**:
- Use template-based resumes
- They still work, just not as tailored

---

**Bottom Line**: Both are excellent choices. Claude is our recommendation for most users due to cost and quality, but OpenAI is great too. The choice is yours!
