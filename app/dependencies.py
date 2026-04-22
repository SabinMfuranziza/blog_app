from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.auth import verify_access_token
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    payload = verify_access_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    current_user = db.query(user.User).filter(user.User.id == user_id).first()
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return current_user

