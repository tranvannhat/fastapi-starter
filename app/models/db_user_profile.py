from sqlalchemy import Boolean, Column, String, ForeignKey
from app.models.base import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

class DbUserProfile(BaseModel):
    first_name = Column(String, default=None)
    middle_name = Column(String, default=None)
    last_name = Column(String, default=None)
    dob = Column(String, default=None)
    gender = Column(String, default=None)
    avatar = Column(String, default=None)
    bio = Column(String, default=None)
    following = Column(Boolean(), default=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("db_user.id"))
    user = relationship("DbUser", back_populates="user_profile")