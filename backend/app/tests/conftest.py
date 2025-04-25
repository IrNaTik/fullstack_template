import os
import sys
import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
import sys
import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.main import app
from app.models import Base
from app.deps import get_db
from app.core.config import settings

# Programmer should change it dynamycly if its necessary
collect_ignore = ["crud"]

# Test database URL
SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

# Create test engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        with session.begin_nested():
            yield session
            session.rollback()


