import os

import dotenv
from openai import OpenAI

dotenv.load_dotenv()

openai = OpenAI(base_url=os.getenv("OPENAI_API_BASE"), api_key=os.getenv("OPENAI_API_KEY"))

def get_response_message(prompt: str, model="gpt-4o-mini", temperature=0.1) -> str:
    response = openai.chat.completions.create(model=model,
                                              temperature=temperature,
                                              messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content

if __name__ == '__main__':
    print(get_response_message("why the sky is blue?"))
