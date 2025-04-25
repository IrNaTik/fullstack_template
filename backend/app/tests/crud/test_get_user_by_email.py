from sqlalchemy.orm import Session
from app import crud
from app.core.schemas import UserRegister

def test_get_user_by_email(db: Session):
    # Create test user
    email = "test_get_user_by_email@example.com"
    user = crud.create_user(
        session=db,
        user_register=UserRegister(
            email=email,
            password="password123",
            full_name="Get User"
        ),
        auto_commit=False
    )
    
    # Test getting user
    found_user = crud.get_user_by_email(db, email)
    assert found_user is not None
    assert found_user.email == email
    assert found_user.id == user.id

def test_get_user_by_email_not_found(db: Session):
    # Test getting non-existent user
    found_user = crud.get_user_by_email(db, "test_get_user_by_email_not_found@example.com")
    assert found_user is None