from typing import Optional
from typing import List

from pydantic import EmailStr
from pydantic import Field

from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    #name: Mapped[str] = mapped_column(String(30))
    #fullname: Mapped[Optional[str]] 
    #addresses: Mapped[list["Address"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    #password: str = Field(min_length=8, max_length=40)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    items: Mapped[list["Items"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Items(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="items")

    

