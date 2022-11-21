from __future__ import annotations
from datetime import timedelta, datetime
from fastapi import status, HTTPException, UploadFile, Query
from globals import MAX_IMAGE_UPLOAD_SIZE
from pathlib import Path
from shutil import rmtree
from jose import jwt
from passlib.context import CryptContext
from globals import EnvVars, ALGORITHM
from pydantic_schemas.auth_schemas import LoginUser


def new_brownfield_image_upload(
    files: list[UploadFile], bf_images_dir_path: Path
) -> None:
    # check if all uploaded files are valid content_type and max of 8 files were uploaded
    valid_mime_types = all(
        [file.content_type in ("image/jpeg", "image/png") for file in files]
    )
    if not valid_mime_types:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    elif len(files) > 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    # start writing files to disk, in case some of the file exceeds max size throw exception and delete everything that was written
    try:
        bf_images_dir_path.mkdir(exist_ok=False)
    except FileExistsError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    for file in files:
        content = file.file.read(MAX_IMAGE_UPLOAD_SIZE)
        if len(file.file.read(1)) != 0:
            clear_images_dir(bf_images_dir_path)
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        with open(Path(bf_images_dir_path, file.filename), "wb") as f:
            f.write(content)


def clear_images_dir(dir_path: Path):
    rmtree(dir_path)


# auth
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(client_password: str, user: LoginUser | None) -> bool:
    if not user:
        return False
    if not verify_password(client_password, user.hashed_password):
        return False
    return True


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, EnvVars.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt(token: str):
    return jwt.decode(token, EnvVars.SECRET_KEY, algorithms=[ALGORITHM])


## PAGINATION
from typing import Generic, Sequence, TypeVar
from dataclasses import asdict
from fastapi import Query
from pydantic import BaseModel
from pydantic.types import conint
from fastapi_pagination import create_page, resolve_params
from fastapi_pagination.bases import AbstractParams, BasePage, RawParams, AbstractPage

T = TypeVar("T")


class LimitOffsetParams(BaseModel, AbstractParams):
    limit: int = Query(20, ge=1, le=40, description="Page size limit")
    offset: int = Query(0, ge=0, description="Page offset")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.limit,
            offset=self.offset,
        )


class LimitOffsetPage(BasePage[T], Generic[T]):
    limit: conint(ge=1)  # type: ignore
    offset: conint(ge=0)  # type: ignore

    __params_type__ = LimitOffsetParams

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        params: AbstractParams,
    ) -> LimitOffsetPage[T]:
        return cls(
            total=total,
            items=items,
            **asdict(params.to_raw_params()),
        )


def paginate(
    items: Sequence[T],
    total: int,
    params: AbstractParams,
) -> AbstractPage[T]:
    params = resolve_params(params)

    return create_page(
        items=items,
        total=total,
        params=params,
    )
