"""Analytics API routes — dashboard KPIs and statistics."""

import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from collections import Counter

from app.database import get_db, Candidate, JobPosting, MatchResult, Skill
from app.schemas.models import AnalyticsInsights, DashboardStats


def _categorize_title(title: str) -> str:
    t = (title or "").lower()
    if any(k in t for k in ["sales", "business development", "customer success"]):
        return "Sales & BD"
    if any(k in t for k in ["hr ", "human resources", "talent", "training", "learning", "compensation", "benefit", "instructional"]):
        return "HR & Training"
    if any(k in t for k in ["supply chain", "procurement", "sourcing", "logistics", "distribution"]):
        return "Supply Chain"
    if any(k in t for k in ["engineer", "engineering", "mechanical", "electrical", "manufacturing"]):
        return "Engineering"
    if any(k in t for k in ["lawyer", "legal", " ip ", "attorney", "gdpr", "privacy"]):
        return "Legal"
    if any(k in t for k in ["financ", "accounti", "treasury", "risk", "investment", "equity", "aml"]):
        return "Finance"
    if any(k in t for k in ["marketing", "seo", "brand", "content"]):
        return "Marketing"
    if any(k in t for k in ["health", "clinical", "hospital", "pharma"]):
        return "Healthcare"
    return "Tech"

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard(db: Session = Depends(get_db)):
    """Get dashboard statistics and KPIs."""
    total_candidates = db.query(Candidate).count()
    total_jobs = db.query(JobPosting).count()
    total_matches = db.query(MatchResult).count()
    candidates_with_email = db.query(Candidate).filter(Candidate.email.isnot(None), Candidate.email != "").count()
    candidates_with_phone = db.query(Candidate).filter(Candidate.phone.isnot(None), Candidate.phone != "").count()
    candidates_with_education = db.query(Candidate).filter(
        Candidate.education.isnot(None),
        Candidate.education != "",
        Candidate.education != "Unknown",
    ).count()
    total_skills = db.query(Skill).count()
    avg_skills_per_candidate = round(total_skills / total_candidates, 2) if total_candidates else 0.0
    jobs_with_matches = db.query(func.count(func.distinct(MatchResult.job_id))).scalar() or 0

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
        candidates_with_email=candidates_with_email,
        candidates_with_phone=candidates_with_phone,
        candidates_with_education=candidates_with_education,
        avg_skills_per_candidate=avg_skills_per_candidate,
        jobs_with_matches=jobs_with_matches,
        top_skills=top_skills,
        best_candidates=best_candidates,
        score_distribution=score_distribution,
    )


@router.get("/insights", response_model=AnalyticsInsights)
def get_insights(db: Session = Depends(get_db)):
    """Aggregate insights: skill demand vs supply, category quality, experience-vs-score, top jobs by champion."""

    # ── Skill demand (jobs side) — explode JSON list of required_skills ──
    demand_counter: Counter = Counter()
    for (req_skills,) in db.query(JobPosting.required_skills).all():
        for s in (req_skills or []):
            demand_counter[s.strip().lower()] += 1

    # ── Skill supply (candidate side) ──
    supply_counter: Counter = Counter()
    for (sk,) in db.query(Skill.skill_name).all():
        supply_counter[(sk or "").strip().lower()] += 1

    # Take top demanded skills, then attach supply numbers
    top_demanded = demand_counter.most_common(10)
    skill_supply_demand = [
        {"skill": skill, "demand": demand, "supply": supply_counter.get(skill, 0)}
        for skill, demand in top_demanded
    ]

    # ── Category quality: per category, count jobs and avg of TOP score per job ──
    job_top_scores: dict[int, tuple[str, str, float]] = {}  # job_id -> (title, category, top_score)
    for job in db.query(JobPosting).all():
        top = (
            db.query(func.max(MatchResult.final_score))
            .filter(MatchResult.job_id == job.id)
            .scalar()
        )
        job_top_scores[job.id] = (job.title, _categorize_title(job.title), float(top or 0.0))

    category_buckets: dict[str, list[float]] = {}
    for _title, cat, top in job_top_scores.values():
        category_buckets.setdefault(cat, []).append(top)
    category_quality = [
        {
            "category": cat,
            "job_count": len(scores),
            "avg_top_score": round(sum(scores) / len(scores), 2) if scores else 0.0,
        }
        for cat, scores in sorted(category_buckets.items(), key=lambda kv: -len(kv[1]))
    ]

    # ── Experience vs avg match score: bucket candidates by experience years ──
    candidate_avgs = (
        db.query(
            Candidate.id,
            Candidate.experience_years,
            func.avg(MatchResult.final_score).label("avg_score"),
            func.count(MatchResult.id).label("match_count"),
        )
        .join(MatchResult, Candidate.id == MatchResult.candidate_id)
        .group_by(Candidate.id)
        .all()
    )
    bucket_defs = [(0, 1), (1, 3), (3, 5), (5, 8), (8, 99)]
    bucket_labels = ["0-1", "1-3", "3-5", "5-8", "8+"]
    buckets: list[list[float]] = [[] for _ in bucket_defs]
    counts: list[int] = [0] * len(bucket_defs)
    for _id, yrs, avg, _n in candidate_avgs:
        for i, (lo, hi) in enumerate(bucket_defs):
            if (yrs or 0) >= lo and (yrs or 0) < hi:
                buckets[i].append(float(avg or 0.0))
                counts[i] += 1
                break
    experience_score = [
        {
            "band": bucket_labels[i],
            "avg_score": round(sum(buckets[i]) / len(buckets[i]), 2) if buckets[i] else 0.0,
            "candidates": counts[i],
        }
        for i in range(len(bucket_defs))
    ]

    # ── Top 8 jobs by champion (top-1) score ──
    champion_rows = (
        db.query(
            MatchResult.job_id,
            Candidate.name.label("candidate_name"),
            MatchResult.final_score,
            JobPosting.title,
        )
        .join(JobPosting, MatchResult.job_id == JobPosting.id)
        .join(Candidate, MatchResult.candidate_id == Candidate.id)
        .order_by(MatchResult.final_score.desc())
        .all()
    )
    seen_jobs: set[int] = set()
    top_jobs_by_champion = []
    for job_id, cand_name, score, title in champion_rows:
        if job_id in seen_jobs:
            continue
        seen_jobs.add(job_id)
        top_jobs_by_champion.append({
            "job_id": job_id,
            "job_title": title,
            "champion_name": cand_name,
            "top_score": round(float(score), 2),
            "category": _categorize_title(title),
        })
        if len(top_jobs_by_champion) >= 8:
            break

    return AnalyticsInsights(
        skill_supply_demand=skill_supply_demand,
        category_quality=category_quality,
        experience_score=experience_score,
        top_jobs_by_champion=top_jobs_by_champion,
    )
