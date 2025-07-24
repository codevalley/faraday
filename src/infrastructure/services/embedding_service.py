"""OpenAI embedding service implementation."""

import os
from typing import List

import openai
from openai import AsyncOpenAI

from src.domain.exceptions import EmbeddingError
from src.domain.services.embedding_service import EmbeddingService


class OpenAIEmbeddingService(EmbeddingService):
    """Implementation of EmbeddingService using OpenAI's embeddings API."""

    def __init__(
        self,
        api_key: str = None,
        model: str = "text-embedding-ada-002",
        batch_size: int = 100,
    ):
        """Initialize the OpenAI embedding service.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: The embedding model to use
            batch_size: Maximum number of texts to embed in a single API call
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")

        self.model = model
        self.batch_size = batch_size
        self.client = AsyncOpenAI(api_key=self.api_key)

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate a vector embedding for the given text.

        Args:
            text: The text to generate an embedding for

        Returns:
            A vector embedding representing the text

        Raises:
            EmbeddingError: If embedding generation fails
        """
        if not text.strip():
            raise EmbeddingError("Cannot generate embedding for empty text")

        try:
            response = await self.client.embeddings.create(
                model=self.model,
                input=text,
            )
            return response.data[0].embedding
        except Exception as e:
            raise EmbeddingError(f"Failed to generate embedding: {str(e)}")

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate vector embeddings for multiple texts.

        Args:
            texts: The texts to generate embeddings for

        Returns:
            A list of vector embeddings representing the texts

        Raises:
            EmbeddingError: If embedding generation fails
        """
        if not texts:
            return []

        # Filter out empty texts
        valid_texts = [text for text in texts if text.strip()]
        if not valid_texts:
            raise EmbeddingError("Cannot generate embeddings for empty texts")

        try:
            # Process in batches to avoid API limits
            results = []
            for i in range(0, len(valid_texts), self.batch_size):
                batch = valid_texts[i:i + self.batch_size]
                response = await self.client.embeddings.create(
                    model=self.model,
                    input=batch,
                )
                # Sort by index to maintain original order
                sorted_embeddings = sorted(response.data, key=lambda x: x.index)
                batch_embeddings = [item.embedding for item in sorted_embeddings]
                results.extend(batch_embeddings)
            return results
        except Exception as e:
            raise EmbeddingError(f"Failed to generate embeddings: {str(e)}")