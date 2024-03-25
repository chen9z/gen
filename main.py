import os
import logging
import sys

import dotenv
from llama_index.core.embeddings import resolve_embed_model
from llama_index.llms.openai import OpenAI
from llama_index.core import set_global_handler
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, load_index_from_storage, Settings, StorageContext

if __name__ == '__main__':
    dotenv.load_dotenv()
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    client = OpenAI(model="gpt-3.5-turbo-0613", temperature=0)
    client.api_base = os.getenv("OPENAI_API_BASE")
    client.api_key = os.getenv("OPENAI_API_KEY")

    Settings.embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")
    Settings.llm = client
    set_global_handler("simple")

    PERSIST_DIR = "./storage"
    index = None
    if os.path.exists(PERSIST_DIR):
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
    else:
        documents = SimpleDirectoryReader("./data").load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir="./storage")

    query_engine = index.as_query_engine()
    response = query_engine.query("hi")
    print(response)
