import uuid
from typing import Union, List

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, UpdateStatus, ScoredPoint, VectorParams, Distance
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
        self.vector_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
        )
        points = []
        for sentence in sentences:
            embeddings = self.model.encode(sentence, normalize_embeddings=True)
            text_id = str(uuid.uuid4())
            payload = {"text": sentence}
            point = PointStruct(id=text_id, vector=embeddings.tolist(), payload=payload)
            points.append(point)

        operation = self.vector_client.upsert(
            collection_name=collection_name,
            wait=True,
            points=points
        )

        if operation.status == UpdateStatus.COMPLETED:
            print("Data inserted successfully")
        else:
            print("Data inserted Failed")

    def query(self, collection_name: str, queries: Union[str, List[str]]) -> List[ScoredPoint]:
        q_embeddings = self.model.encode(instruction + queries, normalize_embeddings=True)
        query_result = self.vector_client.search(collection_name, q_embeddings, limit=2)
        return query_result


if __name__ == '__main__':
    query_model = QueryModel()
    connection_name = "design"
    with open("./data/design.md", "r") as f:
        data = f.read()
        spliter = SentenceSpliter(1000, 100)
        results = spliter.split_text(data)
        # for r in results:
            # print(f'Sentence: {r}\n')
        query_model.encode(connection_name, results)

        results = query_model.query(connection_name, "RocketMQ 设计理念")
        for ll in results:
            print(ll)
