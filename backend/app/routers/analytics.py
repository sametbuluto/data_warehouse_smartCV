"""Analytics API routes — dashboard KPIs and statistics."""

import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from collections import Counter

from app.database import get_db, Candidate, JobPosting, MatchResult, Skill
from app.schemas.models import DashboardStats

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard(db: Session = Depends(get_db)):
    """Get dashboard statistics and KPIs."""
    total_candidates = db.query(Candidate).count()
    total_jobs = db.query(JobPosting).count()
    total_matches = db.query(MatchResult).count()

    # Average match score
    avg_score_result = db.query(func.avg(MatchResult.final_score)).scalar()
    avg_match_score = round(float(avg_score_result), 2) if avg_score_result else 0.0

    # Top skills (most common across all candidates)
    all_skills = db.query(Skill.skill_name).all()
    skill_counts = Counter(s[0] for s in all_skills)
    top_skills = [{"name": name, "count": count} for name, count in skill_counts.most_common(10)]

    # Best candidates (highest average final_score)
    best_candidates = []
    candidates_with_scores = (
        db.query(
            Candidate.id,
            Candidate.name,
            func.avg(MatchResult.final_score).label("avg_score"),
        )
        .join(MatchResult, Candidate.id == MatchResult.candidate_id)
        .group_by(Candidate.id)
        .order_by(func.avg(MatchResult.final_score).desc())
        .limit(5)
        .all()
    )
    for c in candidates_with_scores:
        best_candidates.append({
            "id": c.id,
            "name": c.name,
            "avg_score": round(float(c.avg_score), 2),
        })

    # Score distribution (buckets: 0-20, 20-40, 40-60, 60-80, 80-100)
    score_distribution = []
    buckets = [(0, 20), (20, 40), (40, 60), (60, 80), (80, 100)]
    for low, high in buckets:
        count = db.query(MatchResult).filter(
            MatchResult.final_score >= low,
            MatchResult.final_score < (high + 1 if high == 100 else high),
        ).count()
        score_distribution.append({"range": f"{low}-{high}", "count": count})

    return DashboardStats(
        total_candidates=total_candidates,
        total_jobs=total_jobs,
        total_matches=total_matches,
        avg_match_score=avg_match_score,
        top_skills=top_skills,
        best_candidates=best_candidates,
        score_distribution=score_distribution,
    )
