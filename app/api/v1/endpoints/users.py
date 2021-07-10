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


@router.get("", response_model=DataResponse[List[schemas.User]])
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


@router.put("/me", response_model=DataResponse[schemas.User])
def update_user_me(
        *,
        request: Request,
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
    return DataResponse().success_response(request, user)


@router.get("/me", response_model=DataResponse[schemas.User])
def read_user_me(
        request: Request,
        db: Session = Depends(deps.get_db),  # noqa
        current_user: models.DbUser = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return DataResponse().success_response(request, current_user)


@router.post("/open", response_model=DataResponse[schemas.User])
def create_user_open(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        password: str = Body(...),
        email: EmailStr = Body(...),
        full_name: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise CustomException(
            http_code=403,
            message="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise CustomException(
            http_code=400,
            message="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
    user = crud.user.create(db, obj_in=user_in)
    return DataResponse().success_response(request, user)


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
        request: Request,
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
        raise CustomException(http_code=400, message="The user doesn't have enough privileges")
    return DataResponse().success_response(request, user)


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
        *,
        request: Request,
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
        raise CustomException(
            http_code=404,
            message="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return DataResponse().success_response(request, user)


@router.put("/profile/{user_id}", response_model=DataResponse[schemas.UserProfile])
def update_user_profile(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        user_id: str,
        user_profile_in: schemas.UserProfileUpdate,
        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    """
    Update a user profile
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise CustomException(
            http_code=404,
            message="The user with this username does not exist in the system",
        )
    print(user_id)
    user_profile = crud.user_profile.get_by_user_id(db, user_id=user_id)
    if user_profile:
        response = crud.user_profile.update(db, db_obj=user_profile, obj_in=user_profile_in)
    else:
        user_profile_in.user_id = user_id
        response = crud.user_profile.create(db, obj_in=user_profile_in)
    print(user_profile)
    return DataResponse().success_response(request, response)

