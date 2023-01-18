from pydantic_schemas.auth_schemas import (
    NewUser,
    UpdatedUser,
    UserInDB,
    LoginUser,
    User as UserSchema,
)
from sqlalchemy.orm import Session
from sqlalchemy import select, update, text
from database.auth_models import User, Role
from email_validator import validate_email
from globals import PERMISSIONS
from routers.routers_utils import get_password_hash


def create_new_user(new_user: NewUser, sess: Session) -> None:
    new_user_dict = new_user.dict()
    new_user_dict["hashed_password"] = get_password_hash(new_user.password)
    new_user_dict.pop("password")
    clerk_role = sess.execute(select(Role).where(Role.name == "clerk")).scalar_one()
    user_to_create = User(**new_user_dict)
    user_to_create.roles.append(clerk_role)
    sess.add(user_to_create)
    sess.commit()
    return user_to_create.id  # type: ignore


def get_user_by_email(email: str, sess: Session) -> LoginUser | None:
    validate_email(email)
    stmt = (
        """
    select perms.name, users.hashed_password, users.is_admin , users.is_active from auth.users as users
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
    user_permissions = [t.name for t in res]  # type: ignore
    # Throws UserPermissionException when permission not found for some reason
    user_permissions = PERMISSIONS.get_perms_numbers(user_permissions)

    user_hashed_pass = res[0].hashed_password  # type: ignore
    is_admin = res[0].is_admin  # type: ignore
    is_active = res[0].is_active  # type: ignore
    return LoginUser(
        hashed_password=user_hashed_pass,
        permissions=user_permissions,
        is_admin=is_admin,
        is_active=is_active,
    )


def get_user_by_session(user_session: str, sess: Session) -> UserInDB | None:
    stmt = select(User).where(User.last_session == user_session)
    res = sess.execute(stmt).scalar_one_or_none()
    if res is None:
        return None
    return UserInDB.from_orm(res)


def get_all_users(sess: Session) -> list[UserSchema]:
    users = []
    res = sess.query(User).all()
    for user in res:
        users.append(UserSchema.from_orm(user))
    return users


def update_user(updated_user: UpdatedUser, sess: Session) -> None:
    user = sess.execute(select(User).where(User.id == updated_user.id)).scalar_one()
    if updated_user.email is not None:
        validate_email(updated_user.email)  # raises exception if not valid
        user.email = updated_user.email
    if updated_user.is_active is not None:
        user.is_active = updated_user.is_active
    if updated_user.phone is not None:
        user.phone = updated_user.phone
    if updated_user.password is not None:
        user.hashed_password = get_password_hash(updated_user.password)
    sess.add(user)
    sess.commit()


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
