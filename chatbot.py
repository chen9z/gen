import os

import dotenv
from langchain_groq import ChatGroq

if __name__ == '__main__':
    dotenv.load_dotenv()

    chat = ChatGroq(model='mixtral-8x7b-32768', temperature=0.2)
    print(chat.invoke("who are you?"))
