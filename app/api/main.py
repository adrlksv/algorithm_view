from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.handlers.jwt_auth.router import router as jwt_auth_router
from app.api.handlers.oauth.router import router as github_oauth_router
from app.api.handlers.crypto.aes.router import router as aes_router
from app.api.handlers.crypto.rsa.router import router as rsa_router
from app.api.handlers.crypto.ecc.router import router as ecc_router


origins = [
    "http://localhost:5173",
    "http://192.168.0.12:5173",
]


def create_app() -> FastAPI:
    app = FastAPI(
        docs_url="/api/docs",
        description="Generate crypto key project",
        debug=True,
        title="Generate key",
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "UPDATE", "OPTIONS"],
        allow_headers=["*"],
    )
    
    app.include_router(jwt_auth_router)
    app.include_router(github_oauth_router)
    app.include_router(aes_router)
    app.include_router(rsa_router)
    app.include_router(ecc_router)
    
    return app
