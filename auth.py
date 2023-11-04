from pydantic import BaseModel, EmailStr, Field

class AuthDetails(BaseModel):
    email: EmailStr = Field(..., description="Email address", example="user@example.com")
    password: str = Field(..., description="Password", min_length=8)