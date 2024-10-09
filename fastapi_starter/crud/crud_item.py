from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from fastapi_starter.crud.base import CRUDBase
from fastapi_starter.models.db_item import DbItem
from fastapi_starter.schemas.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[DbItem, ItemCreate, ItemUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: ItemCreate, owner_id: int
    ) -> DbItem:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[DbItem]:
        return (
            db.query(self.model)
            .filter(DbItem.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


item = CRUDItem(DbItem)
