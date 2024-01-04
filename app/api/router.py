from fastapi import APIRouter

from app.core.config import get_settings

from .endpoints import farms_router, fields_router, research_router

settings = get_settings()

# Add all the API endpoints from the endpoints folder
api_router = APIRouter()
api_router.include_router(farms_router, prefix="/farms", tags=["farms"])
api_router.include_router(fields_router, prefix="/fields", tags=["fields"])
api_router.include_router(research_router, prefix="/research", tags=["research"])
