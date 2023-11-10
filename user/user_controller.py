from fastapi import APIRouter, HTTPException
from user.user_model import User, UserResponse
import user.user_service as user_service
router = APIRouter()


# Create a new user
@router.post("/register", response_model=UserResponse)
async def register_user(user: User):
    try:
        await user_service.register_user(user)
        return {
                "status": "success",
                "message": user.email + " registered successfully" + " and spams emails will be deleted every 3 hours"
            }
    
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred: " + str(e))
    
    

# Authenticate a user
@router.post("/login", response_model=UserResponse)
async def login_user(user: User):
    return await user_service.login_user(user)
