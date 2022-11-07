from pydantic import BaseModel

class NewUser(BaseModel):
    email: str
    phone: str
    password: str

class User(BaseModel):
    email : str
    phone : str
    is_active : bool
    is_admin: bool

class UserInDB(User):
    last_session : str | None = None
    hashed_password: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_session: str 
    