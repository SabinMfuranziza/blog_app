from datetime import datetime
from pydantic import BaseModel


class ArticleResponse(BaseModel):
    id: int
    title: str
    body:str
    status:str
    author_id: int
    created_at: datetime


    class Config:
        from_attributes = True
        

class ArticleCreate(BaseModel):
    title:str
    body:str
    status:str = "draft"


class ArticleUpdate(BaseModel):
    title:str|None = None
    body:str|None = None
    status:str|None = None

