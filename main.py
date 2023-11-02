import imaplib
import email
from email.header import decode_header



# Configuration
EMAIL = input("What is your email: ")
PASSWORD = input("What is your app-password: ")
SPAM_FOLDER = "[Gmail]/Spam"  # The folder where spam emails are moved to

def delete_spam_emails():
    # Connect to the IMAP server (Gmail in this case)
    mail = imaplib.IMAP4_SSL("imap.gmail.com")

    result = None

    # Log in to your email account
    if EMAIL is not None and PASSWORD is not None:
        mail.login(EMAIL, PASSWORD)
        result, _ = mail.select(SPAM_FOLDER)
    else:
        if EMAIL is None and PASSWORD is None:
            print("email and password are none")
        elif EMAIL is None:
            print("Email is none!")
        elif PASSWORD is None:
            print("Password is None!")
    # Select the spam folder
    
    if result!=None and result == "OK":
        # Search for all emails in the spam folder
        result, email_ids = mail.search(None, "ALL")
        
        if result == "OK":
            email_id_list = email_ids[0].split()
            for email_id in email_id_list:
                # Mark the email as deleted
                mail.store(email_id, '+FLAGS', '(\Deleted)')
            
            # Permanently remove deleted emails (Expunge)
            mail.expunge()
        else:
            print("Error searching for emails:", result)

        # Close the mailbox
        mail.close()
    else:
        print("Error selecting folder:", result)
 

    # Logout
    mail.logout()

if __name__ == "__main__":
    delete_spam_emails()


