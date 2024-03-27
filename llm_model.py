import os

import dotenv
from openai import OpenAI
from groq import Groq
import google.generativeai as genai

dotenv.load_dotenv()

openai = OpenAI(base_url=os.getenv("OPENAI_API_BASE"), api_key=os.getenv("OPENAI_API_KEY"))
groq = Groq(api_key=os.getenv("GROQ_API_KEY"), base_url=os.getenv("GROQ_API_BASE"))

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")


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


def get_response_message_with_gemini(prompt: str) -> str:
    return model.generate_content(prompt).text
