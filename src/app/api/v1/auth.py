from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.db.gateway import DBGateway
from app.db.session import get_gateway
from app.schemas.auth import LoginIn, TokenOut
from app.services.auth_service import authenticate_user, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login", response_model=TokenOut)
async def login(
    payload: LoginIn,
    gw: DBGateway = Depends(get_gateway),
) -> TokenOut:
    user = await authenticate_user(
        gw,
        login=payload.login,
        password=payload.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login or password",
        )

    access_token = create_access_token(subject=str(user.id))
    return TokenOut(access_token=access_token)