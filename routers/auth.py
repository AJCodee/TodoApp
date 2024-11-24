from fastapi import APIRouter
from pydantic import BaseModel
from models import Users
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

@router.post("/auth/")
async def create_user(create_user_request: CreateUserRequest):
    """Create a new user."""
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True
    )
    
    return create_user_model