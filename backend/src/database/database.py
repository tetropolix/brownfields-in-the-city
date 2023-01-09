from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from globals import EnvVars

engine = create_engine(EnvVars.SQLALCHEMY_DATABASE_URL,echo=True)
Session = sessionmaker(bind = engine)
