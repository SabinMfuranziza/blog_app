from pydantic import BaseModel, EmailStr
from datetime import datetime

# What the user sends us
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# What we send back (Notice: NO password here!)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token:str
    token_type:str
