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
        