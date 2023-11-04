from typing import Union
from fastapi import FastAPI




    
app = FastAPI()

@app.post("/clear")
async def login(data: dict):
    email = data.get("email")
    password = data.get("password")

    return {"email": email, "password": password}