from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import settings
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.schemas import EmailData
from pathlib import Path
from jinja2 import Template
from typing import Any



def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent / "emails_templates" / "build" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content

def generate_password_reset_token(subject: str) -> str:
    subject = str(subject)
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.now(timezone.utc)
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": subject},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt

def generate_reset_password_email(email_to: str, email: str, token: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    link = f"{settings.BACKEND_HOST}{settings.API_V1_STR}/login/reset-password?token={token}"
    html_content = render_email_template(
        template_name="reset_password.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
    return EmailData(body=html_content, subject=subject, recipients=[email])

async def send_email(email: str, token: str):
    email_data = generate_reset_password_email(email, email, token)
    message = MessageSchema(
        subject=email_data.subject,
        recipients=email_data.recipients,
        body=email_data.body,
        subtype="html",
        charset="utf-8"
    )
    conf = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_FROM_NAME="Password reset",
        MAIL_STARTTLS=settings.MAIL_STARTTLS,
        MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
        USE_CREDENTIALS=settings.USE_CREDENTIALS,
        VALIDATE_CERTS=settings.VALIDATE_CERTS,
        TEMPLATE_FOLDER=Path(__file__).parent / "emails_templates" / "build" 
    )
    fm = FastMail(conf)
    await fm.send_message(message)