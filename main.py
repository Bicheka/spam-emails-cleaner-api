from fastapi import FastAPI, HTTPException
import asyncio
from auth import AuthDetails
from email_deletion import delete_spam_emails
from background_schedule_task import schedule_spam_deletion

from fastapi.middleware.cors import CORSMiddleware

# database import
from user.user_controller import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(schedule_spam_deletion())


@app.get("/test")
async def root():
    return {"message": "working ok"}

@app.post("/clear")
async def clear_spam_emails(data: AuthDetails):
    try:
        result = await delete_spam_emails(data)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


app.include_router(router)