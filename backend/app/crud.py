import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User
from app.core.security import get_password_hash
from app.core.schemas import UserRegister


def create_user(*, session: Session, user_register: UserRegister, auto_commit: bool = True) -> User:
    # Check if user already exists
    if get_user_by_email(session, user_register.email):
        raise ValueError("Email already registered")
    
    db_obj = User(
        email=user_register.email,
        full_name=user_register.full_name,
        hashed_password=get_password_hash(user_register.password)
    )
    session.add(db_obj)
    if auto_commit:
        session.commit()
    return db_obj

def get_user_by_email(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email==email)
    result = session.execute(statement=statement).scalar_one_or_none()
    return result

def get_user_by_id(session: Session, user_id: str) -> User | None:
    statement = select(User).where(User.id==user_id)
    result = session.execute(statement=statement).scalar_one_or_none()
    return result
