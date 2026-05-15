from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import auth
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.utils import hash_password, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from app.controller import auth_controller
router = APIRouter(
    prefix = "/auth",
    tags = ["Authentication"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register_user(user : UserCreate, db: Session = Depends(get_db)):
    new_user = auth_controller.register_user(user, db)
    return new_user



@router.post("/login")
def Login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_controller.login_user(form_data, db)
    return auth_controller.create_token(user)