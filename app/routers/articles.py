from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.article import Article
from app.schemas.articles import ArticleResponse

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


@router.get("/{id}", response_model=ArticleResponse)
def get_article(id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id, Article.status == "published").first() 
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


