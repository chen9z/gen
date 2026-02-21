from typing import List

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sympy.physics.quantum.gate import normalized
from transformers import AutoModel

DEFAULT_MODEL = "jinaai/jina-embeddings-v3"
model = AutoModel.from_pretrained(DEFAULT_MODEL, trust_remote_code=True)
model.to("cuda")


class EmbeddingRequest(BaseModel):
    input: List[str]
    model: str = Field(default=DEFAULT_MODEL, description="Use Default Model for embeddings")


class EmbeddingResponse(BaseModel):
    data: List[dict]
    model: str
    usage: dict


def get_embedding(text: str) -> List[float]:
    try:
        embedding = model.encode([text])[0]
        normalized_embedding = embedding / np.linalg.norm(embedding)
        return normalized_embedding.tolist()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error encoding text: {str(e)}")


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
