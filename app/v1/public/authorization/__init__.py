from fastapi import (
    APIRouter,
)
from app.v1.public.authorization.signup import signup

auth = APIRouter(prefix="/authorization")

auth.include_router(signup)