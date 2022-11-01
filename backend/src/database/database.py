from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

if(SQLALCHEMY_DATABASE_URL is None):
    raise RuntimeError('Connection to database has failed due to missing connection URL')


engine = create_engine(SQLALCHEMY_DATABASE_URL,echo=True)
Session = sessionmaker(bind = engine)
Base = declarative_base()