from fastapi import APIRouter, Depends, status, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import Users
from database import SessionLocal
from typing import Annotated
from datetime import timedelta, datetime, timezone
# This import is for being able to hash passwords in a database.
from passlib.context import CryptContext # type: ignore
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'

# Code for hashing a user password for security.
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    """Request model for creating a new user."""
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="templates")

### Pages ###

@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

### Endpoints ###
def authenticate_user(username: str, password:str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

# Function for creating a token.
def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role : str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail='Could not validate user')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

# Create a new user endpoint.
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest, db: db_dependency):
    """Create a new user."""
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password), # This line makes sure the password being created is hashed. 
        is_active = True,
        phone_number = create_user_request.phone_number
    )
    
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
   
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    """Login a user and return an access token."""
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Could not validate user')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}
