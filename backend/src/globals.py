from dotenv import load_dotenv
import os
from enum import Enum

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