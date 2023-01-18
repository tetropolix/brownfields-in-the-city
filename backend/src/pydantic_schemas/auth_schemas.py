from pydantic import BaseModel
from globals import PERMISSIONS

# Used when creating/registering new user
class NewUser(BaseModel):
    email: str
    phone: str
    password: str


# Base class for working with already logged in user
class User(BaseModel):
    id: int
    email: str
    phone: str
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True


class UpdatedUser(BaseModel):
    '''Used as User schema model which is used for user update by system admin (e.g. password reset)'''
    id: int
    email: str | None
    phone: str | None
    password: str | None
    is_active: bool | None


# Used for veryfing session value in DB
class UserInDB(User):
    last_session: str | None = None


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
