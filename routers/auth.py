from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import Users
from database import SessionLocal
from typing import Annotated
# This import is for being able to hash passwords in a database.
from passlib.context import CryptContext # type: ignore

router = APIRouter()

# Code for hashing a user password for security.
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class CreateUserRequest(BaseModel):
    """Request model for creating a new user."""
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependecy = Annotated[Session, Depends(get_db)]

@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependecy, create_user_request: CreateUserRequest):
    """Create a new user."""
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password), # This line makes sure the password being created is hashed. 
        is_active = True
    )
    
    db.add(create_user_model)
    db.commit()