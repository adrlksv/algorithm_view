from fastapi import APIRouter, Request, Response, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth_depends import get_current_user
from app.db.database import get_db

from app.db.users.models import User

from app.exceptions.exceptions import IncorrectEmailOrPasswordException, TokenAbsentException, UserAlreadyExistsException
from app.repository.users.user_repository import UsersRepository
from app.schemas.users.schemas import SUserCreate, SUserLogin
from app.services.auth.jwt.jwt_auth import (
    authenticate_user, 
    create_access_token,
    create_refresh_token, 
    get_password_hash
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
async def register_user(user_data: SUserCreate, session: AsyncSession = Depends(get_db)):
    existing_user = await UsersRepository.find_one_or_none(email=user_data.email, session=session)
    if existing_user:
        raise UserAlreadyExistsException
    
    hashed_password = get_password_hash(user_data.password)
    await UsersRepository.add(
        session=session,
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password
    )


@router.post("/login")
async def login_user(response: Response, user_data: SUserLogin, session: AsyncSession = Depends(get_db)):
    user = await authenticate_user(
        session=session,
        email=user_data.email, 
        password=user_data.password
    )
    if not user:
        raise IncorrectEmailOrPasswordException
    
    access_token = create_access_token({"sub": str(user.user_id)})
    refresh_token = create_refresh_token({"sub": str(user.user_id)})

    response.set_cookie(
        "refer_access_token",
        access_token,
        httponly=True,
        samesite="strict",
    )
    response.set_cookie(
        "refer_refresh_token",
        refresh_token,
        httponly=True,
        samesite="strict"
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.post("/refresh")
async def refresh_token(
    request: Request, 
    response: Response, 
    session: AsyncSession = Depends(get_db)
):
    refresh_token = request.cookies.get("refer_refresh_token")
    if not refresh_token:
        raise TokenAbsentException
    
    user = await get_current_user(session=session,
                                  token=refresh_token)
    new_access_token = create_access_token({"sub": str(user.user_id)})

    response.set_cookie(
        "refer_access_token",
        new_access_token,
        httponly=True,
        samesite="strict"
    )

    return {
        "access_token": new_access_token
    }


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("refer_access_token")
    response.delete_cookie("refer_refresh_token")


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
