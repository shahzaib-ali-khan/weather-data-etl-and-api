from fastapi import APIRouter

from packages.app.api.v1 import weather

api_router = APIRouter(prefix="/v1")

# Include all route modules
api_router.include_router(weather.router)
