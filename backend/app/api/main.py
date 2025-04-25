from fastapi import APIRouter
from app.api.routers import private
from app.api.routers import users

api_router = APIRouter()

api_router.include_router(private.router)
api_router.include_router(users.router)
