"""
Main FastAPI application for LVBK system.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import os
from typing import Dict, Any

from .endpoints import router
from ..utils import setup_logging

# Set up logging
logger = setup_logging(__name__)


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title="LVBK Martial Arts Computer Vision AI System",
        description="AI system for analyzing martial arts techniques through computer vision",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Configure trusted hosts
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Configure appropriately for production
    )
    
    # Include API routes
    app.include_router(router, prefix="/api")
    
    @app.get("/health")
    async def health_check() -> Dict[str, Any]:
        """
        Health check endpoint.
        
        Returns:
            Dict[str, Any]: Health status information
        """
        return {
            "status": "healthy",
            "version": "0.1.0",
            "service": "LVBK API"
        }
    
    @app.get("/")
    async def root() -> Dict[str, str]:
        """
        Root endpoint.
        
        Returns:
            Dict[str, str]: Welcome message
        """
        return {
            "message": "Welcome to LVBK Martial Arts Computer Vision AI System",
            "docs": "/docs",
            "health": "/health"
        }
    
    logger.info("LVBK API application created successfully")
    return app


# Create app instance for uvicorn
app = create_app()

