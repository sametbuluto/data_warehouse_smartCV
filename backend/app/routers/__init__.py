from .candidates import router as candidates_router
from .jobs import router as jobs_router
from .matching import router as matching_router
from .analytics import router as analytics_router

__all__ = ["candidates_router", "jobs_router", "matching_router", "analytics_router"]
