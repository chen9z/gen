from transformers import AutoModel

# Initialize the model
model = AutoModel.from_pretrained("jinaai/jina-embeddings-v3", trust_remote_code=True)
model.to("cuda")

texts = [
    "Follow the white rabbit.",  # English
    "Sigue al conejo blanco.",  # Spanish
    "Suis le lapin blanc.",  # French
    "跟着白兔走。",  # Chinese
    "اتبع الأرنب الأبيض.",  # Arabic
    "Folge dem weißen Kaninchen.",  # German
]

# When calling the `encode` function, you can choose a `task` based on the use case:
# 'retrieval.query', 'retrieval.passage', 'separation', 'classification', 'text-matching'
# Alternatively, you can choose not to pass a `task`, and no specific LoRA adapter will be used.
embeddings0 = model.encode(texts)
embeddings1 = model.encode(texts, task="retrieval.query")
embeddings2 = model.encode(texts, task="retrieval.passage")
embeddings3 = model.encode(texts, task="separation")
embeddings4 = model.encode(texts, task="classification")
embeddings5 = model.encode(texts, task='text-matching')

# Compute similarities
print(embeddings0[0] @ embeddings0[3].T)
print(embeddings1[0] @ embeddings1[3].T)
print(embeddings2[0] @ embeddings2[3].T)
print(embeddings3[0] @ embeddings3[3].T)
print(embeddings4[0] @ embeddings4[3].T)
print(embeddings5[0] @ embeddings5[3].T)
