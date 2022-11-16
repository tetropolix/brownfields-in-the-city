from pydantic import BaseModel
from globals import PERMISSIONS

class NewUser(BaseModel):
    email: str
    phone: str
    password: str

class User(BaseModel):
    email : str
    phone : str
    is_active : bool
    
class UserInDB(User):
    last_session : str | None = None

    class Config:
        orm_mode = True

class UserWithPermissions(User):
    permissions: list[int]

class LoginUser(BaseModel):
    hashed_password: str
    permissions: list[int]

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_session: str 
    permissions: list[int]
    