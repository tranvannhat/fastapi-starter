from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from fastapi_starter.core.security import get_password_hash, verify_password
from fastapi_starter.crud.base import CRUDBase
from fastapi_starter.models.db_user import DbUser
from fastapi_starter.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[DbUser, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[DbUser]:
        return db.query(DbUser).filter(DbUser.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> DbUser:
        db_obj = DbUser(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: DbUser, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> DbUser:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[DbUser]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: DbUser) -> bool:
        return user.is_active

    def is_superuser(self, user: DbUser) -> bool:
        return user.is_superuser


user = CRUDUser(DbUser)
