import spacy
import re
import json

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Example list of technical and soft skills (expand as needed)
TECHNICAL_SKILLS = [
    "python", "java", "c++", "sql", "javascript", "html", "css", "machine learning", "data analysis"
]
SOFT_SKILLS = [
    "communication", "leadership", "teamwork", "problem solving", "adaptability", "creativity"
]

def extract_education(resume_text):
    # Simple patterns for degrees and universities (expand as needed)
    degree_patterns = [
        r"(bachelor(?:'s)?\s?of\s?\w+|b\.tech|btech|b\.e|be|bsc|msc|m\.tech|mtech|mba|ph\.?d)",  # degrees
        r"(master(?:'s)?\s?of\s?\w+)",
        r"(ba|ma|bs|ms|bca|mca)"
    ]
    university_patterns = [
        r"(university\s+of\s+\w+)",
        r"(\w+\s+university)",
        r"(\w+\s+institute\s+of\s+\w+)",
        r"(\w+\s+college)"
    ]
    education = []
    for pattern in degree_patterns + university_patterns:
        matches = re.findall(pattern, resume_text, re.IGNORECASE)
        for match in matches:
            if match and match.lower() not in [e.lower() for e in education]:
                education.append(match.strip())
    return education

def ats_extractor(resume_data):
    doc = nlp(resume_data)

    # Extract name (first PERSON entity)
    name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    # Extract email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', resume_data)
    email = email_match.group(0) if email_match else None

    # Extract education
    education = extract_education(resume_data)

    # Extract skills
    resume_lower = resume_data.lower()
    technical_skills = [skill for skill in TECHNICAL_SKILLS if skill in resume_lower]
    soft_skills = [skill for skill in SOFT_SKILLS if skill in resume_lower]

    # Extract github and linkedin links
    github = None
    linkedin = None
    github_match = re.search(r'(https?://github\.com/[^\s]+)', resume_data)
    linkedin_match = re.search(r'(https?://(www\.)?linkedin\.com/[^\s]+)', resume_data)
    if github_match:
        github = github_match.group(0)
    if linkedin_match:
        linkedin = linkedin_match.group(0)

    # Dummy employment details (expand as needed)
    employment_details = []

    result = {
        "full_name": name,
        "email_id": email,
        "education": education,
        "github_portfolio": github,
        "linkedin_id": linkedin,
        "employment_details": employment_details,
        "technical_skills": technical_skills,
        "soft_skills": soft_skills
    }

    return result