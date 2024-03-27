import uuid
from typing import Union, List

from qdrant_client import QdrantClient
from qdrant_client.http.models import CollectionStatus
from qdrant_client.models import PointStruct, UpdateStatus, ScoredPoint, VectorParams, Distance
from sentence_transformers import SentenceTransformer

instruction = "为这个句子生成表示以用于检索相关文章："


class QueryModel:
    def __init__(self, model_name_or_path="BAAI/bge-large-zh-v1.5", persist_dir="./storage"):
        self.model_name_or_path = model_name_or_path
        self.persist_dir = persist_dir
        self.encoder = SentenceTransformer(model_name_or_path, trust_remote_code=True)
        self.vector_client = QdrantClient(path=persist_dir)

    def encode(self, collection_name: str, sentences: List[str]):
        collection_info = self.vector_client.get_collection(collection_name=collection_name)
        if collection_info is None or collection_info.status != CollectionStatus.GREEN:
            self.vector_client.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=self.encoder.get_sentence_embedding_dimension(),
                                            distance=Distance.COSINE),
            )
        points = []
        for sentence in sentences:
            embeddings = self.encoder.encode(sentence, show_progress_bar=True, normalize_embeddings=True)
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

    def query(self, collection_name: str, queries: Union[str, List[str]], limit=5) -> List[ScoredPoint]:
        q_embeddings = self.encoder.encode(instruction + queries, normalize_embeddings=True)
        query_result = self.vector_client.search(collection_name, q_embeddings, limit=limit * 10)
        return sorted(query_result, key=lambda x: x.score, reverse=True)[:limit]
