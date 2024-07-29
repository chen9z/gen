from typing import List, Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from transformers import AutoModel
from numpy.linalg import norm

DEFAULT_MODEL = "jinaai/jina-embeddings-v2-base-code"
cos_sim = lambda a, b: (a @ b.T) / (norm(a) * norm(b))
model = AutoModel.from_pretrained(DEFAULT_MODEL, trust_remote_code=True)


class EmbeddingRequest(BaseModel):
    input: List[str]
    model: str = Field(default=DEFAULT_MODEL, description="Use Default Model for embeddings")


class EmbeddingResponse(BaseModel):
    data: List[dict]
    model: str
    usage: dict


def get_embedding(text: str) -> List[float]:
    return model.encode(text).tolist()


app = FastAPI()


@app.post("/v1/embeddings")
def get_embeddings(request: EmbeddingRequest) -> EmbeddingResponse:
    if not request.input:
        raise HTTPException(status_code=400, detail="Input cannot be empty")

    embeddings = [get_embedding(text) for text in request.input]
    response = EmbeddingResponse(
        data=[
            {
                "object": "embedding",
                "embedding": embedding,
                "index": i
            } for i, embedding in enumerate(embeddings)
        ],
        model=request.model,
        usage={
            "prompt_tokens": sum(len(text.split()) for text in request.input),
            "total_tokens": sum(len(text.split()) for text in request.input)
        }
    )

    return response


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
