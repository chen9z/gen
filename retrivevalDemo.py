from langchain_community.document_loaders import WebBaseLoader
from typing import Dict
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter


def parse_retriever_input(params: Dict):
    return params["messages"][-1].content


if __name__ == '__main__':
    loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=0)
    all_splitters = text_splitter.split_documents(data)

    print(all_splitters)


