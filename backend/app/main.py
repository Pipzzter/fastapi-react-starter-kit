from app.api.v1.routers import api_router
from app.core.config import get_settings
from app.middleware import register_middlewares
from fastapi import FastAPI


def create_app() -> FastAPI:
    settings = get_settings()
    app_instance = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        docs_url=f"{settings.api_v1_prefix}/docs" if settings.api_v1_prefix else None,
    )
    register_middlewares(app_instance)
    app_instance.include_router(api_router, prefix=settings.api_v1_prefix)
    return app_instance


app = create_app()
