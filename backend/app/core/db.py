from sqlalchemy import create_engine
from app.core.config import settings

from app.models import Base

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

# Base.metadata.create_all(engine)