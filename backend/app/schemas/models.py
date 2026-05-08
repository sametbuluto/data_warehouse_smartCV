"""Pydantic schemas for API request/response models."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# --- Candidate Schemas ---
class CandidateBase(BaseModel):
    name: str = "Unknown"
    email: Optional[str] = None
    phone: Optional[str] = None
    education: Optional[str] = None
    experience_years: float = 0.0

class CandidateResponse(CandidateBase):
    id: int
    skills: list[str] = []
    file_path: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class CandidateListResponse(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    skills_count: int = 0
    experience_years: float = 0.0
    created_at: datetime

    class Config:
        from_attributes = True


# --- Job Schemas ---
class JobCreate(BaseModel):
    title: str
    description: str
    required_skills: list[str] = []
    min_experience: float = 0.0
    education_level: str = "Bachelor"

class JobResponse(JobCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- Match Schemas ---
class MatchResultResponse(BaseModel):
    id: int
    candidate_id: int
    candidate_name: str
    job_id: int
    job_title: str
    skill_score: float
    experience_score: float
    education_score: float
    semantic_score: float
    final_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    created_at: datetime

    class Config:
        from_attributes = True

class MatchExplanation(BaseModel):
    candidate_name: str
    job_title: str
    final_score: float
    skill_score: float
    experience_score: float
    education_score: float
    semantic_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    explanation: str


# --- Analytics Schemas ---
class DashboardStats(BaseModel):
    total_candidates: int
    total_jobs: int
    total_matches: int
    avg_match_score: float
    candidates_with_email: int
    candidates_with_phone: int
    candidates_with_education: int
    avg_skills_per_candidate: float
    jobs_with_matches: int
    top_skills: list[dict]
    best_candidates: list[dict]
    score_distribution: list[dict]
