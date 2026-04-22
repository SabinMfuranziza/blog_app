from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.schemas.user import UserResponse

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.get("/me", response_model=UserResponse)
def get_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user



