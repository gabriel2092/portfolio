"""
Clinical Trial Matching API
Main FastAPI application entry point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from dotenv import load_dotenv
import os

from api.routes import trials, matching
from core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting Clinical Trial Matching API")
    yield
    logger.info("Shutting down Clinical Trial Matching API")


# Initialize FastAPI app
app = FastAPI(
    title="Clinical Trial Matching API",
    description="Match patients to clinical trials using EMR data and AI-powered criteria analysis",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(trials.router, prefix="/api/trials", tags=["trials"])
app.include_router(matching.router, prefix="/api/matching", tags=["matching"])


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "status": "healthy",
        "service": "Clinical Trial Matching API",
        "version": "1.0.0"
    }


@app.get("/api/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "claude_api_configured": bool(settings.ANTHROPIC_API_KEY),
        "cache_enabled": settings.ENABLE_CACHE
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
