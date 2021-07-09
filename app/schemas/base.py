from typing import Optional, TypeVar, Generic
from pydantic.generics import GenericModel
from fastapi import Request
from pydantic import BaseModel
from starlette import status

from app.utils import generate_track_id

T = TypeVar("T")


class ResponseSchemaBase(BaseModel):
    __abstract__ = True

    ip: str = None
    track_id: str = None

    def error_response(self, request: Request, error: T):
        return {
            "track_id": f'{request.client.host.replace(".", "")}{generate_track_id()}E',
            "ip": f'{request.client.host}',
            "error": error
        }


class DataResponse(ResponseSchemaBase, GenericModel, Generic[T]):
    data: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True

    def success_response(self, request: Request, data: T):
        return {
            "track_id": f'{request.client.host.replace(".", "")}{generate_track_id()}S',
            "ip": f'{request.client.host}',
            "data": data
        }
