from fastapi import APIRouter, Depends, HTTPException
from app.models.article import Article  
from app.schemas.articles import ArticleResponse, ArticleCreate, ArticleUpdate
from app.dependencies import get_current_user, get_admin_user
from app.schemas.user import UserResponse
from app.models.user import User
from app.schemas.admin import AdminUserUpdate
from app.controller import admin_controller  
from sqlalchemy.orm import Session
from app.database import get_db


router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@router.get("/users", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 10, admin_user = Depends(get_admin_user)):
    return admin_controller.get_users(db, skip, limit, admin_user)


@router.get("/users/{id}", response_model=UserResponse)
def read_user(id: int, db: Session = Depends(get_db), admin_user = Depends(get_admin_user)):
    return admin_controller.get_user(id, db, admin_user)

@router.patch("/users/{id}", response_model=UserResponse)
def update_user(id: int, user: AdminUserUpdate, db: Session = Depends(get_db), admin_user = Depends(get_admin_user)):
    return admin_controller.update_user(id, user, db, admin_user)


@router.delete("/users/{id}", status_code=204)
def delete_user(id: int, db: Session = Depends(get_db), admin_user = Depends(get_admin_user)):
    return admin_controller.delete_user(id, db, admin_user)


    
