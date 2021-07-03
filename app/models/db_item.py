from sqlalchemy import Column, String
from app.models.base import BaseModel

class DbItem(BaseModel):
    title = Column(String, index=True)
    description = Column(String, index=True)
