from fastapi import APIRouter, HTTPException
from typing import Any

from app.core.schemas import UserRegister
from app.deps import SessionDep
from app import crud

router = APIRouter(prefix="/users")

@router.post("/signup")
def user_register(session: SessionDep, user_in: UserRegister) -> Any:
    try:
        user = crud.create_user(session=session, user_register=user_in)
        return {"message": "User created successfully", "user_id": user.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
