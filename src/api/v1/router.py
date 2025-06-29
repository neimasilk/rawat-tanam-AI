from fastapi import APIRouter
from .endpoints import identify, species, auth

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    identify.router,
    prefix="/identify",
    tags=["Plant Identification"]
)

api_router.include_router(
    species.router,
    prefix="/species",
    tags=["Species Database"]
)

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

# API Info endpoint
@api_router.get("/info", tags=["API Info"])
async def api_info():
    """Get API information and status"""
    return {
        "name": "Rawat Tanam AI API",
        "version": "1.0.0",
        "description": "Indonesian Flora Identification API Platform",
        "endpoints": {
            "identify": "/api/v1/identify",
            "species": "/api/v1/species",
            "auth": "/api/v1/auth"
        },
        "documentation": "/api/v1/docs",
        "status": "operational"
    }