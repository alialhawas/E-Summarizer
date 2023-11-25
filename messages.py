import base64
import quopri
import re


class messages:
    
    def __init__(self,From: str , Subject: str , content: str):
        self.From = From
        self.Subject = Subject
        self.content = content
        
    def get_content_from_message (email_msg):
    
        if email_msg.is_multipart():
            for part in email_msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" not in content_disposition and "text/plain" in content_type:
                    body = part.get_payload(decode=True).decode()
                    return body
        else:
            body = email_msg.get_payload(decode=True).decode()
            return body

    def decode_mime_messages(subject):
        mime_word_pattern = re.compile(r'=\?([^?]+)\?([BbQq])\?([^?]+)\?=')

        def decode_mime_word(encoded_word, charset, encoding):
            if encoding.lower() == 'b':
                byte_string = base64.b64decode(encoded_word)
            elif encoding.lower() == 'q':
                byte_string = quopri.decodestring(encoded_word)
            return byte_string.decode(charset)
        
        decoded_string = mime_word_pattern.sub(
            lambda match: decode_mime_word(match.group(3), match.group(1), match.group(2)),
            subject
        )

        return decoded_string
