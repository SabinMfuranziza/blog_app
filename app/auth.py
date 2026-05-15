from fastapi import HTTPException
from jose import jwt
import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM="HS256"

def create_access_token(data: dict):
    data_copy = data.copy()
    encode = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
    return encode

def verify_access_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})     
