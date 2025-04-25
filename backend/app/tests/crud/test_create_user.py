import pytest
from sqlalchemy.orm import Session
from app.models import User
from app import crud
from app.core.security import get_password_hash
from app.core.schemas import UserRegister


def test_create_user(db: Session):
    # Test data
    email = "test_create_user@example.com"
    password = "testpassword123"
    full_name = "Test User"
    
    # Create user
    user = crud.create_user(
        session=db,
        user_register=UserRegister(
            email=email,
            password=password,
            full_name=full_name
        ),
        auto_commit=False
    )
    
    # Assertions
    assert user.email == email
    assert user.full_name == full_name
    assert user.hashed_password != password  # Password should be hashed
    #assert user.is_active is True
    #assert user.is_superuser is False

def test_create_user_duplicate_email(db: Session):
    # Create first user
    email = "test_create_user_duplicate_email@example.com"
    crud.create_user(
        session=db,
        user_register=UserRegister(
            email=email,
            password="password123",
            full_name="First User"
        ),
        auto_commit=False
    )
    
    # Try to create second user with same email
    #with pytest.raises(ValueError, match="Email already registered"):
    try:
        crud.create_user(
            session=db,
            user_register=UserRegister(
                email=email,
                password="password456",
                full_name="Second User"
            ),
            auto_commit=False
        )
        pytest.fail("Дублированные данные вошли в таблицу")
    except ValueError as e:
        assert str(e) == "Email already registered"


def test_create_user_without_fullname(db: Session):
    # Test creating user without full_name
    email = "test_create_user_without_fullname@example.com"
    user = crud.create_user(
        session=db,
        user_register=UserRegister(
            email=email,
            password="password123"
        ),
        auto_commit=False
    )
    
    # Assertions
    assert user.email == email
    assert user.full_name is None
    assert user.hashed_password != "password123" 

