from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.core.exception_handler import CustomException
from app.schemas.base import DataResponse
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/user", response_model=DataResponse[List[schemas.User]])
def read_users(
        request: Request,
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.DbUser = Depends(deps.get_current_active_superuser),  # noqa
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return DataResponse().success_response(request, users)


@router.post("/user", response_model=DataResponse[schemas.User])
def create_user(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        user_in: schemas.UserCreate,
        current_user: models.DbUser = Depends(deps.get_current_active_superuser),  # noqa
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise CustomException(http_code=status.HTTP_400_BAD_REQUEST, message="The user with this username already exists in the system.")
    user = crud.user.create(db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return DataResponse().success_response(request, user)


@router.put("/user/me", response_model=schemas.User)
def update_user_me(
        *,
        db: Session = Depends(deps.get_db),
        password: str = Body(None),
        full_name: str = Body(None),
        email: EmailStr = Body(None),
        current_user: models.DbUser = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/user/me", response_model=schemas.User)
def read_user_me(
        db: Session = Depends(deps.get_db),  # noqa
        current_user: models.DbUser = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/user/open", response_model=schemas.User)
def create_user_open(
        *,
        db: Session = Depends(deps.get_db),
        password: str = Body(...),
        email: EmailStr = Body(...),
        full_name: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/user/{user_id}", response_model=schemas.User)
def read_user_by_id(
        user_id: int,
        current_user: models.DbUser = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/user/{user_id}", response_model=schemas.User)
def update_user(
        *,
        db: Session = Depends(deps.get_db),
        user_id: int,
        user_in: schemas.UserUpdate,
        current_user: models.DbUser = Depends(deps.get_current_active_superuser),  # noqa
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
