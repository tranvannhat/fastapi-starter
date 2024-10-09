from fastapi import APIRouter, Request
from typing import Any
from fastapi_starter import schemas
from fastapi_starter.schemas.base import DataResponse

router = APIRouter()


@router.get("/status", response_model=DataResponse[schemas.Success])
def check_status(request: Request) -> Any:
    """Check status API"""
    return DataResponse().success_response(request, {})