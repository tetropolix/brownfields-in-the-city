from sqlalchemy import ForeignKey,Integer,Column,String,Float,Numeric,Boolean
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema":"auth"}
    id = Column(Integer,primary_key=True,index=True)
    last_session = Column(String(64),nullable=True,default=None,index=True,unique=True)
    email = Column(String(256),index=True,nullable=False,unique=True)
    phone = Column(String(32),nullable=False)
    hashed_password = Column(String(256),nullable=False)
    is_active = Column(Boolean,nullable=False,default = False)
    is_admin = Column(Boolean,nullable=False,default = False)