from typing import Optional
from uuid import UUID
from pydantic import BaseModel


# Shared properties
class UserProfileBase(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    user_id: Optional[UUID] = None


# Properties to receive via API on creation
class UserProfileCreate(UserProfileBase):
    pass


# Properties to receive via API on update
class UserProfileUpdate(UserProfileBase):
    pass


class UserProfileInDBBase(UserProfileBase):

    class Config:
        orm_mode = True


# Additional properties to return via API
class UserProfile(UserProfileInDBBase):
    pass


# Additional properties stored in DB
class UserProfileInDB(UserProfileInDBBase):
    pass
