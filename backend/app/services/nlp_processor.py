"""NLP processing pipeline using spaCy and NLTK for resume analysis."""

import re
import logging
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

logger = logging.getLogger(__name__)

# Load spaCy model (lightweight English model)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.warning("spaCy model not found. Run: python -m spacy download en_core_web_sm")
    nlp = None

# Predefined skills list for matching (~200 common tech skills)
KNOWN_SKILLS = {
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "c", "ruby",
    "go", "golang", "rust", "swift", "kotlin", "php", "r", "scala", "perl",
    "matlab", "dart", "lua", "shell", "bash", "powershell",
    # Web Frontend
    "react", "angular", "vue", "vue.js", "svelte", "next.js", "nextjs",
    "html", "css", "sass", "less", "tailwindcss", "tailwind", "bootstrap",
    "jquery", "webpack", "vite",
    # Web Backend
    "node.js", "nodejs", "express", "django", "flask", "fastapi", "spring",
    "spring boot", "asp.net", ".net", "rails", "laravel",
    # Databases
    "sql", "mysql", "postgresql", "postgres", "mongodb", "redis", "sqlite",
    "oracle", "cassandra", "elasticsearch", "dynamodb", "firebase",
    # Cloud & DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "k8s",
    "terraform", "ansible", "jenkins", "ci/cd", "github actions", "gitlab",
    "linux", "nginx", "apache",
    # Data & ML
    "machine learning", "deep learning", "tensorflow", "pytorch", "keras",
    "scikit-learn", "pandas", "numpy", "scipy", "matplotlib", "seaborn",
    "nlp", "natural language processing", "computer vision", "opencv",
    "data science", "data analysis", "data engineering", "spark", "hadoop",
    "airflow", "tableau", "power bi",
    # Mobile
    "android", "ios", "react native", "flutter",
    # Tools & Practices
    "git", "github", "gitlab", "bitbucket", "jira", "confluence",
    "agile", "scrum", "rest", "restful", "graphql", "api",
    "microservices", "design patterns", "oop", "tdd", "unit testing",
    # Other
    "figma", "photoshop", "ui/ux", "ux design", "excel", "word",
    "project management", "communication", "leadership", "problem solving",
}

# Education level hierarchy for scoring
EDUCATION_LEVELS = {
    "high school": 20,
    "associate": 40,
    "bachelor": 60,
    "master": 80,
    "mba": 80,
    "phd": 100,
    "doctorate": 100,
}


def extract_email(text: str) -> str | None:
    """Extract email address from text using regex."""
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    """Extract phone number from text using regex."""
    pattern = r"[\+]?[(]?[0-9]{1,4}[)]?[-\s\./0-9]{7,15}"
    match = re.search(pattern, text)
    return match.group(0).strip() if match else None


def extract_name(text: str) -> str:
    """Extract candidate name using spaCy NER.

    Falls back to first non-empty line if NER fails.
    """
    if nlp is None:
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        return lines[0][:100] if lines else "Unknown"

    # Use first 500 chars for name detection (names are usually at the top)
    doc = nlp(text[:500])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()

    # Fallback: first non-empty line
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    return lines[0][:100] if lines else "Unknown"


def extract_skills(text: str) -> list[str]:
    """Extract skills from text by matching against known skills list.

    Uses lowercased text matching with word boundary awareness.
    """
    text_lower = text.lower()
    found_skills = []

    for skill in KNOWN_SKILLS:
        # Use word boundary matching for short skills to avoid false positives
        if len(skill) <= 2:
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        elif skill in text_lower:
            found_skills.append(skill)

    return sorted(set(found_skills))


def extract_experience_years(text: str) -> float:
    """Extract years of experience from text.

    Looks for patterns like '5 years', '3+ years of experience', etc.
    """
    patterns = [
        r"(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)?",
        r"experience\s*:?\s*(\d+)\s*(?:years?|yrs?)",
    ]

    years = []
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        years.extend([float(y) for y in matches])

    return max(years) if years else 0.0


def extract_education(text: str) -> str:
    """Extract highest education level from text."""
    text_lower = text.lower()

    # Check from highest to lowest
    for level in ["phd", "doctorate", "master", "mba", "bachelor", "associate", "high school"]:
        if level in text_lower:
            return level.title()

    # Check for degree abbreviations
    abbreviations = {
        r"\bph\.?d\.?\b": "PhD",
        r"\bm\.?s\.?\b": "Master",
        r"\bm\.?sc\.?\b": "Master",
        r"\bm\.?a\.?\b": "Master",
        r"\bb\.?s\.?\b": "Bachelor",
        r"\bb\.?sc\.?\b": "Bachelor",
        r"\bb\.?a\.?\b": "Bachelor",
        r"\bb\.?eng\.?\b": "Bachelor",
    }

    for pattern, level in abbreviations.items():
        if re.search(pattern, text_lower):
            return level

    return "Unknown"


def preprocess_text(text: str) -> str:
    """Clean and preprocess text for NLP analysis.

    Pipeline: lowercase → remove special chars → tokenize → remove stopwords → lemmatize.
    """
    # Lowercase
    text = text.lower()

    # Remove URLs and emails
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "", text)

    # Remove special characters but keep spaces
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Lemmatize with spaCy if available
    if nlp:
        doc = nlp(text)
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and len(token.text) > 1]
        return " ".join(tokens)

    return text


def parse_resume(text: str) -> dict:
    """Full NLP pipeline to parse a resume.

    Returns structured data extracted from raw resume text.
    """
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience_years": extract_experience_years(text),
        "preprocessed_text": preprocess_text(text),
    }
