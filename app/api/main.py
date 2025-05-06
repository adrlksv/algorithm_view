from fastapi import FastAPI

from handlers.jwt_auth.router import router as jwt_auth_router


async def create_app() -> FastAPI:
    app = FastAPI(
        docs_url="/api/docs",
        description="Generate crypto key project",
        debug=True,
        title="Generate key",
    )
    
    app.include_router(jwt_auth_router)
    
    return app
