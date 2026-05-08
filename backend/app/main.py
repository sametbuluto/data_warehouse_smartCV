"""FastAPI application entry point — Smart CV Analysis & Candidate Matching System."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.database import init_db
from app.routers import candidates_router, jobs_router, matching_router, analytics_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    init_db()
    logger.info("Database initialized successfully.")
    yield
    logger.info("Application shutting down.")


app = FastAPI(
    title="Smart CV Analysis & Candidate Matching System",
    description="AI-powered recruitment platform using NLP and ML for resume analysis and candidate matching.",
    version=__version__,
    lifespan=lifespan,
)

# CORS — allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(candidates_router)
app.include_router(jobs_router)
app.include_router(matching_router)
app.include_router(analytics_router)


@app.get("/")
async def root():
    return {
        "name": "Smart CV Analysis & Candidate Matching System",
        "version": __version__,
        "docs": "/docs",
        "endpoints": {
            "candidates": "/api/candidates",
            "jobs": "/api/jobs",
            "matching": "/api/match/{job_id}",
            "analytics": "/api/analytics/dashboard",
        },
    }


@app.get("/api/health")
async def health():
    return {"status": "ok"}
