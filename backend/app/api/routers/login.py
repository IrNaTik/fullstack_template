from app.core.schemas import UserLogin
from app.deps import SessionDep
from app import crud
from app.core.security import verify_password, create_access_token, create_refresh_token
from fastapi import HTTPException, Response, Form
from typing import Any
from fastapi import APIRouter
from app.deps import CurrentUser
from app.utils import generate_password_reset_token
from app.utils import generate_reset_password_email
from app.utils import send_email
from app.core.security import get_password_hash
from app.core.schemas import NewPassword
from app.core.schemas import PasswordResetRequest
from app.core.security import verify_password_reset_token
from fastapi.responses import HTMLResponse, RedirectResponse
from app.core.config import settings

router = APIRouter(prefix="/login")

@router.post("/")
def user_login(session: SessionDep, user_in: UserLogin) -> Any:
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    if not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "message": "User logged in successfully"
    }

@router.post("/test-token")
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user
    
@router.post("/password-reset")
async def password_reset(session: SessionDep, reset_request: PasswordResetRequest) -> Any:
    """
    Request password reset
    """
    
    user = crud.get_user_by_email(session=session, email=reset_request.email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Generate reset token
    reset_token = generate_password_reset_token(str(user.id))
    
    # Generate and send email
    # email_data = generate_reset_password_email(
    #     email_to=user.email,
    #     email=user.email,
    #     token=reset_token
    # )
    await send_email(
        email=user.email,
        token=reset_token
    )
    
    return {"message": "Password reset email sent successfully"}

# @router.get("/reset-password", response_class=HTMLResponse)
# async def reset_form(token: str):
#     return RedirectResponse(url=f"/login/reset-password/?token={token}")

@router.get("/reset-password", response_class=HTMLResponse)
async def reset_form(token: str):
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Сброс пароля</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f5f5f5;
            }}
            .form-container {{
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                width: 100%;
                max-width: 400px;
            }}
            .form-group {{
                margin-bottom: 20px;
            }}
            label {{
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }}
            input[type="password"] {{
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }}
            button {{
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                width: 100%;
                font-size: 16px;
            }}
            button:hover {{
                background-color: #45a049;
            }}
            .error {{
                color: red;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="form-container">
            <h2>Сброс пароля</h2>
            <form action="/login/reset-password" method="post">
                <input type="hidden" name="token" value="{token}">
                <div class="form-group">
                    <label for="new_password">Новый пароль:</label>
                    <input type="password" id="new_password" name="new_password" required>
                </div>
                <button type="submit">Сохранить новый пароль</button>
            </form>
        </div>
    </body>
    </html>
    """

@router.post("/reset-password")
async def reset_password(session: SessionDep, body: NewPassword) -> Any:
    """
    Reset password
    """
    user_id = verify_password_reset_token(token=body.token)
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    user = crud.get_user_by_id(session=session, user_id=int(user_id))
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    
    # Update user's password
    user.hashed_password = get_password_hash(body.new_password)
    session.commit()
    
    return {"message": "Password updated successfully"}
