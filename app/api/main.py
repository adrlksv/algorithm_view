from fastapi import FastAPI

from api.handlers.jwt_auth.router import router as jwt_auth_router
from api.handlers.oauth.router import router as github_oauth_router
from api.handlers.algorithms.router import router as algorithm_router


def create_app() -> FastAPI:
    app = FastAPI(
        docs_url="/api/docs",
        description="Generate crypto key project",
        debug=True,
        title="Generate key",
    )
    
    app.include_router(jwt_auth_router)
    app.include_router(github_oauth_router)
    app.include_router(algorithm_router)
    
    return app
