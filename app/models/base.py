from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (String, BigInteger, Boolean, event)
import uuid
import time
from math import floor


def default_uuid():
    return str(uuid.uuid4())


def default_timestamp():
    return time.time()


def model_on_create_listener(mapper, connection, instance): # noqa
    if instance.created_at is None:
        instance.created_at = floor(time.time())
    if instance.updated_at is None:
        instance.updated_at = floor(time.time())


def model_on_update_listener(mapper, connection, instance):  # noqa
    instance.created_at = instance.created_at
    instance.updated_at = floor(time.time())
    if instance.deleted is True:
        instance.deleted_at = floor(time.time())


class BaseModel:
    id = Column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
    created_at = Column(BigInteger(), index=True)
    created_by = Column(String(), nullable=True)
    updated_at = Column(BigInteger())
    updated_by = Column(String(), nullable=True)
    deleted = Column(Boolean, default=False, index=True)
    deleted_by = Column(String(), nullable=True)
    deleted_at = Column(BigInteger())


event.listen(BaseModel, 'before_insert',
             model_on_create_listener, propagate=True)
event.listen(BaseModel, 'before_update',
             model_on_update_listener, propagate=True)
