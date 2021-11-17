from motor.metaprogramming import asynchronize
import motor.motor_asyncio
import requests
import os

r = requests.get("http://ip.42.pl/raw")
ip = r.text

if ip != os.getenv('SERVER_IP', "0.0.0.0"):
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('DATABASE_LOCAL', "mongodb://127.0.0.1:27017"))
else:
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('DATABASE', "0.0.0.0"))

db = client["MetaExchange"]
users = db["users"]
user_deleted = db["usersDeleted"]


async def insert_db(db, data):
    return await globals()[db].insert_one(data)

async def find_one_query(db, querry):
    return await globals()[db].find_one(querry)

async def find_query(db, querry):
    cursor =  globals()[db].find(querry)
    return await cursor.to_list(length=1000)
    
async def update_db(db, scdata, ndata):

    return await globals()[db].update_one(scdata, {"$set": ndata}, upsert=True)

async def delete_db(db, obj):
    await globals()[db].delete_one(obj)