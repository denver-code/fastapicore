import aioredis

from fastapi import (
    FastAPI,
    Depends
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from typing import Optional

app = FastAPI(title="FastAPICore", debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    redis = await aioredis.create_redis_pool("redis://localhost")
    await FastAPILimiter.init(redis)

@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def home_event():
    return {"Hello":"world"}