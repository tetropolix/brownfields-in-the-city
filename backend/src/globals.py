from dotenv import load_dotenv
import os
from enum import Enum
from custom_exceptions import UserPermissionException

load_dotenv()



SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
BROWNFIELD_IMAGES_DIR = os.getenv("BROWNFIELD_IMAGES_DIR")
SECRET_KEY = os.getenv("SECRET_KEY")
MAX_IMAGE_UPLOAD_SIZE = 2097152 # in bytes = 2MB
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

env_vars = [SQLALCHEMY_DATABASE_URL,BROWNFIELD_IMAGES_DIR,SECRET_KEY]

for var in env_vars:
    if var is None:
        raise RuntimeError(f'Unable to load {var} environment variable')

class EnvVars:
    SQLALCHEMY_DATABASE_URL: str = SQLALCHEMY_DATABASE_URL
    BROWNFIELD_IMAGES_DIR: str  = BROWNFIELD_IMAGES_DIR
    SECRET_KEY: str  = SECRET_KEY

class PERMISSIONS(Enum):
    BF_CREATE = 1
    BF_READ = 2
    BF_UPDATE = 3
    BF_DELETE = 4
    USER_CREATE = 5
    USER_READ = 6
    USER_UPDATE = 7
    USER_DELETE = 8

    @classmethod
    def get_perms_numbers(cls,perms:list[str]):
        perms_numbers: list[int] = []
        for perm in perms:
            match perm:
                case"brownfields:create":
                    perms_numbers.append(cls.BF_CREATE.value)
                case "brownfields:read":
                    perms_numbers.append(cls.BF_READ.value)
                case "brownfields:update":
                    perms_numbers.append(cls.BF_UPDATE.value)
                case "brownfields:delete":
                    perms_numbers.append(cls.BF_DELETE.value)
                case "users:read":
                    perms_numbers.append(cls.USER_READ.value)
                case "users:create":
                    perms_numbers.append(cls.USER_CREATE.value)
                case "users:update":
                    perms_numbers.append(cls.USER_UPDATE.value)
                case "users:delete":
                    perms_numbers.append(cls.USER_DELETE.value)
                case _:
                    raise UserPermissionException()
        return perms_numbers
