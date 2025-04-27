from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from typing import List

class PrivateUserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    is_verified: bool = False 

class UserRegister(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)

class UserLogin(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)

class NewPassword(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)

class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(max_length=255)

class EmailData(BaseModel):
    recipients: List[EmailStr]
    subject: str
    body: str



