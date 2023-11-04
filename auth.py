from pydantic import BaseModel, EmailStr

class AuthDetails(BaseModel):
    email: EmailStr
    password: str