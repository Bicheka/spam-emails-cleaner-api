from fastapi import HTTPException, status
from user.user_model import User, UserResponse
from motor.motor_asyncio import AsyncIOMotorClient
from encryption import encrypt_password, decrypt_password
import os
# Configuration
# MONGO_URI = "mongodb://localhost:27017"  # Update with your MongoDB URI

ATLAS_PASSWORD = os.environ.get("MONGO_ATLAS_PASSWORD")
ATLAS_USERNAME = os.environ.get("MONGO_ATLAS_USERNAME")

MONGO_URI = f"mongodb+srv://{ATLAS_USERNAME}:{ATLAS_PASSWORD}@email-cleaner-db.ccazkdq.mongodb.net/?retryWrites=true&w=majority"  # Update with your MongoDB URI
DATABASE_NAME = "users_db"  # Update with your database name
USERS_COLLECTION = "users"  # Update with your collection name

# MongoDB connection setup
client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[USERS_COLLECTION]


async def create_user(user: User) -> UserResponse:
    # Check if the user already exists
    existing_user = await collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered")

    # Hash the user's password
    hashed_password = encrypt_password(user.password)

    # Insert the new user into the database
    user_data = {"email": user.email, "password": hashed_password}
    await collection.insert_one(user_data)

    return UserResponse(email=user.email)

async def login_user(user: User):
    # Find the user by email
    stored_user = await collection.find_one({"email": user.email})

    if not stored_user or not decrypt_password(stored_user["password"]) == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    return UserResponse(email=user.email)

#fetches one at the time for optimization at large scale
async def fetch_users_from_database():
    cursor = collection.find({})
    async for user in cursor:
        yield user