
from vllm import LLM

llm = LLM(model="Kwaipilot/OASIS-code-1.3B", task="embed", trust_remote_code=True)
(output,) = llm.embed("Hello, my name is")

embeds = output.outputs.embedding
print(f"Embeddings: {embeds!r} (size={len(embeds)})")
