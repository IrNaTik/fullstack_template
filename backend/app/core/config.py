import secrets
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# Its make possible to use settings not only from fastapi? but in alembic script too
BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", "..", ".."))
print(BASE_DIR)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_ignore_empty=True,
        extra="ignore",
    )
    
    API_V1_STR: str = "/api/v1"
    BACKEND_HOST: str 
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 
    FRONTEND_HOST: str = "http://localhost:5173"

    PROJECT_NAME: str = "FastAPI Template"
    #SENTRY_DSN: HttpUrl | None = None
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    # Emails

    # Mailtrap
    MAIL_USERNAME: str = "ba0aoz2zv0bmm"
    MAIL_PASSWORD: str = "bad9uqtook20q"
    MAIL_FROM: str = "noreply@ignitrudi.com"
    MAIL_PORT: int = 2525
    MAIL_SERVER: str = "ba0aoz2zv0bmm.mailtrap.ru"
    MAIL_FROM_NAME: str = "Password Reset"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = False

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        user = self.POSTGRES_USER
        password = self.POSTGRES_PASSWORD
        server = self.POSTGRES_SERVER
        port = self.POSTGRES_PORT
        db = self.POSTGRES_DB

        if password:
            return f"postgresql+psycopg2://{user}:{password}@{server}:{port}/{db}"
        else:
            return f"postgresql+psycopg2://{user}@{server}:{port}/{db}"

        

settings = Settings()
