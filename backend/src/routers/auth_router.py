from datetime import timedelta
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import get_current_active_user
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from dependencies import get_session, Protected
from pydantic_schemas.auth_schemas import NewUser, User, Token
from crud.auth_cruds import (
    assign_user_new_session,
    create_new_user,
    get_user_by_email,
    remove_user_session,
)
from .routers_utils import create_access_token, get_password_hash, authenticate_user
from globals import ACCESS_TOKEN_EXPIRE_MINUTES, PERMISSIONS
from secrets import token_urlsafe

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    sess: Session = Depends(get_session),
):
    """Route which grants access token to the client(browser) - used as login mechanism"""
    user_in_db = get_user_by_email(form_data.username, sess)
    if not authenticate_user(form_data.password, user_in_db) or user_in_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user_in_db.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not active",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    generated_user_session = token_urlsafe(32)
    access_token = create_access_token(
        data={
            "sub": generated_user_session,
            "roles": user_in_db.permissions,
            "admin": user_in_db.is_admin,
            "active": user_in_db.is_active,
        },
        expires_delta=access_token_expires,
    )
    assign_user_new_session(form_data.username, generated_user_session, sess)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/logout")
async def logout(
    current_user: User = Depends(get_current_active_user),
    sess: Session = Depends(get_session),
):
    """Logs out user - removes last session assigned to user which is determined by jwt sent"""
    remove_user_session(current_user.email, sess)
    return {}


@router.post("/register")
def register_user(new_user: NewUser, sess: Session = Depends(get_session)):
    """New user registration"""
    new_user.password = get_password_hash(new_user.password)
    try:
        id = create_new_user(new_user, sess)
    except IntegrityError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    if id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create new user",
        )
    return {}


@router.get("/users/me")
async def read_users_me(
    current_user: Protected = Depends(Protected([PERMISSIONS.BF_READ])),
):
    """Testing purpose"""
    return current_user
