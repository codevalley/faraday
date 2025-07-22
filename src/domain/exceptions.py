"""Domain exceptions for the Personal Semantic Engine."""

from uuid import UUID


class DomainError(Exception):
    """Base exception for domain layer errors."""

    pass


class ThoughtNotFoundError(DomainError):
    """Raised when a thought cannot be found."""

    def __init__(self, thought_id: UUID):
        super().__init__(f"Thought with ID {thought_id} not found")
        self.thought_id = thought_id


class UserNotFoundError(DomainError):
    """Raised when a user cannot be found."""

    def __init__(self, user_id: UUID = None, email: str = None):
        if user_id:
            super().__init__(f"User with ID {user_id} not found")
            self.user_id = user_id
        elif email:
            super().__init__(f"User with email {email} not found")
            self.email = email
        else:
            super().__init__("User not found")


class EntityExtractionError(DomainError):
    """Raised when entity extraction fails."""

    def __init__(self, message: str):
        super().__init__(f"Entity extraction failed: {message}")


class EmbeddingError(DomainError):
    """Raised when embedding generation fails."""

    def __init__(self, message: str):
        super().__init__(f"Embedding generation failed: {message}")


class VectorStoreError(DomainError):
    """Raised when vector storage or retrieval fails."""

    def __init__(self, message: str):
        super().__init__(f"Vector store operation failed: {message}")


class AuthenticationError(DomainError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message)