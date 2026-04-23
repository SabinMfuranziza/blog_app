from fastapi import FastAPI
from app.database import engine, Base
from app.models import user, article
from app.routers import auth
from app.routers import users
from app.routers import articles


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog App")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(articles.router)

@app.get("/")
def root():
    return {"message": "Blog API is running"}