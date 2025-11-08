"""Main FastAPI application."""

from typing import cast

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.types import ExceptionHandler

from packages.app.api.v1.router import api_router
from packages.app.config import settings


def create_application() -> FastAPI:
    limiter = Limiter(key_func=get_remote_address)

    application = FastAPI(
        title=settings.APP_NAME,
        description="FastAPI application with JWT authentication",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configure CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rate limiting
    application.state.limiter = limiter
    application.add_exception_handler(
        RateLimitExceeded, cast(ExceptionHandler, _rate_limit_exceeded_handler)
    )
    application.add_middleware(SlowAPIMiddleware)

    # Include API routers
    application.include_router(api_router, prefix="/api")

    return application


app = create_application()


@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    """Root endpoint for health check."""
    return {"message": "FastAPI App is running", "status": "healthy"}
