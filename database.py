# This is going to be the database for the TodoApp
# To use the SQLite3 database in terminal use - sqlite3 todos.db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# This line is used to connect to the postgresql / pgadmin database.
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:passpost@localhost/TodoApplicationDatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

