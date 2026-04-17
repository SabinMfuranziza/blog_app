from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.utils import hash_password

router = APIRouter(
    prefix = "/auth",
    tags = ["Authentication"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register_user(user : UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashed_pwd = hash_password(user.password)
    new_user = User(
        username = user.username,
        email=user.email,
        hashed_password = hashed_pwd
    
    )

    db.add(new_user)
    db.commit
    db.refresh(new_user)

    return new_user