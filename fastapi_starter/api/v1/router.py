from fastapi import APIRouter

from fastapi_starter.api.v1.endpoints import (status, authen, users)

api_router = APIRouter()
api_router.include_router(status.router, tags=["StarterAPI"])
api_router.include_router(authen.router, tags=["Authen"])
api_router.include_router(users.router, prefix="/user", tags=["Users"])