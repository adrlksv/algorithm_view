from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse

from db.database import get_db
from services.auth.oauth_providers.github import (
    get_github_auth_url, 
    exchange_code_for_token, 
    get_github_user
)
from repository.users.user_repository import UsersRepository
from services.auth.jwt.jwt_auth import create_access_token, create_refresh_token

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/oauth", 
    tags=["Oauth"]
)


@router.get("/github/login")
async def github_login():
    return RedirectResponse(get_github_auth_url())


@router.get("/github/callback")
async def github_callback(request: Request, response: Response, session: AsyncSession = Depends(get_db)):
    code = request.query_params.get("code")
    if not code:
        return {
            "error": "Authorization failed"
        }

    token = await exchange_code_for_token(code)
    user_data = await get_github_user(token)

    email = user_data.get("email")
    if not email:
        email = f"{user_data['id']}@github.com"

    existing_user = await UsersRepository.find_one_or_none(session=session, email=email)

    if not existing_user:
        await UsersRepository.add(
            session=session,
            email=email,
            username=user_data["login"],
            hashed_password="github_auth",
        )
        existing_user = await UsersRepository.find_one_or_none(session=session, email=email)

    access_token = create_access_token({"sub": str(existing_user.user_id)})
    refresh_token = create_refresh_token({"sub": str(existing_user.user_id)})

    response.set_cookie(
        key="refer_access_token",
        value=access_token,
        httponly=True,
        samesite="Lax",
        secure=False,
        path="/",
    )
    response.set_cookie(
        key="refer_refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="Lax",
        secure=False,
        path="/",
    )

    return {
        "message": "Успешная аутентификация",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": existing_user.user_id,
            "email": existing_user.email,
            "username": existing_user.username
        }
    }
