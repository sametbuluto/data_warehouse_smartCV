"""Matching engine: TF-IDF vectorization, cosine similarity, and weighted scoring."""

import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.services.nlp_processor import preprocess_text, EDUCATION_LEVELS

logger = logging.getLogger(__name__)

# Scoring weights — skill and semantic dominate so scores spread wider
WEIGHT_SKILL = 0.50
WEIGHT_EXPERIENCE = 0.20
WEIGHT_EDUCATION = 0.10
WEIGHT_SEMANTIC = 0.20


def calculate_skill_score(candidate_skills: list[str], required_skills: list[str]) -> tuple[float, list[str], list[str]]:
    """Calculate skill match score with non-linear penalty for missing skills.

    Uses power curve so missing even 1-2 skills meaningfully drops the score,
    creating wider separation between candidates.
    """
    if not required_skills:
        return 100.0, list(candidate_skills), []

    candidate_set = {s.lower() for s in candidate_skills}
    required_set = {s.lower() for s in required_skills}

    matched = candidate_set & required_set
    missing = required_set - candidate_set

    n = len(required_set)
    n_matched = len(matched)

    # Power curve: 9/9=100, 8/9=87, 7/9=75, 6/9=63, 5/9=51, 4/9=40, 3/9=29...
    score = (n_matched / n) ** 1.25 * 100
    return round(score, 2), sorted(matched), sorted(missing)


def calculate_experience_score(candidate_years: float, required_years: float) -> float:
    """Experience score with a sweet-spot curve.

    - Far under-qualified: steep penalty
    - Slightly under: proportional penalty
    - Meets requirement: 85-95
    - Ideal fit (1-2x required): 100
    - Heavily overqualified (3x+): modest penalty (likely poor fit)
    """
    if required_years <= 0:
        return 100.0

    ratio = candidate_years / required_years

    if ratio >= 3.0:
        # Very overqualified — likely won't stay
        return 72.0
    elif ratio >= 2.0:
        # Overqualified
        return 88.0
    elif ratio >= 1.0:
        # Meets or slightly exceeds — linear from 85 to 100
        return round(85.0 + (ratio - 1.0) / 1.0 * 15.0, 2)
    elif ratio >= 0.5:
        # Somewhat under — proportional
        return round(ratio * 85.0, 2)
    else:
        # Significantly under-qualified
        return round(ratio * 60.0, 2)


def calculate_education_score(candidate_education: str, required_education: str) -> float:
    """Education score — meeting or exceeding gives full marks; gap is penalized proportionally."""
    candidate_level = EDUCATION_LEVELS.get(candidate_education.lower(), 40)
    required_level = EDUCATION_LEVELS.get(required_education.lower(), 60)

    if candidate_level >= required_level:
        return 100.0
    return round((candidate_level / required_level) * 100, 2)


def calculate_semantic_similarity(cv_text: str, job_text: str) -> float:
    """Calculate semantic similarity using TF-IDF + Cosine Similarity."""
    cv_processed = preprocess_text(cv_text)
    job_processed = preprocess_text(job_text)

    if not cv_processed.strip() or not job_processed.strip():
        return 0.0

    try:
        vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform([cv_processed, job_processed])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(similarity) * 100, 2)
    except Exception as e:
        logger.error(f"TF-IDF similarity calculation failed: {e}")
        return 0.0


def calculate_final_score(
    candidate_skills: list[str],
    required_skills: list[str],
    candidate_experience: float,
    required_experience: float,
    candidate_education: str,
    required_education: str,
    cv_text: str,
    job_text: str,
) -> dict:
    """Calculate the weighted final matching score.

    Formula:
        Final = 50% Skill + 20% Experience + 10% Education + 20% Semantic
    """
    skill_score, matched, missing = calculate_skill_score(candidate_skills, required_skills)
    exp_score = calculate_experience_score(candidate_experience, required_experience)
    edu_score = calculate_education_score(candidate_education, required_education)
    sem_score = calculate_semantic_similarity(cv_text, job_text)

    final = (
        WEIGHT_SKILL * skill_score
        + WEIGHT_EXPERIENCE * exp_score
        + WEIGHT_EDUCATION * edu_score
        + WEIGHT_SEMANTIC * sem_score
    )

    return {
        "skill_score": skill_score,
        "experience_score": exp_score,
        "education_score": edu_score,
        "semantic_score": sem_score,
        "final_score": round(final, 2),
        "matched_skills": matched,
        "missing_skills": missing,
    }


def generate_explanation(result: dict, candidate_name: str, job_title: str) -> str:
    """Generate a human-readable explanation of the matching result."""
    lines = [
        f"### Match Analysis: {candidate_name} → {job_title}",
        f"",
        f"**Final Score: {result['final_score']:.1f}/100**",
        f"",
        f"#### Score Breakdown:",
        f"- **Skill Match ({WEIGHT_SKILL*100:.0f}%):** {result['skill_score']:.1f}/100",
        f"- **Experience Match ({WEIGHT_EXPERIENCE*100:.0f}%):** {result['experience_score']:.1f}/100",
        f"- **Education Match ({WEIGHT_EDUCATION*100:.0f}%):** {result['education_score']:.1f}/100",
        f"- **Semantic Similarity ({WEIGHT_SEMANTIC*100:.0f}%):** {result['semantic_score']:.1f}/100",
        f"",
    ]

    if result["matched_skills"]:
        lines.append(f"#### ✅ Matched Skills ({len(result['matched_skills'])}):")
        lines.append(", ".join(result["matched_skills"]))
        lines.append("")

    if result["missing_skills"]:
        lines.append(f"#### ❌ Missing Skills ({len(result['missing_skills'])}):")
        lines.append(", ".join(result["missing_skills"]))
        lines.append("")

    score = result["final_score"]
    if score >= 80:
        lines.append("#### 🟢 Assessment: **Excellent Match** — Highly recommended for this position.")
    elif score >= 60:
        lines.append("#### 🟡 Assessment: **Good Match** — Meets most requirements with minor gaps.")
    elif score >= 40:
        lines.append("#### 🟠 Assessment: **Partial Match** — Some relevant skills but significant gaps exist.")
    else:
        lines.append("#### 🔴 Assessment: **Weak Match** — Does not meet most requirements.")

    return "\n".join(lines)
