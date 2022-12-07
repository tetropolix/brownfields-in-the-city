from sqlalchemy import ForeignKey,Integer,Column,String,Float,Numeric,Boolean,Table
from sqlalchemy.orm import relationship
from .database import Base


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("auth.users.id"), primary_key=True),
    Column("role_id", ForeignKey("auth.roles.id"), primary_key=True),
    schema='auth'
)

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema":"auth"}
    id = Column(Integer,primary_key=True,index=True)
    last_session = Column(String(64),nullable=True,default=None,index=True,unique=True)
    email = Column(String(256),index=True,nullable=False,unique=True)
    phone = Column(String(32),nullable=False)
    hashed_password = Column(String(256),nullable=False)
    is_admin = Column(Boolean,nullable=False,default=False)
    is_active = Column(Boolean,nullable=False,default = False)
    roles = relationship("Role",secondary=user_roles)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("permission_id", ForeignKey("auth.permissions.id"), primary_key=True),
    Column("role_id", ForeignKey("auth.roles.id"), primary_key=True),
    schema='auth'
)

class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = {"schema":"auth"}
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(64),unique=True,nullable=False)

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema":"auth"}
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(64),unique=True,nullable=False)



