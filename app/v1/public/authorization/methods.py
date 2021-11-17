from fastapi import (
    HTTPException,
    Header
)

import jwt
import os
import hashlib


async def login_required(Authorization=Header("Authorization")):
    try:
        session = Authorization
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")

async def get_password_hash(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
