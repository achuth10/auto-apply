from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="auto-job-applicant",
    version="1.0.0",
    author="Auto Job Applicant",
    description="Automated job application system with AI-powered resume generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/auto-job-applicant",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "selenium>=4.15.0",
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0",
        "click>=8.1.0",
        "python-dotenv>=1.0.0",
        "openai>=1.3.0",
        "pydantic>=2.5.0",
        "playwright>=1.40.0",
        "chromadb>=0.4.0",
        "python-docx>=1.1.0",
        "jinja2>=3.1.0",
        "colorama>=0.4.6",
        "tabulate>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "auto-apply=main:cli",
        ],
    },
)
