from pydantic_schemas.auth_schemas import NewUser, UserInDB, LoginUser
from sqlalchemy.orm import Session
from sqlalchemy import select, update, text
from database.auth_models import User, Role
from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException
from globals import PERMISSIONS
from custom_exceptions import UserPermissionException


def create_new_user(new_user: NewUser, sess: Session) -> None:
    new_user_dict = new_user.dict()
    new_user_dict["hashed_password"] = new_user_dict.pop("password")
    clerk_role = sess.execute(select(Role).where(Role.name == "clerk")).scalar_one()
    user_to_create = User(**new_user_dict)
    user_to_create.roles.append(clerk_role)
    sess.add(user_to_create)
    sess.commit()
    return user_to_create.id  # type: ignore


def get_user_by_email(email: str, sess: Session) -> LoginUser | None:
    try:
        validate_email(email)
    except EmailNotValidError:
        raise HTTPException(status_code=400)
    stmt = (
        """
    select perms.name, users.hashed_password from auth.users as users
    join auth.user_roles as ur on users.id = ur.user_id
    join auth.roles as roles on roles.id = ur.role_id
    join auth.role_permissions as rp on roles.id = rp.role_id
    join auth.permissions as perms on rp.permission_id = perms.id
    where users.email = '%s';
    """
        % email
    )
    res = sess.execute(text(stmt)).all()
    if res == []:
        return None
    try:
        user_permissions = [t.name for t in res]  # type: ignore -- ignores type hinting for Row namedtuple
        user_permissions = PERMISSIONS.get_perms_numbers(user_permissions)
    except UserPermissionException:
        raise HTTPException(500)
    user_hashed_pass = res[0].hashed_password  # type: ignore -- ignores type hinting for Row namedtuple
    is_admin = res[0].is_admin  # type: ignore -- ignores type hinting for Row namedtuple
    return LoginUser(
        hashed_password=user_hashed_pass,
        permissions=user_permissions,
        is_admin=is_admin,
    )


def get_user_by_session(user_session: str, sess: Session) -> UserInDB | None:
    stmt = select(User).where(User.last_session == user_session)
    res = sess.execute(stmt).scalar_one_or_none()
    if res is None:
        return None
    return UserInDB.from_orm(res)


def assign_user_new_session(user_email: str, session_value: str, db_sess: Session):
    stmt = (
        update(User).where(User.email == user_email).values(last_session=session_value)
    )
    db_sess.execute(stmt)
    db_sess.commit()


def remove_user_session(user_email: str, db_sess: Session):
    stmt = update(User).where(User.email == user_email).values(last_session=None)
    db_sess.execute(stmt)
    db_sess.commit()
