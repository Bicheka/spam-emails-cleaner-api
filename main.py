import uvicorn
from fastapi import FastAPI, HTTPException
from model.Auth import AuthDetails
from email_deletion import delete_spam_emails

app = FastAPI()

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
        return e
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
