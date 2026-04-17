from fastapi import FastAPI
from app.database import engine, Base
from app.models import user, article
from app.routers import auth

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Blog App")

@app.get("/")
def root():
    return {"message": "Blog API is running"}