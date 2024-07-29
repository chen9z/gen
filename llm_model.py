import os

import dotenv
from openai import OpenAI
from groq import Groq

dotenv.load_dotenv()

openai = OpenAI(base_url=os.getenv("OPENAI_API_BASE"), api_key=os.getenv("OPENAI_API_KEY"))
groq = Groq(api_key=os.getenv("GROQ_API_KEY"), base_url=os.getenv("GROQ_API_BASE"))


ollama = OpenAI(base_url="http://localhost:8081/v1", api_key="ollama")

def get_response_message(prompt: str, model="gpt-3.5-turbo-0613", temperature=0.1) -> str:
    response = openai.chat.completions.create(model=model,
                                              temperature=temperature,
                                              messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content


def get_response_message_with_groq(prompt: str, model="mixtral-8x7b-32768", temperature=0.1) -> str:
    response = groq.chat.completions.create(model=model,
                                            temperature=temperature,
                                            messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content

def get_response_message_with_chatglm(prompt: str) -> str:
    openai.base_url = "http://0.0.0.0:8000/v1"
    response = openai.chat.completions.create(
        model="chatglm3-6b-128k",
        temperature=0.3,
        top_p=0.2,
        max_tokens=128 * 1024,
        messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content


def get_response_message_with_ollama(prompt: str, model="llama3:8b-instruct-q6_K", temperature=0.1) -> str:
    response = ollama.chat.completions.create(model=model,
                                              temperature=temperature,
                                              messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content

def get_stream_response_ollama(prompt: str, model="llama3:8b-instruct-q6_K", temperature=0.1):
    completions = ollama.chat.completions.create(model=model,
                                              temperature=temperature,
                                              stream=True,
                                              messages=[{"role": "user", "content": prompt}]
                                              )
    for chunk in completions:
        print(chunk.choices[0].delta.content)


if __name__ == '__main__':
    print(get_response_message_with_ollama("why the sky is blue", model="qwen2:7b-instruct-q6_K"))
    print(get_response_message_with_ollama("你是谁", model="qwen2:7b-instruct-q6_K"))
