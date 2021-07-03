from datetime import datetime

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr


def to_underscore(name):
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

@as_declarative()
class Base:
    __abstract__ = True
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        return to_underscore(self.__name__)


class BareBaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)