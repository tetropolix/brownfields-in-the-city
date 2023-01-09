import sys
from dotenv import load_dotenv
import os
from enum import Enum
from custom_exceptions import UserPermissionException

env_file_path = os.getenv("BROWNFIELDS_ENV_FILE")

## load .env file based on command line option --env_file, if ommited load env variables from actual envirnoment
if env_file_path is not None:
    load_dotenv(env_file_path)
else:
    load_dotenv()

MAX_IMAGE_UPLOAD_SIZE = 2097152  # in bytes = 2MB
ALGORITHM = "HS256"
IMAGES_DIR = "images"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

env_vars = dict(
    SQLALCHEMY_DATABASE_URL=os.getenv("SQLALCHEMY_DATABASE_URL"),
    BROWNFIELDS_STATIC_DIR=os.getenv("BROWNFIELDS_STATIC_DIR"),
    SECRET_KEY=os.getenv("SECRET_KEY"),
    BROWFIELDS_STATIC_PATH_IMAGES=os.getenv("BROWFIELDS_STATIC_PATH_IMAGES"),
    BROWNFIELDS_IMAGES_DIR=os.getenv("BROWNFIELDS_IMAGES_DIR"),
)

# Check if env variables were incialized
for key, val in env_vars.items():
    if val is None:
        raise RuntimeError(f"Unable to load value for environment variable {key}")


class EnvVars:
    SECRET_KEY: str = env_vars.get("SECRET_KEY")  # type: ignore
    SQLALCHEMY_DATABASE_URL: str = env_vars.get("SQLALCHEMY_DATABASE_URL")  # type: ignore
    #DIRECTORY USED AS MOUNTING POINT FOR STATIC FILES -> {STATIC_DIR}
    BROWNFIELDS_STATIC_DIR: str = env_vars.get("BROWNFIELDS_STATIC_DIR")  # type: ignore 
    #DIRECTORY INSIDE STATIC_DIR WHICH SHOULD BE USED FOR STORING IMAGES -> {STATIC_DIR/IMAGES_DIR}
    BROWNFIELDS_IMAGES_DIR: str = env_vars.get("BROWNFIELDS_IMAGES_DIR")  # type: ignore 
    #PART WHICH WILL BE ATTACHED AFTER /static URL PATH FOR OBTAINING, SPECIFIC DIRECTORY FOR STORING IMAGES -> {IMAGES_DIR}
    BROWFIELDS_STATIC_PATH_IMAGES: str = env_vars.get("BROWFIELDS_STATIC_PATH_IMAGES")  # type: ignore 


# Check if env paths are exisiting directories
for p in [
    EnvVars.BROWNFIELDS_STATIC_DIR,
    EnvVars.BROWNFIELDS_IMAGES_DIR,
]:
    if not (os.path.exists(p) and os.path.isdir(p)):
        raise RuntimeError(f"Necessary directory {p} is missing")

# No check for static paths which should be part of static dir - TODO


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
    def get_perms_numbers(cls, perms: list[str]):
        perms_numbers: list[int] = []
        for perm in perms:
            match perm:
                case "brownfields:create":
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
