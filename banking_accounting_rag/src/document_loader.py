"""마크다운 문서 로딩 및 청킹 모듈."""
import os
import re
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import config


def parse_markdown(file_path: str) -> list[Document]:
    """마크다운 파일을 페이지 단위로 파싱하여 Document 리스트로 반환."""
    filename = os.path.basename(file_path)
    volume = "상" if "상" in filename else "하"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # <!-- Page N --> 기준으로 분할
    page_pattern = r"<!-- Page (\d+) -->\n(.*?)(?=<!-- Page \d+ -->|$)"
    pages = re.findall(page_pattern, content, re.DOTALL)

    documents = []
    for page_num, page_text in pages:
        text = page_text.strip()
        # 구분선 제거
        text = re.sub(r"\n---\n?", "", text)
        if not text or len(text) < 10:
            continue
        documents.append(Document(
            page_content=text,
            metadata={"volume": volume, "page": int(page_num), "source": filename},
        ))

    return documents


def load_all_documents() -> list[Document]:
    """docs/md 폴더의 모든 마크다운 파일을 로딩."""
    all_docs = []
    for filename in sorted(os.listdir(config.DOCS_DIR)):
        if filename.endswith(".md"):
            path = os.path.join(config.DOCS_DIR, filename)
            docs = parse_markdown(path)
            all_docs.extend(docs)
            print(f"  로딩 완료: {filename} ({len(docs)}개 페이지)")
    print(f"  총 {len(all_docs)}개 페이지 로딩")
    return all_docs


def chunk_documents(documents: list[Document]) -> list[Document]:
    """문서를 청크로 분할."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", "。", ". ", " ", ""],
    )

    chunks = []
    for doc in documents:
        splits = splitter.split_text(doc.page_content)
        for i, text in enumerate(splits):
            chunks.append(Document(
                page_content=text,
                metadata={
                    **doc.metadata,
                    "chunk_index": i,
                    "chunk_total": len(splits),
                },
            ))

    print(f"  총 {len(chunks)}개 청크 생성")
    return chunks


if __name__ == "__main__":
    docs = load_all_documents()
    chunks = chunk_documents(docs)
    # 샘플 출력
    for c in chunks[:3]:
        print(f"\n[{c.metadata}]")
        print(c.page_content[:200])
