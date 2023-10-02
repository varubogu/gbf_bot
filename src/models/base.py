from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

import os

DBUSER = os.environ['DBUSER']
DBPASSWORD = os.environ['DBPASSWORD']
DBHOST = os.environ['DBHOST']
DBDATABASE = os.environ['DBDATABASE']

DATABASE_URL = f'postgresql://{DBUSER}:{DBPASSWORD}@{DBHOST}/{DBDATABASE}'
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False
    )
)

Base = declarative_base()
