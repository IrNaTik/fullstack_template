import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User

#from sqlmodel import Session, select

#from app.core.security import get_password_hash, verify_password
#from app.models import Item, ItemCreate, User, UserCreate, UserUpdate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def get_user_by_email(session: Session, email: str) -> User | None:
    statement = select(User).where(email=email)
    res = session.execute(statement=statement)
