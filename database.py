# This is going to be the database for the TodoApp
# To use the SQLite3 database in terminal use - sqlite3 todos.db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
# Get variables from envirmoment
<<<<<<< HEAD
# Code to hide your personal details for database connection. 
=======
>>>>>>> 1fdf800 (Added a .env file and template for database info)
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')


#Code for making the database connect to aiven (Working on)
# Path to the downloaded CA certificate from Aiven
SSL_CERT_PATH = '/absolute/path/to/ca.pem'
SQLALCHEMY_DATABASE_URL = f'postgresql://{username}:{password}@{host}:{port}/{db_name}?sslmode=require'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"sslmode": "require", "sslrootcert": SSL_CERT_PATH})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

