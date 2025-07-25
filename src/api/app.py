"""FastAPI application for the Personal Semantic Engine."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.container import container
from src.api.routes.thoughts import create_thoughts_router
from src.api.routes.search import create_search_router
from src.api.routes.timeline import create_timeline_router
from src.api.routes.admin import router as admin_router


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

    # Dependency injection
    app.container = container

    # Include routers
    thoughts_router = create_thoughts_router(
        create_thought_usecase=container.create_thought_usecase(),
        get_thoughts_usecase=container.get_thoughts_usecase(),
        get_thought_by_id_usecase=container.get_thought_by_id_usecase(),
        update_thought_usecase=container.update_thought_usecase(),
        delete_thought_usecase=container.delete_thought_usecase(),
        auth_middleware=container.auth_middleware(),
    )
    app.include_router(thoughts_router)

    search_router = create_search_router(
        search_thoughts_usecase=container.search_thoughts_usecase(),
        auth_middleware=container.auth_middleware(),
    )
    app.include_router(search_router)

    timeline_router = create_timeline_router(
        get_timeline_usecase=container.get_timeline_usecase(),
        auth_middleware=container.auth_middleware(),
    )
    app.include_router(timeline_router)

    # Include admin router
    app.include_router(admin_router)

    return app


# Only create app if running as main module
if __name__ == "__main__":
    app = create_app()
else:
    app = None
