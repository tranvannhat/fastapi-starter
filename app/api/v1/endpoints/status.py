from fastapi import APIRouter, Request
from typing import Any
from starlette import status
from app.core.http import http_response_success
from app.schemas.base import ResponseSchemaBase

router = APIRouter()


@router.get("/status", response_model=ResponseSchemaBase)
def check_status(request: Request) -> Any:
    """Check status API"""
    return http_response_success(request, status_code=status.HTTP_200_OK)