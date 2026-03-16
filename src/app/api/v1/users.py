from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.db.gateway import DBGateway
from app.db.session import get_gateway
from app.schemas.user import UserCreateIn, UserOut, UserUpdateIn

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreateIn,
    gw: DBGateway = Depends(get_gateway),
) -> UserOut:
    repo = gw.users()

    existing = await repo.get_by_login(payload.login)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="login already exists",
        )

    created = await repo.create(
        {
            "login": payload.login,
            "display_name": payload.display_name,
            "password_hash": payload.password_hash,
            "is_platform_admin": payload.is_platform_admin,
        }
    )
    if not created:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to create user",
        )

    return UserOut.model_validate(created)


@router.get("", response_model=list[UserOut])
async def list_users(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
    gw: DBGateway = Depends(get_gateway),
) -> list[UserOut]:
    users = await gw.users().get_many(offset=offset, limit=limit)
    return [UserOut.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: UUID,
    gw: DBGateway = Depends(get_gateway),
) -> UserOut:
    user = await gw.users().get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )
    return UserOut.model_validate(user)


@router.get("/by-login/{login}", response_model=UserOut)
async def get_user_by_login(
    login: str,
    gw: DBGateway = Depends(get_gateway),
) -> UserOut:
    user = await gw.users().get_by_login(login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )
    return UserOut.model_validate(user)


@router.patch("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: UUID,
    payload: UserUpdateIn,
    gw: DBGateway = Depends(get_gateway),
) -> UserOut:
    update_data = payload.model_dump(exclude_none=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="empty update payload",
        )

    existing = await gw.users().get_by_id(user_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )

    updated = await gw.users().update(user_id, update_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to update user",
        )

    return UserOut.model_validate(updated)