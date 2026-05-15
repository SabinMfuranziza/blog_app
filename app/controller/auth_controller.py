
from app.auth import create_access_token
from fastapi import HTTPException
from app.utils import hash_password, verify_password
from app.models.user import User


def register_user(user, db):
    existing_useremail = db.query(User).filter(User.email == user.email).first()
    existing_username = db.query(User).filter(User.username == user.username).first()
    hashed_pwd = hash_password(user.password) 
    if existing_useremail:
        raise HTTPException(status_code=400, detail="Email already registered")
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")   
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login_user(user, db):
    db_user = db.query(User).filter(User.email == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    return db_user


def create_token(user):
    token = create_access_token({"sub": str(user.id), "role":user.role})
    return {"access_token": token, "token_type": "bearer"}