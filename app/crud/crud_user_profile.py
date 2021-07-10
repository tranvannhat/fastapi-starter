from typing import List

from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.db_user_profile import DbUserProfile
from app.schemas.user_profile import UserProfileCreate, UserProfileUpdate


class CRUDUserProfile(CRUDBase[DbUserProfile, UserProfileCreate, UserProfileUpdate]):
    def get_by_user_id(self, db: Session, *, user_id: str) -> List[DbUserProfile]:
        return db.query(self.model).filter(DbUserProfile.user_id == user_id).first()


user_profile = CRUDUserProfile(DbUserProfile)
