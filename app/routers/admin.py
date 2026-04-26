from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.article import Article  
from app.schemas.articles import ArticleResponse, ArticleCreate, ArticleUpdate
from app.dependencies import get_current_user, get_admin_user
from app.schemas.user import UserResponse
from app.models.user import User
from app.schemas.admin import AdminUserUpdate


router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@router.get("/users", response_model=list[UserResponse])
def get_users(skip:int=0,limit:int=10,db: Session = Depends(get_db), admin_user = Depends(get_admin_user)):
    return db.query(User).offset(skip).limit(limit).all()


@router.get("/users/{id}", response_model=UserResponse)
def get_user(id:int, db:Session = Depends(get_db), admin_user = Depends(get_admin_user)):
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.patch("/users/{id}", response_model=UserResponse)
def update_user(id:int, user: AdminUserUpdate, db: Session = Depends(get_db), admin_user = Depends(get_admin_user)):
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/users/{id}", status_code=204)
def delete_user(id:int, db: Session = Depends(get_db), admin_user = Depends(get_admin_user)):
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if id == admin_user.id:
        raise HTTPException(status_code=400, detail="You can't delete yourself")
    db.delete(db_user)
    db.commit()



@router.get("/articles", response_model=list[ArticleResponse])
def get_all_articles(skip:int=0,limit:int=10,db: Session = Depends(get_db), admin_user = Depends(get_admin_user),author_id:int = None):
    query = db.query(Article)
    if author_id:
        query = query.filter(Article.author_id == author_id)
    return query.offset(skip).limit(limit).all()


@router.patch("/articles/{id}", response_model=ArticleResponse)
def update_article(id:int, article: ArticleUpdate, db: Session = Depends(get_db), admin_user = Depends(get_admin_user)):
    db_article = db.query(Article).filter(Article.id == id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    for key, value in article.model_dump(exclude_unset=True).items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article

@router.delete("/articles/{id}", status_code=204)
def delete_article(id:int, db: Session = Depends(get_db), admin_user = Depends(get_admin_user)):
    db_article = db.query(Article).filter(Article.id == id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(db_article)
    db.commit()

    
    
