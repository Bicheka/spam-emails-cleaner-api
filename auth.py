from pydantic import BaseModel, EmailStr, Field

class AuthDetails(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
