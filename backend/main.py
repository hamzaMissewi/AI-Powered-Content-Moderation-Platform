import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text

from app.core.config import settings
from app.api.v1.api import api_router
from app.db.session import engine, Base, SessionLocal
from app.core.logging_config import setup_logging
from app.core.middleware import LoggingMiddleware, RateLimitMiddleware
from app.core.exceptions import (
    ContentModerationException,
    ContentValidationError,
    FileUploadError,
    ModelLoadError,
    RateLimitExceeded
)

# Configure logging
logger = logging.getLogger(__name__)
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    # Startup: Initialize database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

    # Verify database connection
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("Database connection verified")
    except Exception as e:
        logger.warning(f"Database connection check failed: {e}")

    yield  # Application runs here

    # Shutdown: Clean up resources
    logger.info("Shutting down application...")

def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="AI-powered content moderation API with user authentication",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
    )

    # Set up CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add custom middleware
    app.add_middleware(LoggingMiddleware)
    if settings.RATE_LIMIT_ENABLED:
        app.add_middleware(RateLimitMiddleware)

    # Custom exception handlers
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle request validation errors."""
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({
                "detail": exc.errors(),
                "body": exc.body,
            }),
        )
    
    @app.exception_handler(ContentModerationException)
    async def content_moderation_exception_handler(request: Request, exc: ContentModerationException):
        """Handle content moderation specific exceptions."""
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers,
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Handle all other exceptions."""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )

    # Include API routers
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # Health check endpoint
    @app.get("/health", tags=["health"])
    async def health_check() -> dict:
        """Comprehensive health check endpoint."""
        db_status = check_db_connection()
        return {
            "status": "healthy" if db_status else "degraded",
            "version": "1.0.0",
            "environment": settings.ENVIRONMENT,
            "database": "connected" if db_status else "disconnected",
            "rate_limiting": "enabled" if settings.RATE_LIMIT_ENABLED else "disabled"
        }
    
    @app.get("/", tags=["root"])
    async def root():
        """Root endpoint with API information."""
        return {
            "message": "Smart Content Moderation API",
            "version": "1.0.0",
            "docs": "/api/docs",
            "health": "/health"
        }

    return app

def check_db_connection() -> bool:
    """Check if the database is accessible."""
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return True
    except Exception:
        return False

app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        workers=4,
    )
