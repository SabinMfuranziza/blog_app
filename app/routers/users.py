from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.schemas.user import UserResponse
from app.controller import user_controller

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: UserResponse = Depends(get_current_user)):
    return user_controller.get_user(current_user)




