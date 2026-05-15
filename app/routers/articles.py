from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.article import Article
from app.schemas.articles import ArticleResponse, ArticleCreate, ArticleUpdate
from app.dependencies import get_current_user, get_admin_user
from app.controller import article_controller

router = APIRouter(
    prefix="/articles",
    tags=["Articles"]
)

@router.get("/", response_model=list[ArticleResponse])
def get_articles_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), author_id: int = None):
    return article_controller.get_articles(db, author_id, skip, limit)


@router.get("/my_articles", response_model=list[ArticleResponse])
def get_my_articles_endpoint(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return article_controller.get_my_articles(db, current_user)


@router.get("/admin", response_model=list[ArticleResponse])
def admin_get_all_articles_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), admin_user = Depends(get_admin_user), author_id: int = None):
    return article_controller.admin_get_all_articles(skip, limit, db, admin_user, author_id)


@router.patch("/admin/{id}", response_model=ArticleResponse)
def admin_update_article_endpoint(id: int, article: ArticleUpdate, db: Session = Depends(get_db), admin_user = Depends(get_admin_user)):
    return article_controller.admin_update_article(id, article, db, admin_user)

@router.delete("/admin/{id}", status_code=204)
def admin_delete_article_endpoint(id: int, db: Session = Depends(get_db), admin_user = Depends(get_admin_user)):
    return article_controller.admin_delete_article(id, db, admin_user)
        

@router.get("/{id}", response_model=ArticleResponse)
def get_article_endpoint(id: int, db: Session = Depends(get_db)):
    return article_controller.get_article(id, db)


@router.post("/", response_model=ArticleResponse, status_code=201)
def create_article_endpoint(article: ArticleCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return article_controller.create_article(article, db, current_user)

@router.patch("/{id}", response_model=ArticleResponse)
def update_article_endpoint(id: int, article: ArticleUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return article_controller.update_Article(id, article, db, current_user)



@router.delete("/{id}", status_code=204)
def delete_article_endpoint(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return article_controller.delete_article(id, db, current_user)

