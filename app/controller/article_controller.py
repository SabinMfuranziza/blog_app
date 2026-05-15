from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.article import Article
from app.schemas.articles import ArticleResponse, ArticleCreate, ArticleUpdate





def get_articles(db,author_id:int = None,skip:int = 0, limit:int = 10):
    
    query = db.query(Article).filter(Article.status == "published")
    if author_id:
        query = query.filter(Article.author_id == author_id)
    return query.offset(skip).limit(limit).all()



def get_my_articles(db, current_user):
    return db.query(Article).filter(Article.author_id == current_user.id).all()




def admin_get_all_articles(db,skip:int=0,limit:int=10, admin_user=None,author_id:int = None):
    query = db.query(Article)
    if author_id:
        query = query.filter(Article.author_id == author_id)
    return query.offset(skip).limit(limit).all()



def admin_update_article(id:int, article: ArticleUpdate, db, admin_user):
    db_article = db.query(Article).filter(Article.id == id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    for key, value in article.model_dump(exclude_unset=True).items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article

def admin_delete_article(id:int, db, admin_user):
    db_article = db.query(Article).filter(Article.id == id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(db_article)
    db.commit()





def get_article(id: int, db):
    article = db.query(Article).filter(Article.id == id, Article.status == "published").first() 
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


def create_article(article: ArticleCreate, db, current_user):
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



def update_Article(id:int, article: ArticleUpdate, db, current_user):
    db_article = db.query(Article).filter(Article.id == id, Article.author_id == current_user.id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found or you don't have permission to edit it")
    for key, value in article.model_dump(exclude_unset=True).items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article



def delete_article(id:int , db, current_user ):
    db_article = db.query(Article).filter(Article.id == id, Article.author_id == current_user.id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found or you don't have permission to delete it")
    db.delete(db_article)
    db.commit()