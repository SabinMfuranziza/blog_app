from pydantic import BaseModel, EmailStr
from datetime import datetime


class AdminCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "admin"

class AdminUserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    role: str | None = None