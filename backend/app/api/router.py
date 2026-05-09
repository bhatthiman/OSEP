from fastapi import APIRouter

from app.api.routes import (
    projects,
    components,
    build
)

api_router = APIRouter()

api_router.include_router(
    projects.router,
    prefix="/projects",
    tags=["Projects"]
)

api_router.include_router(
    components.router,
    prefix="/components",
    tags=["Components"]
)

api_router.include_router(
    build.router,
    prefix="/build",
    tags=["Build"]
)
