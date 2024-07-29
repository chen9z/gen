import os

import dotenv
from groq import Groq

if __name__ == '__main__':
    dotenv.load_dotenv()
    base_url = os.getenv('GROQ_API_BASE')
    api_key = os.getenv('GROQ_API_KEY')
    llm = Groq(base_url=base_url, api_key=api_key)

    chat_completion = llm.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Explain the importance of low latency LLMs",
            }
        ],
        model="mixtral-8x7b-32768",
    )

    print(chat_completion.choices[0].message.content)
