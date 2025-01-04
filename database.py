# This is going to be the database for the TodoApp
# To use the SQLite3 database in terminal use - sqlite3 todos.db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# This line is used to connect to the postgresql / pgadmin database.
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:passpost@localhost/TodoApplicationDatabase'

# Path to the downloaded CA certificate from Aiven
SSL_CERT_PATH = '/path/to/ca.pem'

SQLALCHEMY_DATABASE_URL = 'postgresql://avnadmin:AVNS_TOEMvgcDE3O-Iu08Zqm@pg-3f4ef746-deployment-database.g.aivencloud.com:10732/defaultdb?sslmode=require'


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"sslmode": "require", "sslrootcert": SSL_CERT_PATH})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

