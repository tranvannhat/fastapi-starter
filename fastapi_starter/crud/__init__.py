from .crud_item import item
from .crud_user import user
from .crud_user_profile import user_profile

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from fastapi_starter.models.item import Item
# from fastapi_starter.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
