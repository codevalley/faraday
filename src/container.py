"""Dependency injection container for the Personal Semantic Engine.

This module provides a centralized container for managing dependencies and their
lifecycle throughout the application.
"""

from dependency_injector import containers, providers

from src.infrastructure.database.connection import Database


class Container(containers.DeclarativeContainer):
    """Application container for dependency injection."""

    config = providers.Configuration()

    # Infrastructure
    db = providers.Singleton(Database, connection_string=config.db.connection_string)

    # Repositories
    # Will be added as we implement them

    # Services
    # Will be added as we implement them

    # Use cases
    # Will be added as we implement them


container = Container()