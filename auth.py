from pydantic import BaseModel, EmailStr, Field

class AuthDetails(BaseModel):
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., description="Password")