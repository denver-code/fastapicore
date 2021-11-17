# import motor.motor_asyncio
import requests
import os

# r = requests.get("http://ip.42.pl/raw")
# ip = r.text

# if ip != os.getenv('SERVER_IP', "0.0.0.0"):
#     client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('DATABASE_LOCAL', "mongodb://127.0.0.1:27017"))
# else:
#     client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('DATABASE', "0.0.0.0"))

# db = client["MetaExchange"]
# users = db["users"]
# user_deleted = db["usersDeleted"]

from app.v1.api.database_api import *


async def user_exist(email):
    return bool(await users.find_one({"email":email}))

async def insert_user(user_object):
    return bool(await users.insert_one({
        "email": user_object["email"],
        "password": user_object["password"],
        "wallets": [],
        "history": []
    }))

async def backup_user(user):
    if bool(await user_deleted.find_one({"email":user["email"]})):
        await user_deleted.insert_one(user)

async def get_user(email):
    return await users.find_one({"email":email})

async def update_user(email, new_data):
    return await globals()[db].update_one({"email":email}, {"$set": new_data}, upsert=True)

async def delete_user(email):
    await backup_user(await get_user(email))
    return bool(await users.delete_one({"email":email}))