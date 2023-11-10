import imaplib
from fastapi import HTTPException
from auth import AuthDetails

async def delete_spam_emails(user: AuthDetails)->{}:
    SPAM_FOLDER = "[Gmail]/Spam"  # The folder where spam emails are moved to by Gmail

    try:
        # Connect to the IMAP server (Gmail in this case)
        with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
            # Log in to email account
            mail.login(user.email, user.password)
            
            #increase the maximum number of messages to be handled
            mail._MAXLINE = 1000000

            # Select the spam folder
            result, _ = mail.select(SPAM_FOLDER)
            if result != "OK":
                raise HTTPException(status_code=401, detail="Error selecting folder: " + result)

            # Search for all emails in the spam folder
            result, email_ids = mail.search(None, "ALL")
            if result != "OK":
                raise HTTPException(status_code=500, detail="Error searching for emails: " + result)

            email_id_list = email_ids[0].split()
            for email_id in email_id_list:
                # Mark the email as deleted
                mail.store(email_id, '+FLAGS', '(\Deleted)')

            # Permanently remove deleted emails (Expunge)
            mail.expunge()

            return {
                "status": "success",
                "emails_deleted": len(email_id_list),
                "message": "Deleted " + str(len(email_id_list)) + " emails from " + user.email
            }

    except imaplib.IMAP4.error as e:
        raise HTTPException(status_code=401, detail="Error authenticating email or app password might be wrong")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred")
