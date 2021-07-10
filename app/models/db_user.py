from sqlalchemy import Boolean, Column, String
from app.models.base import BaseModel
from sqlalchemy.orm import relationship

class DbUser(BaseModel):
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    user_profile = relationship("DbUserProfile", back_populates="user")
