from fastapi import APIRouter, HTTPException
from user.user_model import User, UserResponse
import user.user_service as user_service
router = APIRouter()


# Create a new user
@router.post("/register")
async def register_user(user: User):
    await user_service.create_user(user)
    return {
            "status": "success",
            "message": user.email + " registered successfully" + " and spams emails will be deleted every 3 hours."
        }

# Authenticate a user
@router.post("/login")
async def login_user(user: User):
    return await user_service.login_user(user)

@router.delete("/unregister")
async def delete_user(user: User):
    await user_service.delete_user(user)
    return {
            "status": "success",
            "message": user.email + " unregistered successfully. spams emails will not be deleted from this account anymore."
        }