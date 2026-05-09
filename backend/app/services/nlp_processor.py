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

# Predefined skills list for matching (500+ skills across all major industries)
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
    # Design & UX
    "figma", "photoshop", "illustrator", "sketch", "invision", "zeplin",
    "ui/ux", "ux design", "user research", "wireframing", "prototyping",
    "adobe creative suite", "canva", "adobe xd",
    # General Office & Soft Skills
    "excel", "word", "powerpoint", "microsoft office", "google workspace",
    "project management", "communication", "leadership", "problem solving",
    "critical thinking", "time management", "teamwork", "presentation",
    "stakeholder management", "strategic planning",
    # ── FINANCE & ACCOUNTING ──────────────────────────────────────────────────
    "financial analysis", "financial modeling", "financial reporting",
    "accounting", "auditing", "tax planning", "bookkeeping",
    "budgeting", "forecasting", "variance analysis", "cost accounting",
    "management accounting", "accounts payable", "accounts receivable",
    "general ledger", "balance sheet", "income statement", "cash flow",
    "gaap", "ifrs", "sarbanes-oxley", "sox", "internal controls",
    "risk management", "credit analysis", "credit risk", "market risk",
    "operational risk", "liquidity risk", "var", "stress testing",
    "equity research", "investment analysis", "portfolio management",
    "asset management", "fixed income", "derivatives", "options",
    "bloomberg terminal", "bloomberg", "reuters eikon", "factset",
    "valuation", "dcf", "lbo", "merger & acquisition", "m&a",
    "investment banking", "private equity", "venture capital",
    "treasury management", "cash management", "fx hedging",
    "regulatory reporting", "basel iii", "solvency ii",
    "aml", "kyc", "anti-money laundering", "compliance",
    "cfa", "cpa", "acca", "frm",
    "sap", "sap fico", "sap s4hana", "oracle financials", "quickbooks",
    "hyperion", "anaplan", "adaptive insights", "essbase",
    # ── HEALTHCARE & MEDICAL ─────────────────────────────────────────────────
    "clinical research", "clinical trials", "good clinical practice", "gcp",
    "fda regulations", "ema regulations", "ich guidelines",
    "pharmacovigilance", "drug safety", "adverse event reporting",
    "medical coding", "icd-10", "cpt codes", "medical billing",
    "emr", "ehr", "epic", "cerner", "meditech",
    "hl7", "fhir", "healthcare interoperability",
    "hipaa", "healthcare compliance", "patient privacy",
    "healthcare analytics", "real-world evidence", "biostatistics",
    "clinical data management", "redcap", "medidata rave",
    "medical imaging", "radiology", "pathology",
    "hospital administration", "healthcare operations",
    "patient care", "nursing", "pharmacy",
    "medical writing", "regulatory submissions", "ctd",
    "health economics", "health technology assessment", "hta",
    "public health", "epidemiology",
    # ── MARKETING & DIGITAL ──────────────────────────────────────────────────
    "digital marketing", "performance marketing", "growth hacking",
    "seo", "sem", "ppc", "paid search", "paid media",
    "google ads", "meta ads", "facebook ads", "instagram ads",
    "linkedin ads", "programmatic advertising",
    "google analytics", "ga4", "adobe analytics", "mixpanel",
    "content marketing", "copywriting", "content strategy",
    "email marketing", "marketing automation",
    "hubspot", "marketo", "salesforce marketing cloud", "mailchimp",
    "social media marketing", "community management",
    "brand management", "brand strategy", "brand identity",
    "market research", "consumer insights", "competitive analysis",
    "a/b testing", "conversion rate optimization", "cro",
    "affiliate marketing", "influencer marketing",
    "pr", "public relations", "media relations",
    "product marketing", "go-to-market", "gtm strategy",
    "crm", "customer lifecycle", "retention marketing",
    "video marketing", "youtube", "tiktok marketing",
    "seo tools", "ahrefs", "semrush", "moz",
    # ── LEGAL ────────────────────────────────────────────────────────────────
    "legal research", "legal writing", "legal analysis",
    "contract law", "contract drafting", "contract negotiation", "contract review",
    "corporate law", "commercial law", "business law",
    "litigation", "dispute resolution", "arbitration", "mediation",
    "intellectual property", "patent law", "trademark", "copyright",
    "employment law", "labor law",
    "data privacy", "gdpr", "ccpa", "data protection",
    "regulatory affairs", "regulatory compliance",
    "due diligence", "legal due diligence",
    "mergers & acquisitions", "corporate transactions",
    "company secretarial", "corporate governance",
    "lexisnexis", "westlaw", "practical law",
    "e-discovery", "legal project management",
    # ── MECHANICAL / CIVIL / ELECTRICAL ENGINEERING ──────────────────────────
    "autocad", "solidworks", "catia", "nx", "creo", "inventor",
    "ansys", "abaqus", "nastran", "finite element analysis", "fea",
    "mechanical design", "product design", "3d modeling",
    "structural analysis", "stress analysis", "fatigue analysis",
    "civil engineering", "structural engineering", "geotechnical engineering",
    "construction management", "project scheduling", "primavera", "ms project",
    "bim", "revit", "archicad",
    "hvac", "mep", "building services",
    "electrical engineering", "power systems", "plc programming",
    "scada", "dcs", "instrumentation", "control systems",
    "lean manufacturing", "six sigma", "kaizen", "5s",
    "quality management", "iso 9001", "iso 14001", "iatf 16949",
    "failure mode analysis", "fmea", "root cause analysis", "rca",
    "3d printing", "additive manufacturing", "cam", "cnc",
    "supply chain engineering", "process improvement",
    # ── HUMAN RESOURCES ──────────────────────────────────────────────────────
    "talent acquisition", "recruitment", "headhunting", "executive search",
    "sourcing", "boolean search", "linkedin recruiter",
    "onboarding", "offboarding", "employee lifecycle",
    "performance management", "performance appraisal", "okr", "kpi",
    "employee relations", "labor relations", "grievance handling",
    "compensation & benefits", "total rewards", "salary benchmarking",
    "hr analytics", "people analytics", "workforce planning",
    "organizational development", "change management",
    "succession planning", "talent management",
    "learning & development", "training delivery", "facilitation",
    "diversity & inclusion", "dei", "employee engagement",
    "hris", "workday", "sap hr", "successfactors", "adp", "bamboohr",
    "employment law", "hr compliance",
    # ── SUPPLY CHAIN & LOGISTICS ─────────────────────────────────────────────
    "supply chain management", "supply chain optimization",
    "logistics", "freight management", "transportation management",
    "warehousing", "inventory management", "stock control",
    "procurement", "strategic sourcing", "category management",
    "vendor management", "supplier evaluation", "rfq", "rfp",
    "demand planning", "s&op", "sales & operations planning",
    "erp", "sap scm", "oracle scm", "sap mm", "sap wm",
    "import/export", "customs", "incoterms", "trade compliance",
    "3pl", "last-mile delivery", "cold chain",
    "lean supply chain", "just-in-time", "kanban",
    "contract manufacturing", "outsourcing",
    # ── SALES & BUSINESS DEVELOPMENT ─────────────────────────────────────────
    "sales strategy", "sales management", "account management",
    "business development", "partnership development",
    "b2b sales", "b2c sales", "enterprise sales", "saas sales",
    "lead generation", "prospecting", "cold calling",
    "pipeline management", "sales forecasting", "quota management",
    "negotiation", "closing", "upselling", "cross-selling",
    "key account management", "customer success",
    "salesforce", "hubspot crm", "pipedrive", "zoho crm",
    "revenue operations", "revops", "sales enablement",
    "client relationship management",
    # ── EDUCATION & INSTRUCTIONAL DESIGN ─────────────────────────────────────
    "instructional design", "curriculum development", "course design",
    "e-learning", "scorm", "lms", "moodle", "canvas", "blackboard",
    "articulate storyline", "articulate rise", "adobe captivate",
    "training delivery", "classroom facilitation",
    "assessment design", "blended learning",
    "adult learning theory", "addie", "sam model",
    "educational technology", "edtech",
    "content creation", "video production", "screencasting",
    "coaching", "mentoring",
}

