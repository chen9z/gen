import json
import os

import dotenv
import requests

dotenv.load_dotenv()


def get_stream():
    headers = {
        "Authorization": f"Bearer {os.getenv('SILICON_API_KEY')}",
        "Content-Type": "application/json",
    }

    response = requests.post(os.getenv('SILICON_API_BASE'), stream=True, headers=headers, json={
        "temperature": 0.0,
        "stream": True,
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "messages": [
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]
    })

    response.raise_for_status()
    for line in response.iter_lines():
        line = line.decode("utf-8")
        if line.startswith("data: ") and not line.endswith("[DONE]"):
            data = json.loads(line[len("data: "):])
            chunk = data["choices"][0]["delta"].get("content", "")
            print(chunk, end="", flush=True)


if __name__ == '__main__':
    get_stream()
