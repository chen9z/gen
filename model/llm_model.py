import os

import dotenv
from openai import OpenAI

dotenv.load_dotenv()

openai = OpenAI(
    base_url=os.getenv("OPENAI_API_BASE"), api_key=os.getenv("OPENAI_API_KEY")
)

ollama = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


def get_response_message(
    prompt: str, model="gpt-3.5-turbo-0613", temperature=0.1
) -> str:
    response = openai.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def get_response_message_with_ollama(
    prompt: str, model="qwen2.5:7b-instruct-q6_K", temperature=0.1
) -> str:
    response = ollama.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


async def get_ollama_response_async(messages, model="qwen2.5:7b-instruct-q6_K"):
    response = ollama.chat.completions.create(
        model=model, messages=messages, temperature=0.1
    )
    return response.choices[0].message.content


def get_stream_response_ollama(
    prompt: str, model="llama3:8b-instruct-q6_K", temperature=0.1
):
    completions = ollama.chat.completions.create(
        model=model,
        temperature=temperature,
        stream=True,
        messages=[{"role": "user", "content": prompt}],
    )
    for chunk in completions:
        print(chunk.choices[0].delta.content)


def get_response_tool(messages, tools=None, model="llama3.1:8b-instruct-q8_0"):
    response = ollama.chat.completions.create(
        model=model, messages=messages, tools=tools, temperature=0.1
    )
    return response


if __name__ == "__main__":
    print(
        get_response_message_with_ollama(
            "why the sky is blue", model="qwen2.5:7b-instruct-q6_K"
        )
    )
    print(get_response_message_with_ollama("你是谁", model="qwen2.5:7b-instruct-q6_K"))
