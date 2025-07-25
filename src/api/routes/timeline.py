"""Timeline API routes for the Personal Semantic Engine."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from src.api.models.timeline_models import (
    RelatedEntriesResponse,
    TimelineRequest,
    TimelineResponse,
    TimelineSummaryResponse,
)
from src.api.models.thought_models import ErrorResponse
from src.application.usecases.get_timeline_usecase import GetTimelineUseCase
from src.domain.entities.enums import EntityType
from src.domain.entities.timeline import DateRange
from src.domain.entities.user import User
from src.domain.exceptions import TimelineError, TimelineQueryError
from src.infrastructure.middleware.authentication_middleware import (
    AuthenticationMiddleware,
)


def create_timeline_router(
    get_timeline_usecase: GetTimelineUseCase,
    auth_middleware: AuthenticationMiddleware,
) -> APIRouter:
    """Create the timeline API router.

    Args:
        get_timeline_usecase: Use case for timeline operations
        auth_middleware: Authentication middleware

    Returns:
        Configured APIRouter for timeline operations
    """
    router = APIRouter(prefix="/api/v1/timeline", tags=["timeline"])

    async def get_current_user(request: Request) -> User:
        """Dependency to get the current authenticated user."""
        return await auth_middleware.require_authentication(request)

    @router.get(
        "",
        response_model=TimelineResponse,
        responses={
            400: {"model": ErrorResponse, "description": "Invalid query parameters"},
            401: {"model": ErrorResponse, "description": "Authentication required"},
            422: {"model": ErrorResponse, "description": "Timeline query parsing failed"},
        },
    )
    async def get_timeline(
        start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
        end_date: Optional[str] = Query(None, description="End date (ISO format)"),
        entity_types: List[EntityType] = Query([], description="Filter by entity types"),
        data_sources: List[str] = Query([], description="Filter by data sources"),
        tags: List[str] = Query([], description="Filter by tags"),
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(20, ge=1, le=100, description="Items per page"),
        sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Sort order"),
        include_groups: bool = Query(False, description="Include grouped entries"),
        include_summary: bool = Query(False, description="Include timeline summary"),
        current_user: User = Depends(get_current_user),
    ) -> TimelineResponse:
        """Get user's timeline with optional filtering and pagination.

        This endpoint returns a chronological view of the user's thoughts and
        extracted entities, with support for date range filtering, entity type
        filtering, and pagination.

        Args:
            start_date: Optional start date for filtering (ISO format)
            end_date: Optional end date for filtering (ISO format)
            entity_types: Optional list of entity types to filter by
            data_sources: Optional list of data sources to filter by
            tags: Optional list of tags to filter by
            page: Page number for pagination
            page_size: Number of items per page
            sort_order: Sort order ("asc" or "desc")
            include_groups: Whether to include grouped entries
            include_summary: Whether to include timeline summary
            current_user: The authenticated user

        Returns:
            Timeline response with entries and metadata

        Raises:
            HTTPException: If timeline retrieval fails
        """
        try:
            # Parse date range if provided
            date_range = None
            if start_date or end_date:
                from datetime import datetime
                
                parsed_start = None
                parsed_end = None
                
                if start_date:
                    try:
                        parsed_start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                    except ValueError:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid start_date format. Use ISO format."
                        )
                
                if end_date:
                    try:
                        parsed_end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                    except ValueError:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid end_date format. Use ISO format."
                        )
                
                date_range = DateRange(
                    start_date=parsed_start,
                    end_date=parsed_end
                )

            # Execute timeline retrieval
            timeline_response = await get_timeline_usecase.execute(
                user_id=current_user.id,
                date_range=date_range,
                entity_types=entity_types if entity_types else None,
                data_sources=data_sources if data_sources else None,
                tags=tags if tags else None,
                page=page,
                page_size=page_size,
                sort_order=sort_order,
            )

            return TimelineResponse.from_domain(timeline_response)

        except TimelineQueryError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Timeline query parsing failed: {str(e)}",
            )
        except TimelineError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Timeline retrieval failed: {str(e)}",
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
        "/summary",
        response_model=TimelineSummaryResponse,
        responses={
            400: {"model": ErrorResponse, "description": "Timeline summary generation failed"},
            401: {"model": ErrorResponse, "description": "Authentication required"},
        },
    )
    async def get_timeline_summary(
        current_user: User = Depends(get_current_user),
    ) -> TimelineSummaryResponse:
        """Get timeline summary statistics for the user.

        This endpoint provides summary statistics about the user's timeline,
        including total entries, date range, entity counts, and activity patterns.

        Args:
            current_user: The authenticated user

        Returns:
            Timeline summary with statistics

        Raises:
            HTTPException: If summary generation fails
        """
        try:
            summary = await get_timeline_usecase.get_summary(current_user.id)
            return TimelineSummaryResponse.from_domain(summary)

        except TimelineError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Timeline summary generation failed: {str(e)}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    @router.get(
        "/entries/{entry_id}/related",
        response_model=RelatedEntriesResponse,
        responses={
            400: {"model": ErrorResponse, "description": "Invalid request parameters"},
            401: {"model": ErrorResponse, "description": "Authentication required"},
            404: {"model": ErrorResponse, "description": "Entry not found"},
        },
    )
    async def get_related_entries(
        entry_id: str,
        limit: int = Query(10, ge=1, le=50, description="Maximum number of related entries"),
        current_user: User = Depends(get_current_user),
    ) -> RelatedEntriesResponse:
        """Get entries related to a specific timeline entry.

        This endpoint finds and returns timeline entries that are related to
        the specified entry based on shared entities, temporal proximity,
        and semantic similarity.

        Args:
            entry_id: ID of the entry to find relations for
            limit: Maximum number of related entries to return
            current_user: The authenticated user

        Returns:
            Related entries response

        Raises:
            HTTPException: If related entries retrieval fails
        """
        try:
            related_entries = await get_timeline_usecase.get_related_entries(
                entry_id=entry_id,
                user_id=current_user.id,
                limit=limit,
            )

            from src.api.models.timeline_models import TimelineEntryResponse
            
            return RelatedEntriesResponse(
                entry_id=entry_id,
                related_entries=[
                    TimelineEntryResponse.from_domain(entry)
                    for entry in related_entries
                ],
                total_count=len(related_entries),
            )

        except TimelineQueryError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
        except TimelineError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Related entries retrieval failed: {str(e)}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    return router