"""Thought management API routes."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse

from src.api.models.thought_models import (
    CreateThoughtRequest,
    ErrorResponse,
    ThoughtListResponse,
    ThoughtResponse,
    UpdateThoughtRequest,
)
from src.application.usecases.create_thought_usecase import CreateThoughtUseCase
from src.application.usecases.delete_thought_usecase import DeleteThoughtUseCase
from src.application.usecases.get_thought_by_id_usecase import GetThoughtByIdUseCase
from src.application.usecases.get_thoughts_usecase import GetThoughtsUseCase
from src.application.usecases.update_thought_usecase import UpdateThoughtUseCase
from src.domain.entities.user import User
from src.domain.exceptions import EntityExtractionError, ThoughtNotFoundError
from src.infrastructure.middleware.authentication_middleware import (
    AuthenticationMiddleware,
)


def create_thoughts_router(
    create_thought_usecase: CreateThoughtUseCase,
    get_thoughts_usecase: GetThoughtsUseCase,
    get_thought_by_id_usecase: GetThoughtByIdUseCase,
    update_thought_usecase: UpdateThoughtUseCase,
    delete_thought_usecase: DeleteThoughtUseCase,
    auth_middleware: AuthenticationMiddleware,
) -> APIRouter:
    """Create the thoughts API router.

    Args:
        create_thought_usecase: Use case for creating thoughts
        get_thoughts_usecase: Use case for getting thoughts
        get_thought_by_id_usecase: Use case for getting thought by ID
        update_thought_usecase: Use case for updating thoughts
        delete_thought_usecase: Use case for deleting thoughts
        auth_middleware: Authentication middleware

    Returns:
        Configured APIRouter for thoughts
    """
    router = APIRouter(prefix="/api/v1/thoughts", tags=["thoughts"])

    async def get_current_user(request: Request) -> User:
        """Dependency to get the current authenticated user."""
        return await auth_middleware.require_authentication(request)

    @router.post(
        "",
        response_model=ThoughtResponse,
        status_code=status.HTTP_201_CREATED,
        responses={
            400: {"model": ErrorResponse, "description": "Invalid input"},
            401: {"model": ErrorResponse, "description": "Authentication required"},
            422: {"model": ErrorResponse, "description": "Entity extraction failed"},
        },
    )
    async def create_thought(
        request: CreateThoughtRequest,
        current_user: User = Depends(get_current_user),
    ) -> ThoughtResponse:
        """Create a new thought with metadata capture.

        Args:
            request: The thought creation request
            current_user: The authenticated user

        Returns:
            The created thought with extracted semantic entries

        Raises:
            HTTPException: If creation fails
        """
        try:
            metadata = request.metadata.to_domain() if request.metadata else None
            
            thought = await create_thought_usecase.execute(
                user_id=current_user.id,
                content=request.content,
                metadata=metadata,
                timestamp=request.timestamp,
            )
            
            return ThoughtResponse.from_domain(thought)
            
        except EntityExtractionError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Entity extraction failed: {str(e)}",
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    @router.get(
        "",
        response_model=ThoughtListResponse,
        responses={
            401: {"model": ErrorResponse, "description": "Authentication required"},
            400: {"model": ErrorResponse, "description": "Invalid pagination parameters"},
        },
    )
    async def get_thoughts(
        skip: int = 0,
        limit: int = 100,
        current_user: User = Depends(get_current_user),
    ) -> ThoughtListResponse:
        """Get user's thoughts with pagination.

        Args:
            skip: Number of thoughts to skip for pagination
            limit: Maximum number of thoughts to return
            current_user: The authenticated user

        Returns:
            Paginated list of user's thoughts

        Raises:
            HTTPException: If retrieval fails
        """
        try:
            thoughts = await get_thoughts_usecase.execute(
                user_id=current_user.id,
                skip=skip,
                limit=limit,
            )
            
            # For now, we'll use the length of returned thoughts as total
            # In a real implementation, you'd want a separate count query
            total = len(thoughts)
            
            return ThoughtListResponse.from_domain_list(
                thoughts=thoughts,
                total=total,
                skip=skip,
                limit=limit,
            )
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    @router.get(
        "/{thought_id}",
        response_model=ThoughtResponse,
        responses={
            401: {"model": ErrorResponse, "description": "Authentication required"},
            403: {"model": ErrorResponse, "description": "Access denied"},
            404: {"model": ErrorResponse, "description": "Thought not found"},
        },
    )
    async def get_thought(
        thought_id: UUID,
        current_user: User = Depends(get_current_user),
    ) -> ThoughtResponse:
        """Get a specific thought by ID with entity details.

        Args:
            thought_id: The ID of the thought to retrieve
            current_user: The authenticated user

        Returns:
            The requested thought with semantic entries

        Raises:
            HTTPException: If retrieval fails
        """
        try:
            thought = await get_thought_by_id_usecase.execute(
                thought_id=thought_id,
                user_id=current_user.id,
            )
            
            return ThoughtResponse.from_domain(thought)
            
        except ThoughtNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Thought not found",
            )
        except ValueError as e:
            if "permission" in str(e).lower():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied",
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    @router.put(
        "/{thought_id}",
        response_model=ThoughtResponse,
        responses={
            400: {"model": ErrorResponse, "description": "Invalid input"},
            401: {"model": ErrorResponse, "description": "Authentication required"},
            403: {"model": ErrorResponse, "description": "Access denied"},
            404: {"model": ErrorResponse, "description": "Thought not found"},
            422: {"model": ErrorResponse, "description": "Entity extraction failed"},
        },
    )
    async def update_thought(
        thought_id: UUID,
        request: UpdateThoughtRequest,
        current_user: User = Depends(get_current_user),
    ) -> ThoughtResponse:
        """Update a thought with re-processing of entities.

        Args:
            thought_id: The ID of the thought to update
            request: The thought update request
            current_user: The authenticated user

        Returns:
            The updated thought with re-processed semantic entries

        Raises:
            HTTPException: If update fails
        """
        try:
            metadata = request.metadata.to_domain() if request.metadata else None
            
            thought = await update_thought_usecase.execute(
                thought_id=thought_id,
                user_id=current_user.id,
                content=request.content,
                metadata=metadata,
            )
            
            return ThoughtResponse.from_domain(thought)
            
        except ThoughtNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Thought not found",
            )
        except EntityExtractionError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Entity extraction failed: {str(e)}",
            )
        except ValueError as e:
            if "permission" in str(e).lower():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied",
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    @router.delete(
        "/{thought_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        responses={
            401: {"model": ErrorResponse, "description": "Authentication required"},
            403: {"model": ErrorResponse, "description": "Access denied"},
            404: {"model": ErrorResponse, "description": "Thought not found"},
        },
    )
    async def delete_thought(
        thought_id: UUID,
        current_user: User = Depends(get_current_user),
    ) -> None:
        """Delete a thought and its related entities.

        Args:
            thought_id: The ID of the thought to delete
            current_user: The authenticated user

        Raises:
            HTTPException: If deletion fails
        """
        try:
            await delete_thought_usecase.execute(
                thought_id=thought_id,
                user_id=current_user.id,
            )
            
        except ThoughtNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Thought not found",
            )
        except ValueError as e:
            if "permission" in str(e).lower():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied",
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    return router