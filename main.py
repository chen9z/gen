import os
import logging
import sys

import dotenv
from openai import OpenAI
from qdrant_client import QdrantClient

import llm_model

dotenv.load_dotenv()
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
os.environ["TOKENIZERS_PARALLELISM"] = "false"
llm = OpenAI(base_url=os.getenv("OPENAI_API_BASE"), api_key=os.getenv("OPENAI_API_KEY"))

prompt_template = """
You are a large language AI assistant. You are given a user question, and please write clean, concise and accurate answer to the question. You will be given a set of related contexts to the question. Please use the context and cite the context at the end of each sentence if applicable.

Your answer must be correct, accurate and written by an expert using an unbiased and professional tone. Please limit to 1024 tokens. Do not give any information that is not related to the question, and do not repeat. Say "information is missing on" followed by the related topic, if the given context do not provide sufficient information.

your answer must be written in the same language as the question.

Here are the set of contexts:

{context}

Answer language: Chinese
Remember, don't blindly repeat the contexts verbatim. And here is the user question:
"""

if __name__ == '__main__':
    # collect_name="test_doc"
    # client = QdrantClient(path=".storage")
    # docs = ["Qdrant has Langchain integrations", "Qdrant also has Llama Index integrations"]
    # metadata = [{"source": "LangChain-docs"}, {"source": "LlamaIndex-docs"}]
    # ids = [42, 2]
    # client.add(collection_name=collect_name,
    #            documents=docs,
    #            metadata=metadata,
    #            ids=ids)
    #
    # query_result = client.query(collect_name, "langchain", limit=2)
    # print(query_result)
    # system_prompt = prompt_template.format(context="\n\n".join(response.document for response in query_result))
    # system_prompt = system_prompt + "\nwhat is langchain"
    #
    # print(llm_model.get_response_message(system_prompt))
    print(llm_model.get_response_message_with_gemini("write a stroy about a cat and a dog playing in the park."))
