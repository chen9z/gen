import re
from typing import List

import jieba

from data_entity import Document


class Splitter:

    def split(self, path: str, model_max_token: int, tokenizer) -> List[Document]:
        raise NotImplementedError


class SentenceSpliter(Splitter):

    def __init__(self, chunk_size=500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, path: str, model_max_token, tokenizer) -> List[Document]:
        pass

    def split_text(self, text: str) -> List[str]:
        sentence_endings = {'\n\n', '。', '！', '？', '；', '…'}
        chunks, current_chunk = [], ''
        for word in jieba.cut(text):
            if len(current_chunk) + len(word) > self.chunk_size:
                chunks.append(current_chunk.strip())
                current_chunk = word
            else:
                current_chunk += word
            if word[-1] in sentence_endings and len(current_chunk) > self.chunk_size - self.chunk_overlap:
                chunks.append(current_chunk.strip())
                current_chunk = ''
        if current_chunk:
            chunks.append(current_chunk.strip())
        if self.chunk_overlap > 0 and len(chunks) > 1:
            chunks = self._handle_overlap(chunks)
        return chunks

    def _handle_overlap(self, chunks: List[str]) -> List[str]:
        overlapped_chunks = []
        for i in range(len(chunks) - 1):
            chunk = chunks[i] + ' ' + chunks[i + 1][:self.chunk_overlap]
            overlapped_chunks.append(chunk.strip())
        overlapped_chunks.append(chunks[-1])
        return overlapped_chunks


class TextSpliter(Splitter):

    def split(self, path, max_token, tokenize) -> List[Document]:
        with open(path, "r") as file:
            result = []
            cache_line = []
            tokens = 0
            title = ""
            last_line = -1
            for index, line in enumerate(file):
                if line.strip() == "":
                    continue
                if tokens == 0 and index == 0:
                    title = line
                line_tokens = tokenize(line)
                if tokens + len(line_tokens) > max_token:
                    result.append(Document(title=title, content="".join(cache_line), start_line=last_line + 1,
                                           end_line=index, metadata={"title": title}))
                    cache_line = []
                    last_line = index
                    tokens = 0
                    continue
                if re.match(r'^\s*(第.+章|第.+回|后记)\s+.*$', line):
                    result.append(Document(title=title, content="".join(cache_line), start_line=last_line + 1,
                                           end_line=index, metadata={"title": title}))
                    cache_line = []
                    last_line = index
                    title = line
                    tokens = 0
                cache_line.append(line)
                tokens += len(line_tokens)
            return result


if __name__ == '__main__':
    path = "../data/ymxt.txt"
    tokenize = lambda x: x
    splitter = TextSpliter()
    docs = splitter.split(path, 512, tokenize)
    for doc in docs:
        print(doc.__dict__)
