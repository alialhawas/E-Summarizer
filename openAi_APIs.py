from openai import OpenAI
from utils import openAI_key


def Summarize_emails (emails):

    client = OpenAI(
        api_key=openAI_key,
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content":"Summarize these emails:\n\n" + emails ,
            }
        ],
        model="gpt-3.5-turbo",
    )

    return  chat_completion.choices[0].message.content