from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.router import router as v1_router
from app.api.health.router import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, debug=settings.debug)

    app.include_router(health_router)
    app.include_router(v1_router, prefix="/api/v1")

    return app


app = create_app()
