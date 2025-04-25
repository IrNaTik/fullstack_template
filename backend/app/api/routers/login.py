from app.core.schemas import UserLogin
from app.deps import SessionDep
from app import crud
from app.core.security import verify_password, create_access_token, create_refresh_token
from fastapi import HTTPException
from typing import Any
from fastapi import APIRouter

router = APIRouter(prefix="/login")

@router.post("/")
def user_login(session: SessionDep, user_in: UserLogin) -> Any:
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    if not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "message": "User logged in successfully"
    }
