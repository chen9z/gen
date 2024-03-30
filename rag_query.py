import uuid
from typing import Union, List

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, UpdateStatus, ScoredPoint, VectorParams, Distance
from sentence_transformers import SentenceTransformer

from spliter import Splitter

instruction = "为这个句子生成表示以用于检索相关文章："

class QueryIndex:
    def __init__(self, splitter: Splitter, model_name_or_path="BAAI/bge-large-zh-v1.5", persist_dir="./storage"):
        self.model_name_or_path = model_name_or_path
        self.persist_dir = persist_dir
        self.encoder = SentenceTransformer(model_name_or_path, trust_remote_code=True)
        self.vector_client = QdrantClient(path=persist_dir)
        self.splitter = splitter

    def encode(self, collection_name: str, path: str):
        model_token = self.encoder.get_sentence_embedding_dimension()
        # check if collection exists
        if self.vector_client.collection_exists(collection_name=collection_name):
            return

        self.vector_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=model_token,
                                        distance=Distance.COSINE),
        )

        documents = self.splitter.split(path, model_token, self.encoder.tokenizer.tokenize)
        points = []
        for doc in documents:
            print(f">>>>>>>>>>>>>Encoding {doc.title}, start line: {doc.start_line}, end line: {doc.end_line}")
            embeddings = self.encoder.encode(doc.content, show_progress_bar=True, normalize_embeddings=True)
            text_id = str(uuid.uuid4())
            point = PointStruct(id=text_id, vector=embeddings.tolist(), payload=doc.__dict__)
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

    def query(self, collection_name: str, queries: Union[str, List[str]], limit=10) -> List[ScoredPoint]:
        q_embeddings = self.encoder.encode(instruction + queries, normalize_embeddings=True)
        query_result = self.vector_client.search(collection_name, q_embeddings, limit=limit)
        return query_result
