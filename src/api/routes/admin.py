"""Admin API routes for the Personal Semantic Engine."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse

from src.api.models.admin_models import (
    CreateUserRequest,
    CreateUserResponse,
    ErrorResponse,
    HealthCheckResponse,
    UsersListResponse,
)
from src.application.usecases.create_user_usecase import CreateUserUseCase
from src.application.usecases.get_system_health_usecase import GetSystemHealthUseCase
from src.application.usecases.get_users_usecase import GetUsersUseCase
from src.container import container
from src.domain.entities.user import User
from src.domain.exceptions import UserAlreadyExistsError
from src.infrastructure.middleware.authentication_middleware import (
    AuthenticationMiddleware,
)

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


async def get_admin_user(request: Request) -> User:
    """Dependency to require admin authentication.

    Args:
        request: FastAPI request object

    Returns:
        The authenticated admin user

    Raises:
        HTTPException: If user is not authenticated or not an admin
    """
    auth_middleware: AuthenticationMiddleware = container.auth_middleware()
    return await auth_middleware.require_admin(request)


@router.get(
    "/users",
    response_model=UsersListResponse,
    summary="Get all users",
    description="Retrieve a paginated list of all users in the system. Admin access required.",
    responses={
        200: {"description": "Users retrieved successfully"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin access required"},
        500: {"description": "Internal server error"},
    },
)
async def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of users to return"),
    admin_user: User = Depends(get_admin_user),
) -> UsersListResponse:
    """Get all users with pagination.

    Args:
        skip: Number of users to skip for pagination
        limit: Maximum number of users to return
        admin_user: The authenticated admin user (injected by dependency)

    Returns:
        Paginated list of users

    Raises:
        HTTPException: If operation fails
    """
    try:
        get_users_usecase: GetUsersUseCase = container.get_users_usecase()
        users = await get_users_usecase.execute(skip=skip, limit=limit)

        # For simplicity, we'll use the returned count as total
        # In a real implementation, you might want a separate count query
        total = len(users) + skip

        return UsersListResponse.from_domain_list(
            users=users, total=total, skip=skip, limit=limit
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve users: {str(e)}",
        )


@router.post(
    "/users",
    response_model=CreateUserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user account. Admin access required.",
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Invalid request data"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin access required"},
        409: {"description": "User already exists"},
        500: {"description": "Internal server error"},
    },
)
async def create_user(
    request: CreateUserRequest,
    admin_user: User = Depends(get_admin_user),
) -> CreateUserResponse:
    """Create a new user.

    Args:
        request: User creation request data
        admin_user: The authenticated admin user (injected by dependency)

    Returns:
        The created user information

    Raises:
        HTTPException: If user creation fails
    """
    try:
        create_user_usecase: CreateUserUseCase = container.create_user_usecase()
        user = await create_user_usecase.execute(
            email=request.email,
            password=request.password,
            is_admin=request.is_admin,
            is_active=request.is_active,
        )

        return CreateUserResponse.from_domain(user)

    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}",
        )


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="System health check",
    description="Get system health and status information. Admin access required.",
    responses={
        200: {"description": "Health check completed"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin access required"},
        500: {"description": "Health check failed"},
    },
)
async def get_system_health(
    admin_user: User = Depends(get_admin_user),
) -> HealthCheckResponse:
    """Get system health information.

    Args:
        admin_user: The authenticated admin user (injected by dependency)

    Returns:
        System health information

    Raises:
        HTTPException: If health check fails
    """
    try:
        get_health_usecase: GetSystemHealthUseCase = container.get_system_health_usecase()
        health_data = await get_health_usecase.execute()

        return HealthCheckResponse(**health_data)

    except Exception as e:
        # Even if health check fails, we want to return some information
        return HealthCheckResponse(
            timestamp=str(e),
            status="unhealthy",
            services={"health_check": {"status": "failed", "message": str(e)}},
            statistics={"error": "Health check failed"},
        )