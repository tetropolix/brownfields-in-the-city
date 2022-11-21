from crud.auth_cruds import get_user_by_session
from pydantic_schemas.auth_schemas import UserWithPermissions,User
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
from globals import PERMISSIONS

## COMMON

def get_session():
    sess = Session()
    try:
        yield sess
    finally:
        sess.close()

## BROWNFIELDS

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_auth_token_claims(token: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt(token)
        user_session: str = str(payload.get("sub"))
        permissions = payload.get("roles")
        if user_session is None or permissions is None:
            raise credentials_exception
        return TokenData(user_session=user_session,permissions=permissions)
    except JWTError:
        raise credentials_exception

async def get_current_active_user(token_data: TokenData = Depends(get_auth_token_claims),sess: SQLASession = Depends(get_session)) -> UserWithPermissions:
    user_in_db = get_user_by_session(token_data.user_session,sess)
    if user_in_db is None:
        raise HTTPException(status_code=400, detail="Invalid token")
    if user_in_db.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return UserWithPermissions(**user_in_db.dict(),permissions=token_data.permissions)

class Protected:
    def __init__ (self, permissions: list[PERMISSIONS]):
        self.permissions = permissions

    def __call__(self,active_user : UserWithPermissions = Depends(get_current_active_user)) -> User:
        for perm in self.permissions:
            if(perm.value not in active_user.permissions):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
        return User(**active_user.dict())

