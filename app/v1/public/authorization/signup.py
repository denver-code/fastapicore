from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from fastapi_limiter.depends import RateLimiter
from pydantic import (
    BaseModel,
    validator
)
import re
from app.v1.api.database_user_api import (
    insert_user,
    user_exist
)

signup = APIRouter(prefix="/signup")


class User(BaseModel):
    email: str
    password: str
    wallets: list
    history: list

    @validator("email")
    def email_regex(cls, v):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if not re.fullmatch(regex, v):
            raise ValueError("Invalid email")
        return v

    @validator("password")
    def password_hash_checker(cls, v):
        regex = r"^[a-fA-F0-9]{64}$"
        if not re.fullmatch(regex, v):
            raise ValueError("Need hashed password")
        return v


@signup.post("/", dependencies=[Depends(RateLimiter(times=1, seconds=5))])
async def signup_event(user: User):
    user_dict = user.dict()
    if not await user_exist(user_dict["email"]):
        return await insert_user(user_dict)
    raise HTTPException(status_code=403, detail="User already exist")
