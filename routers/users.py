from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path
from models import Todos, Users 
from database import SessionLocal
from .auth import get_current_user 
from passlib.context import CryptContext

router = APIRouter(
    prefix='/user',
    tags=['user'],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependecy = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
# Code for hashing a user password for security.
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Class to dealing with a password change.
class UserVerication(BaseModel):
    password: str
    new_password: str = Field(min_length=6)  

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependecy):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Athentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()

# This is an endpoint for changing password of the user that is currently logged in.
@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependecy, user_verification: UserVerication):
    if user is None:
        raise HTTPException(status_code=401, detail= 'Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()