import os
from dataclasses import dataclass
from typing import List

import tree_sitter_java as ts_java
from tree_sitter import Language, Parser


@dataclass
class Span:
    start: int
    end: int


@dataclass
class Document:
    chunk_id: str
    path: str
    content: str
    score: float
    start_line: int
    end_line: int


def get_content(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()


class CodeSplitter:

    def __init__(self, chunk_size=500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.chunk_min_size = 200

    def _create_document(self, text, start, end) -> Document:
        return Document(chunk_id='', path='', content=text[start:end], score=0, start_line=start, end_line=end)

    def _chunk_node(self, node, text) -> List[Span]:
        span = Span(node.start_byte, node.start_byte)
        chunks = []
        for child in node.children:
            if child.end_byte - child.start_byte > self.chunk_size:
                if span.end > span.start:
                    chunks.append(span)
                span = Span(child.end_byte, child.end_byte)
                if len(child.children) == 0:
                    chunks.append(Span(child.start_byte, child.end_byte))
                else:
                    chunks.extend(self._chunk_node(child, text))
            elif child.end_byte - span.start > self.chunk_size:
                chunks.append(span)
                span = Span(child.start_byte, child.end_byte)
            else:
                span = Span(span.start, child.end_byte)

        if span.end > span.start:
            chunks.append(span)
        return chunks

    def _connect_chunks(self, chunks: List[Span]):
        for pre, cur in zip(chunks[:-1], chunks[1:]):
            pre.end = cur.start

    def __coalesce_chunks(self, chunks: List[Span]) -> List[Span]:
        new_chunks = []
        current_chunk = Span(0, 0)
        for chunk in chunks:
            if chunk.end - chunk.start < self.chunk_min_size and chunk.end - current_chunk.start < self.chunk_size:
                current_chunk.end = chunk.end
            else:
                if current_chunk.end > current_chunk.start:
                    new_chunks.append(current_chunk)
                current_chunk = Span(chunk.start, chunk.end)
        if current_chunk.end > current_chunk.start:
            if current_chunk.end - current_chunk.start < self.chunk_min_size:
                new_chunks[-1].end = current_chunk.end
            else:
                new_chunks.append(current_chunk)
        return new_chunks

    def _get_line_number(self, source_code: str, index: int) -> int:
        total_chars = 0
        for line_number, line in enumerate(source_code.splitlines(keepends=True), start=1):
            total_chars += len(line)
            if total_chars > index:
                return line_number - 1
        return line_number

    def split_text(self, text: str) -> List[Document]:
        parser = Parser(Language(ts_java.language()))
        tree = parser.parse(bytes(text, "utf-8"))

        root_node = tree.root_node
        if not root_node or not root_node or root_node.type == "ERROR":
            return []

        spans = self._chunk_node(root_node, text)
        self._connect_chunks(spans)
        spans = self.__coalesce_chunks(spans)

        documents = []
        for span in spans:
            documents.append(Document(chunk_id='', path='', content=text[span.start:span.end], score=0,
                                      start_line=self._get_line_number(text, span.start),
                                      end_line=self._get_line_number(text, span.end)))

        return documents


if __name__ == '__main__':
    path = os.path.expanduser(
        "~/workspace/spring-ai/spring-ai-core/src/main/java/org/springframework/ai/model/function/FunctionCallbackContext.java")
    # path = os.path.expanduser(
    #     "~/workspace/spring-ai/README.md")
    text = get_content(path)
    splitter = CodeSplitter(chunk_size=2000)
    results = splitter.split_text(text)
    for chunk in results:
        print(f"================ length:{len(chunk.content)}")
        print(f"{chunk.content}")
