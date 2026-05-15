from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.article import Article  
from app.schemas.articles import ArticleResponse, ArticleCreate, ArticleUpdate
from app.schemas.user import UserResponse
from app.models.user import User
from app.schemas.admin import AdminUserUpdate




def get_users(db,skip:int=0,limit:int=10, admin_user = None):
    return db.query(User).offset(skip).limit(limit).all()

def get_user(id:int, db, admin_user):
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



def update_user(id:int, user: AdminUserUpdate, db, admin_user):
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(id:int, db, admin_user):
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if id == admin_user.id:
        raise HTTPException(status_code=400, detail="You can't delete yourself")
    db.delete(db_user)
    db.commit()