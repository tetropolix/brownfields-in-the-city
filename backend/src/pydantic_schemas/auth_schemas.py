from pydantic import BaseModel
from globals import PERMISSIONS

# Used when creating/registering new user
class NewUser(BaseModel):
    email: str
    phone: str
    password: str


# Base class for working with already logged in user
class User(BaseModel):
    email: str
    phone: str
    is_active: bool


# Used for veryfing session value in DB
class UserInDB(User):
    last_session: str | None = None

    class Config:
        orm_mode = True


# Used in PROTECTED depenedency - gets permissions for jwt and validate them against the route
class UserWithPermissions(User):
    permissions: list[int]


# Used when attempting to log in and for initial JWT creation
class LoginUser(BaseModel):
    is_admin: bool
    is_active: bool
    hashed_password: str
    permissions: list[int]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_session: str
    permissions: list[int]
    admin: bool
