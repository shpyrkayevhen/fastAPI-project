from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<IP-address/hostname>/<database_name'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:yevhen199610@localhost/fastapi'

# Connect to db
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# If we want to talk with database we must to create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All our models we will be inheritance from this class
Base = declarative_base()

# DEPENDENCY


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
