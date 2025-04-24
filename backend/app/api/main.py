from fastapi import APIRouter
from app.api.routers import private

api_router = APIRouter()

api_router.include_router(private.router)

