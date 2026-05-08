"""NLP processing pipeline using spaCy for resume analysis."""

import re
import logging
from datetime import datetime

import spacy

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

SKILL_ALIASES = {
    "py": "python",
    "python3": "python",
    "js": "javascript",
    "ts": "typescript",
    "reactjs": "react",
    "react.js": "react",
    "nodejs": "node.js",
    "node js": "node.js",
    "rest api": "rest",
    "rest apis": "rest",
    "restful api": "rest",
    "restful apis": "rest",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "k8s": "kubernetes",
    "ml": "machine learning",
    "nlp engineering": "nlp",
    "nlp engineer": "nlp",
    "powerbi": "power bi",
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "tailwind css": "tailwindcss",
    "github action": "github actions",
    "ci cd": "ci/cd",
    "ui ux": "ui/ux",
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


MONTH_PATTERN = {
    "01": 1, "1": 1, "jan": 1, "january": 1,
    "02": 2, "2": 2, "feb": 2, "february": 2,
    "03": 3, "3": 3, "mar": 3, "march": 3,
    "04": 4, "4": 4, "apr": 4, "april": 4,
    "05": 5, "5": 5, "may": 5,
    "06": 6, "6": 6, "jun": 6, "june": 6,
    "07": 7, "7": 7, "jul": 7, "july": 7,
    "08": 8, "8": 8, "aug": 8, "august": 8,
    "09": 9, "9": 9, "sep": 9, "sept": 9, "september": 9,
    "10": 10, "oct": 10, "october": 10,
    "11": 11, "nov": 11, "november": 11,
    "12": 12, "dec": 12, "december": 12,
}


def normalize_extraction_text(text: str) -> str:
    """Normalize text fragments that commonly break extraction heuristics."""
    return (
        text.replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2019", "'")
        .replace("\u02bc", "'")
    )


def extract_email(text: str) -> str | None:
    """Extract email address from text using regex."""
    text = normalize_extraction_text(text)
    text = re.sub(r"\s*@\s*", "@", text)
    text = re.sub(r"\s*\.\s*", ".", text)
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(pattern, text)
    return match.group(0).lower() if match else None


def extract_phone(text: str) -> str | None:
    """Extract phone number from text using regex."""
    text = normalize_extraction_text(text)
    pattern = r"(?:\+?\d{1,3}[\s\-./]?)?(?:\(?\d{3,4}\)?[\s\-./]?)?\d{3}[\s\-./]?\d{2,4}[\s\-./]?\d{2,4}"
    match = re.search(pattern, text)
    if not match:
        return None

    cleaned = re.sub(r"\s+", " ", match.group(0)).strip(" -./")
    digits = re.sub(r"\D", "", cleaned)
    return cleaned if len(digits) >= 10 else None


def _is_probable_name_line(line: str) -> bool:
    if not line or len(line) > 60:
        return False
    if "@" in line or "http" in line.lower():
        return False
    if re.search(r"\d{2,}", line):
        return False
    if any(token in line.lower() for token in ["summary", "profile", "education", "skills", "experience", "linkedin"]):
        return False

    words = line.replace("|", " ").split()
    if not 2 <= len(words) <= 4:
        return False

    valid_words = 0
    for word in words:
        if re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿÇĞİÖŞÜçğıöşü'’-]+", word):
            valid_words += 1

    return valid_words == len(words)


def extract_name(text: str) -> str:
    """Extract candidate name using spaCy NER.

    Falls back to first non-empty line if NER fails.
    """
    text = normalize_extraction_text(text)
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    for line in lines[:8]:
        if _is_probable_name_line(line):
            return re.sub(r"\s+", " ", line).strip()

    if nlp is None:
        return lines[0][:100] if lines else "Unknown"

    # Use first 500 chars for name detection (names are usually at the top)
    doc = nlp(text[:500])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()

    # Fallback: first non-empty line
    return lines[0][:100] if lines else "Unknown"


def extract_skills(text: str) -> list[str]:
    """Extract skills from text by matching against known skills list.

    Uses lowercased text matching with word boundary awareness.
    """
    text_lower = normalize_extraction_text(text).lower()
    found_skills = set()

    searchable_skills = {skill: skill for skill in KNOWN_SKILLS}
    searchable_skills.update(SKILL_ALIASES)

    for term, canonical in searchable_skills.items():
        pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"
        if re.search(pattern, text_lower):
            found_skills.add(canonical)

    return sorted(found_skills)


def _parse_month_year(token: str) -> tuple[int, int] | None:
    token = token.strip().lower().replace(".", "").replace(" ", "/")

    if token in {"present", "current", "now"}:
        today = datetime.utcnow()
        return today.year, today.month

    match = re.fullmatch(r"([a-z]{3,9}|\d{1,2})/(\d{4})", token)
    if not match:
        return None

    month_token, year_token = match.groups()
    month = MONTH_PATTERN.get(month_token)
    if not month:
        return None

    return int(year_token), int(month)


def extract_date_range_experience(text: str) -> float:
    """Estimate total experience from date ranges like 10/2025 - 03/2026."""
    text = normalize_extraction_text(text)
    pattern = re.compile(
        r"((?:\d{1,2}|[A-Za-z]{3,9})/\d{4})\s*-\s*((?:\d{1,2}|[A-Za-z]{3,9})/\d{4}|present|current|now)",
        re.IGNORECASE,
    )
    excluded_line_keywords = {
        "education",
        "university",
        "school",
        "bachelor",
        "master",
        "phd",
        "degree",
    }

    total_months = 0
    for line in text.splitlines():
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in excluded_line_keywords):
            continue

        for start_token, end_token in pattern.findall(line):
            start = _parse_month_year(start_token)
            end = _parse_month_year(end_token)
            if not start or not end:
                continue

            start_year, start_month = start
            end_year, end_month = end
            months = (end_year - start_year) * 12 + (end_month - start_month) + 1
            if 0 < months <= 600:
                total_months += months

    return round(total_months / 12, 1) if total_months else 0.0


def extract_experience_years(text: str) -> float:
    """Extract years of experience from text.

    Looks for patterns like '5 years', '3+ years of experience', etc.
    """
    text = normalize_extraction_text(text)
    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:professional\s+)?(?:experience|exp)?",
        r"experience\s*:?\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
    ]

    years = []
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        years.extend([float(y) for y in matches])

    derived_from_dates = extract_date_range_experience(text)
    if derived_from_dates:
        years.append(derived_from_dates)

    return round(max(years), 1) if years else 0.0


def extract_education(text: str) -> str:
    """Extract highest education level from text."""
    text_lower = normalize_extraction_text(text).lower()

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

    Pipeline: lowercase → remove special chars → lemmatize.
    """
    # Lowercase
    text = normalize_extraction_text(text).lower()

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
