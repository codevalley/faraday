"""FastAPI application for the Personal Semantic Engine."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.container import container


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application
    """
    app = FastAPI(
        title="Personal Semantic Engine (Faraday)",
        description="A unified, searchable repository of personal data with semantic understanding",
        version="0.1.0",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Update for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    # Will be added as we implement them

    # Dependency injection
    app.container = container

    return app


app = create_app()