SKILL_ALIASES = {
    # Tech aliases
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
    # Finance aliases
    "financial modelling": "financial modeling",
    "p&l": "financial reporting",
    "profit and loss": "financial reporting",
    "m and a": "merger & acquisition",
    "mergers and acquisitions": "merger & acquisition",
    "anti money laundering": "aml",
    "know your customer": "kyc",
    "sap s/4hana": "sap s4hana",
    "sap/4hana": "sap s4hana",
    "chartered financial analyst": "cfa",
    "certified public accountant": "cpa",
    # Healthcare aliases
    "electronic medical records": "emr",
    "electronic health records": "ehr",
    "good clinical practice": "gcp",
    "drug safety reporting": "pharmacovigilance",
    "adverse events": "adverse event reporting",
    # Marketing aliases
    "search engine optimization": "seo",
    "search engine marketing": "sem",
    "pay per click": "ppc",
    "conversion optimization": "conversion rate optimization",
    "google analytics 4": "ga4",
    "facebook advertising": "facebook ads",
    "meta advertising": "meta ads",
    # Legal aliases
    "ip law": "intellectual property",
    "data protection law": "data privacy",
    "general data protection regulation": "gdpr",
    # Engineering aliases
    "finite element": "finite element analysis",
    "computer aided design": "autocad",
    "cad design": "autocad",
    "building information modeling": "bim",
    "failure mode and effects analysis": "fmea",
    "six sigma": "six sigma",
    "lean six sigma": "six sigma",
    # HR aliases
    "talent management": "talent acquisition",
    "human resources information system": "hris",
    "diversity and inclusion": "diversity & inclusion",
    "learning and development": "learning & development",
    "l&d": "learning & development",
    # Supply chain aliases
    "sales and operations planning": "s&op",
    "third party logistics": "3pl",
    "supplier management": "vendor management",
    # Sales aliases
    "account executive": "account management",
    "business dev": "business development",
    "saas": "saas sales",
    "revenue ops": "revenue operations",
    # Education aliases
    "instructional designer": "instructional design",
    "lms administration": "lms",
    "adult learning": "adult learning theory",
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
