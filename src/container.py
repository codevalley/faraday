"""Dependency injection container for the Personal Semantic Engine.

This module provides a centralized container for managing dependencies and their
lifecycle throughout the application.
"""

import os

from dependency_injector import containers, providers

from src.domain.services.embedding_service import EmbeddingService
from src.domain.services.entity_extraction_service import EntityExtractionService
from src.domain.services.vector_store_service import VectorStoreService
from src.infrastructure.database.connection import Database
from src.infrastructure.llm.config import LLMConfigLoader
from src.infrastructure.llm.entity_extraction_service import LLMEntityExtractionService
from src.infrastructure.llm.llm_service import LLMService
from src.infrastructure.repositories.semantic_entry_repository import PostgreSQLSemanticEntryRepository
from src.infrastructure.repositories.thought_repository import PostgreSQLThoughtRepository
from src.infrastructure.repositories.user_repository import PostgreSQLUserRepository
from src.infrastructure.services.embedding_service import OpenAIEmbeddingService
from src.infrastructure.services.vector_store_service import PineconeVectorStore


class Container(containers.DeclarativeContainer):
    """Application container for dependency injection."""

    config = providers.Configuration()

    # Infrastructure
    db = providers.Singleton(Database, connection_string=config.db.connection_string)
    
    # LLM Configuration
    llm_config_loader = providers.Singleton(LLMConfigLoader)
    
    llm_service = providers.Singleton(
        LLMService,
        model=os.getenv("LLM_MODEL"),
        config_loader=llm_config_loader,
    )

    # Repositories
    thought_repository = providers.Singleton(
        PostgreSQLThoughtRepository,
        database=db,
    )
    
    user_repository = providers.Singleton(
        PostgreSQLUserRepository,
        database=db,
    )
    
    semantic_entry_repository = providers.Singleton(
        PostgreSQLSemanticEntryRepository,
        database=db,
    )

    # Services
    entity_extraction_service = providers.Singleton(
        LLMEntityExtractionService,
        llm_service=llm_service,
    )
    
    embedding_service = providers.Singleton(
        OpenAIEmbeddingService,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    vector_store_service = providers.Singleton(
        PineconeVectorStore,
        api_key=os.getenv("PINECONE_API_KEY"),
        environment=os.getenv("PINECONE_ENVIRONMENT"),
    )

    # Use cases
    # Will be added as we implement them


container = Container()