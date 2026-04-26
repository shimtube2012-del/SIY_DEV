"""벡터 DB 구축 스크립트 — 로컬 bge-m3 임베딩 (단일 컬렉션)."""
import time
import chromadb
import ollama as ollama_client
import config
from document_loader import load_all_documents, chunk_documents

BATCH_SIZE = 20
MAX_RETRIES = 3


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """Ollama bge-m3로 텍스트 임베딩 (재시도 포함)."""
    for attempt in range(MAX_RETRIES):
        try:
            response = ollama_client.embed(model=config.EMBED_MODEL, input=texts)
            return response["embeddings"]
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                wait = 5 * (attempt + 1)
                print(f"    임베딩 오류, {wait}초 후 재시도... ({e})")
                time.sleep(wait)
            else:
                raise


def build():
    print("=" * 50)
    print("벡터 DB 구축 시작")
    print(f"임베딩 모델: {config.EMBED_MODEL}")
    print(f"컬렉션: {config.COLLECTION_NAME}")
    print("=" * 50)

    # 1. 문서 로딩 및 청킹
    print("\n[1/3] 문서 로딩...")
    documents = load_all_documents()

    print("\n[2/3] 청킹...")
    chunks = chunk_documents(documents)

    # 2. ChromaDB 초기화
    print("\n[3/3] 임베딩 및 벡터 DB 저장...")
    client = chromadb.PersistentClient(path=config.CHROMA_DIR)

    # 기존 컬렉션 삭제 후 재생성
    try:
        client.delete_collection(config.COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(
        name=config.COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    # 3. 배치 임베딩 및 저장
    total = len(chunks)
    start = time.time()

    for i in range(0, total, BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        texts = [c.page_content for c in batch]
        metadatas = [c.metadata for c in batch]
        ids = [f"chunk_{i + j}" for j in range(len(batch))]

        embeddings = get_embeddings(texts)

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )

        elapsed = time.time() - start
        progress = min(i + BATCH_SIZE, total)
        print(f"  {progress}/{total} 청크 처리 완료 ({elapsed:.1f}초)")

    elapsed = time.time() - start
    print(f"\n완료! {total}개 청크를 {elapsed:.1f}초 만에 처리")
    print(f"저장 경로: {config.CHROMA_DIR}")


if __name__ == "__main__":
    build()
