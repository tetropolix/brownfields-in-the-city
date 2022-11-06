from crud.auth_cruds import get_user_by_email
from pydantic_schemas.auth_schemas import User
from database.database import Session
from sqlalchemy.orm import Session as SQLASession
from fastapi import HTTPException,Form,status, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
from pydantic_schemas.brownfield_schemas import NewBrownfield
from pydantic_schemas.auth_schemas import TokenData
from pydantic import ValidationError
from routers.routers_utils import decode_jwt
from jose import JWTError

def get_session():
    sess = Session()
    try:
        yield sess
    finally:
        sess.close()

def validate_raw_json_new_brownfield(data : str = Form(...)) -> NewBrownfield:
    try:
        new_brownfield = NewBrownfield.parse_raw(data)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return new_brownfield

### AUTH

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme),sess: SQLASession = Depends(get_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt(token)
        email: str = str(payload.get("sub"))
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user_in_db = get_user_by_email(token_data.email,sess)
    if user_in_db is None:
        raise credentials_exception
    return User(**user_in_db.dict())



async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

