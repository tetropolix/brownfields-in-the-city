from pydantic_schemas.auth_schemas import NewUser, UserInDB
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.auth_models import User

def create_new_user(new_user: NewUser,sess: Session) ->  None:
    new_user_dict = new_user.dict()
    new_user_dict['hashed_password'] = new_user_dict.pop('password')
    user_to_create = User(**new_user_dict)
    sess.add(user_to_create)
    sess.commit()
    return user_to_create.id  # type: ignore

def get_user_by_email(email:str,sess: Session) -> UserInDB | None:
    stmt = select(User).where(User.email == email)
    res = sess.execute(stmt).scalar_one_or_none()
    if res is None:
        return None
    return UserInDB.from_orm(res)


