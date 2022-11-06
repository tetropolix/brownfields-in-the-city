
from datetime import timedelta
from fastapi import Depends, HTTPException, status,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import get_current_active_user
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from dependencies import get_session
from pydantic_schemas.auth_schemas import NewUser, User,Token
from crud.auth_cruds import create_new_user,get_user_by_email
from .routers_utils import create_access_token, get_password_hash,authenticate_user
from globals import ACCESS_TOKEN_EXPIRE_MINUTES

router =  APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post("/token",response_model = Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),sess: Session = Depends(get_session)):
    user_in_db = get_user_by_email(form_data.username,sess)
    if not authenticate_user(form_data.password,user_in_db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_in_db.email}, expires_delta=access_token_expires # type:ignore -> user_in_db is not None (authenticate_user fn makes sure)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.post('/register')
def register_user(new_user: NewUser,sess: Session = Depends(get_session)):
    new_user.password = get_password_hash(new_user.password)
    try:
        id = create_new_user(new_user,sess)
    except IntegrityError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    if(id is None):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='Unable to create new user')
    return {}
    

