from fastapi import FastAPI
import imaplib
import email
from typing import List
from messages import messages


app = FastAPI()

def fetch_emails(username: str, password: str, imap_server: str , email_Type : str) -> List[str]:

    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)
    mail.select('inbox')

    listOfMessages = []
    result, data = mail.search(None, email_Type)
    if result == 'OK':
        for num in data[0].split():
            result, data = mail.fetch(num, '(RFC822)')
            if result == 'OK':
                email_msg = email.message_from_bytes(data[0][1])

                listOfMessages.append({
                    'from': messages.decode_mime_messages(email_msg['From']),
                    'subject': messages.decode_mime_messages(email_msg['Subject']),
                    'content': messages.get_content_from_message(email_msg)
                })

    mail.close()
    mail.logout()
    return listOfMessages

@app.get("/fetch-emails/")
def read_emails(username: str, password: str, imap_server: str , email_Type: str):
    emails = fetch_emails(username, password, imap_server, email_Type)
    
