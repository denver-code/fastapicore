from fastapi import (
    APIRouter,
)
from app.v1.public.authorization import auth

public = APIRouter(prefix="/public")

public.include_router(auth)