from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.exception_handler import CustomException
from app.core.security import get_password_hash
from app.schemas.base import DataResponse
from app.utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
    send_new_account_email
)

router = APIRouter()


@router.post("/register", response_model=DataResponse[schemas.User])
def register_user(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        user_in: schemas.UserCreate
) -> Any:
    """
    Register new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise CustomException(http_code=status.HTTP_400_BAD_REQUEST,
                              message="The user with this username already exists in the system.")
    user = crud.user.create(db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(email_to=user_in.email, username=user_in.email, password=user_in.password)
    return DataResponse().success_response(request, user)


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise CustomException(http_code=status.HTTP_400_BAD_REQUEST, message="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise CustomException(http_code=status.HTTP_400_BAD_REQUEST, message="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(user.id, expires_delta=access_token_expires),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=DataResponse[schemas.User])
def test_token(request: Request, current_user: models.DbUser = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return DataResponse().success_response(request, current_user)


@router.post("/password-recovery/{email}", response_model=DataResponse[schemas.Success])
def recover_password(request: Request, email: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    user = crud.user.get_by_email(db, email=email)

    if not user:
        raise CustomException(
            http_code=status.HTTP_404_NOT_FOUND,
            message="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(email_to=user.email, email=email, token=password_reset_token)
    return DataResponse().success_response(request, {})


@router.post("/reset-password/", response_model=DataResponse[schemas.Success])
def reset_password(
        request: Request,
        token: str = Body(...),
        new_password: str = Body(...),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise CustomException(http_code=status.HTTP_400_BAD_REQUEST, message="Invalid token")
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise CustomException(
            http_code=status.HTTP_404_NOT_FOUND,
            message="The user with this username does not exist in the system.",
        )
    elif not crud.user.is_active(user):
        raise CustomException(http_code=status.HTTP_400_BAD_REQUEST, message="Inactive user")
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return DataResponse().success_response(request, {})
