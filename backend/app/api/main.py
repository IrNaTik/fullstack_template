from fastapi import APIRouter
from app.api.routers import private
from app.api.routers import users
from app.api.routers import login

api_router = APIRouter()

api_router.include_router(private.router)
api_router.include_router(users.router)
api_router.include_router(login.router)
