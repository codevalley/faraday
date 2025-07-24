"""Pinecone vector store service implementation."""

import os
from typing import Dict, List, Optional
from uuid import UUID

import pinecone

from src.domain.entities.enums import EntityType
from src.domain.exceptions import VectorStoreError
from src.domain.services.vector_store_service import (
    VectorSearchResult as BaseVectorSearchResult,
)
from src.domain.services.vector_store_service import VectorStoreService


class VectorSearchResult(BaseVectorSearchResult):
    """Result of a vector search operation."""

    def __init__(self, id: str, score: float, metadata: Dict[str, str]):
        """Initialize a vector search result.

        Args:
            id: The unique identifier of the vector
            score: The similarity score (0-1)
            metadata: Additional metadata associated with the vector
        """
        self.id = id
        self.score = score
        self.metadata = metadata


class PineconeVectorStore(VectorStoreService):
    """Implementation of VectorStoreService using Pinecone."""

    def __init__(
        self,
        api_key: str = None,
        environment: str = None,
        index_name: str = "semantic-engine",
        namespace: str = "default",
        dimension: int = 1536,  # Default for text-embedding-ada-002
    ):
        """Initialize the Pinecone vector store.

        Args:
            api_key: Pinecone API key (defaults to PINECONE_API_KEY env var)
            environment: Pinecone environment (defaults to PINECONE_ENVIRONMENT env var)
            index_name: Name of the Pinecone index
            namespace: Default namespace for vectors
            dimension: Dimension of the vectors (1536 for OpenAI ada-002)
        """
        self.api_key = api_key or os.getenv("PINECONE_API_KEY")
        if not self.api_key:
            raise ValueError("Pinecone API key is required")

        self.environment = environment or os.getenv("PINECONE_ENVIRONMENT")
        if not self.environment:
            raise ValueError("Pinecone environment is required")

        self.index_name = index_name
        self.namespace = namespace
        self.dimension = dimension

        # Initialize Pinecone
        pinecone.init(api_key=self.api_key, environment=self.environment)

        # Ensure index exists
        self._ensure_index_exists()

        # Get the index
        self.index = pinecone.Index(self.index_name)

    def _ensure_index_exists(self) -> None:
        """Ensure the Pinecone index exists, creating it if necessary."""
        try:
            # List existing indexes
            existing_indexes = pinecone.list_indexes()

            # Create index if it doesn't exist
            if self.index_name not in existing_indexes:
                pinecone.create_index(
                    name=self.index_name, dimension=self.dimension, metric="cosine"
                )
        except Exception as e:
            raise VectorStoreError(f"Failed to ensure index exists: {str(e)}")

    async def store_vector(
        self, id: str, vector: List[float], metadata: Dict[str, str]
    ) -> None:
        """Store a vector in the vector database.

        Args:
            id: Unique identifier for the vector
            vector: The vector to store
            metadata: Additional metadata to store with the vector

        Raises:
            VectorStoreError: If storage fails
        """
        try:
            self.index.upsert(
                vectors=[{"id": id, "values": vector, "metadata": metadata}],
                namespace=self.namespace,
            )
        except Exception as e:
            raise VectorStoreError(f"Failed to store vector: {str(e)}")

    async def search(
        self,
        query_vector: List[float],
        top_k: int = 10,
        entity_type: Optional[EntityType] = None,
        user_id: Optional[UUID] = None,
    ) -> List[VectorSearchResult]:
        """Search for similar vectors.

        Args:
            query_vector: The vector to search for
            top_k: Maximum number of results to return
            entity_type: Optional filter by entity type
            user_id: Optional filter by user ID

        Returns:
            A list of search results ordered by similarity

        Raises:
            VectorStoreError: If search fails
        """
        try:
            # Build filter if needed
            filter_dict = {}
            if entity_type:
                filter_dict["entity_type"] = entity_type.value
            if user_id:
                filter_dict["user_id"] = str(user_id)

            # Execute search
            response = self.index.query(
                vector=query_vector,
                top_k=top_k,
                namespace=self.namespace,
                filter=filter_dict if filter_dict else None,
                include_metadata=True,
            )

            # Convert to domain objects
            results = []
            for match in response.matches:
                result = VectorSearchResult(
                    id=match.id, score=match.score, metadata=match.metadata
                )
                results.append(result)

            return results
        except Exception as e:
            raise VectorStoreError(f"Failed to search vectors: {str(e)}")

    async def delete_vectors(self, ids: List[str]) -> None:
        """Delete vectors from the vector database.

        Args:
            ids: List of vector IDs to delete

        Raises:
            VectorStoreError: If deletion fails
        """
        try:
            self.index.delete(ids=ids, namespace=self.namespace)
        except Exception as e:
            raise VectorStoreError(f"Failed to delete vectors: {str(e)}")
