from fastapi import APIRouter

from app.api.v1.endpoints import (status)

api_router = APIRouter()
api_router.include_router(status.router, tags=["StarterAPI"])