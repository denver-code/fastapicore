from fastapi import (
    APIRouter,
)
import app.v1.public as public
import app.v1.private as private

api = APIRouter(prefix="/v1")

api.include_router(public.public)
api.include_router(private.private)