from pydantic import BaseModel
from starlette import status


class Success(BaseModel):
    code: int = status.HTTP_200_OK
    message: str = "Success"
