from fastapi import APIRouter
from typing import Any

router = APIRouter()


@router.get("/status")
def status() -> Any:
    """Check status API"""
    return {"message": "API Online"}