documents = [
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',

'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
'''
import time
from torch import device
import torch
from transformers import AutoModel
from rerank_data import documents

# comment out the flash_attention_2 line if you don't have a compatible GPU
model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-m0',
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="auto",
    # attn_implementation="flash_attention_2",
) # or 'cpu' if no GPU is available

model.to('cuda')  # or 'cpu' if no GPU is available
model.eval()

query = "Organic skincare products for sensitive skin"
# construct sentence pairs
text_pairs = [[query, doc] for doc in documents]



tatol_time = 0

times = 100

print(f"len: {len(documents)}")

for i in range(times):
    time_start = time.time()
    scores = model.compute_score(text_pairs, max_length=1024, doc_type="text",batch_size=128)
    tatol_time += time.time() - time_start
    print(f"time: {time.time() - time_start:.2f}s")

print(f"average time: {tatol_time / times:.2f}s")
''',
]