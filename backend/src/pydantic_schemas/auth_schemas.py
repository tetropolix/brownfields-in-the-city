from pydantic import BaseModel

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

class LoginUser(User):
    hashed_password: str
    permissions: list[int] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_session: str 
    