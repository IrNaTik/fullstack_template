from fastapi import APIRouter
from typing import Any

from app.core.schemas import UserRegister
from app.deps import SessionDep

from app import crud

router = APIRouter(prefix="/users")

@router.post("/signup")
def user_register(session: SessionDep, user_in: UserRegister) -> Any:
    user = crud.