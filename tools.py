import logging
import os

import dotenv
import requests
from docling.document_converter import DocumentConverter

dotenv.load_dotenv()

search_url = os.getenv("SEARCH_URL")


def search_web(query: str):
    if not search_url:
        raise ValueError("SEARCH URL not configured")
    params = {"format": "json", "q": query}
    try:
        response = requests.get(search_url, params)
        response.raise_for_status()
        data = response.json()
        return data["results"]
    except Exception as e:
        logging.error(e)
        return None
    return []


async def search_web_async(query: str):
    return search_web(query)


async def fetch_webpage_text(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    coverter = DocumentConverter()
    result = coverter.convert(url, headers=headers)
    return result.document.export_to_markdown()


if __name__ == "__main__":
    pass
