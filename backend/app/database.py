from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URL= os.getenv("MONGO_URL", "mongodb://localhost:27017")

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_URL)
db = client["multi_business_db"]
houses_collection = db["houses"]  # Collection for houses
products_collection=db['stocks']

