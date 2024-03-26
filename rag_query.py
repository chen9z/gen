from typing import Union, List

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from spliter import SentenceSpliter

instruction = "为这个句子生成表示以用于检索相关文章："


class QueryModel:
    def __init__(self, model_name_or_path="BAAI/bge-large-zh-v1.5", persist_dir="./storage"):
        self.model_name_or_path = model_name_or_path
        self.persist_dir = persist_dir
        self.model = SentenceTransformer(model_name_or_path)
        self.vector_client = QdrantClient(path=persist_dir)

    def encode(self, collection_name: str, sentences: List[str]):
        embedding = self.model.encode(sentences, normalize_embeddings=True)
        docs = ["Qdrant has Langchain integrations", "Qdrant also has Llama Index integrations"]
        metadata = [{"source": "LangChain-docs"}, {"source": "LlamaIndex-docs"}]
        ids = [42, 2]
        self.vector_client.add(collection_name=collection_name,
                               documents=docs,
                               metadata=metadata,
                               ids=ids)

    def query(self, collection_name: str, queries: Union[str, List[str]]):
        query_result = self.vector_client.query(collection_name, "langchain", limit=2)
        pass


if __name__ == '__main__':
    query_model = QueryModel()
    with open("./data/design.md", "r") as f:
        data = f.read()
        spliter = SentenceSpliter(400, 20)
        results = spliter.split_text(data)
        for r in results:
            if len(r) > 0:
                query_model.encode(r)
