from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import auth
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.utils import hash_password, verify_password
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix = "/auth",
    tags = ["Authentication"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register_user(user : UserCreate, db: Session = Depends(get_db)):
    existing_useremail = db.query(User).filter(User.email == user.email).first()
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_useremail:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if existing_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    hashed_pwd = hash_password(user.password)
    new_user = User(
        username = user.username,
        email=user.email,
        hashed_password = hashed_pwd
    
    )

    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return new_user


@router.post("/login")
def Login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code = 403, detail="Invalid credentials")
    
    password_check = verify_password(form_data.password, user.hashed_password)
    if not password_check:
        raise HTTPException(status_code = 403, detail="Invalid credentials")
    
    token = auth.create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}