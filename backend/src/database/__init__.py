from sqlalchemy.ext.declarative import declarative_base

## used as Base for ORM classes as well as Base for alebmic migration
## Could be stored in database.py as well, but other dependencies in database.py then have to be resolved when used as part of alembic migration script
Base = declarative_base()