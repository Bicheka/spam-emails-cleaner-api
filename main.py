import uvicorn
from fastapi import FastAPI, HTTPException
from auth import AuthDetails
from email_deletion import delete_spam_emails

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/clear")
async def clear_spam_emails(data: AuthDetails):
    try:
        email = data.email
        password = data.password
        print("Email: " + email)
        print("Password: " + password)
        result = await delete_spam_emails(data)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
