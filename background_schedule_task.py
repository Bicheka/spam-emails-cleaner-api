import asyncio
from user.user_service import fetch_users_from_database
from email_deletion import delete_spam_emails
from encryption import decrypt_password
from auth import AuthDetails

async def schedule_spam_deletion():
    while True:
        print ("claning emails...")
        users = await fetch_users_from_database()

        for user in users:
            try:
                decoded_password = decrypt_password(user["password"])
                response = await delete_spam_emails(AuthDetails(email=user["email"], password=decoded_password))
                print(response)
            except Exception as e:
                # Handle the error or log it, and proceed to the next user
                print(f"Error for user {user['email']}: {str(e)}")
        await asyncio.sleep(30) #sleep for 30 seconds before running again