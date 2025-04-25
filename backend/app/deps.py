from collections.abc import Generator
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.db import engine
from app.core.config import settings
from app import crud
from app.models import User
import jwt
from pydantic import ValidationError
from fastapi import HTTPException
from fastapi import status
from datetime import datetime, timezone 
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(
    session: SessionDep,
    token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        now_timestamp = datetime.now(timezone.utc).timestamp()
        if payload["exp"] < now_timestamp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user = crud.get_user_by_id(session, int(t.sub))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]