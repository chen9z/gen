import time
import torch
import os
from transformers import AutoModel, AutoConfig
from rerank_data import documents

# 设置环境变量以启用更详细的日志
os.environ["PYTORCH_JIT_LOG_LEVEL"] = "info"
os.environ["TRANSFORMERS_VERBOSITY"] = "info"


model = AutoModel.from_pretrained(
    "jinaai/jina-reranker-m0",
    torch_dtype=torch.float16,
    trust_remote_code=True,
)
if torch.cuda.is_available():
    print("CUDA is available. Moving model to GPU.")
    model.to('cuda')
else:
    print("CUDA is not available. Model remains on CPU. Flash Attention 2 will not work.")
model.eval()



query = "Organic skincare products for sensitive skin"
text_pairs = [[query, doc] for doc in documents]

total_time = 0
times = 50

print("\n=== 性能测试 ===")
print(f"Number of documents to process: {len(documents)}")

# 主测试循环
torch.cuda.synchronize()
for i in range(times):
    time_start = time.time()

    with torch.inference_mode():
        scores = model.compute_score(
            text_pairs,
            doc_type="text"
        )

    torch.cuda.synchronize()
    batch_time = time.time() - time_start
    total_time += batch_time
    print(f"Batch {i+1}/{times}, time: {batch_time:.2f}s")

print(f"\nAverage time per batch: {total_time/times:.2f}s")
