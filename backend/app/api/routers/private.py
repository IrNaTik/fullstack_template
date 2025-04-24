from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["private"], prefix="/private")

class PrivateUserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    is_verified: bool = False 

@router.post("/users")
def create_user(user_in: PrivateUserCreate) -> Any:
    """
    Create a new user
    """
    

    return user_in