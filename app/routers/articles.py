from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.article import Article
from app.schemas.articles import ArticleResponse, ArticleCreate, ArticleUpdate
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/articles",
    tags=["Articles"]
)

@router.get("/", response_model=list[ArticleResponse])
def get_articles(db: Session = Depends(get_db),author_id:int = None,skip:int = 0, limit:int = 10):
    
    query = db.query(Article).filter(Article.status == "published")
    if author_id:
        query = query.filter(Article.author_id == author_id)
    return query.offset(skip).limit(limit).all()

@router.get("/my_articles", response_model=list[ArticleResponse])
def get_my_articles(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Article).filter(Article.author_id == current_user.id).all()


@router.get("/{id}", response_model=ArticleResponse)
def get_article(id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id, Article.status == "published").first() 
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.post("/", response_model=ArticleResponse, status_code=201)
def create_article(article: ArticleCreate, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    new_article = Article(
        title = article.title,
        body = article.body,
        status = article.status, 
        author_id = current_user.id
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

@router.patch("/{id}", response_model=ArticleResponse)
def update_Article(id:int, article: ArticleUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_article = db.query(Article).filter(Article.id == id, Article.author_id == current_user.id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found or you don't have permission to edit it")
    for key, value in article.model_dump(exclude_unset=True).items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article

@router.delete("/{id}", status_code=204)
def delete_article(id:int , db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_article = db.query(Article).filter(Article.id == id, Article.author_id == current_user.id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found or you don't have permission to delete it")
    db.delete(db_article)
    db.commit()