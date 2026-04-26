"""2단계: Q&A 데이터셋의 질문을 RAG에 입력하고 답변/검색결과 수집."""
import json

import eval_config as ec
import rag_chain
import config
from gemini_util import call_with_retry


def load_qa_dataset() -> list[dict]:
    with open(ec.QA_DATASET_FILE, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def hit_at_k(sources: list[dict], gold_volume: str, gold_page: int) -> bool:
    for s in sources:
        if s.get("volume") == gold_volume and s.get("page") == gold_page:
            return True
    return False


def main():
    print(f"[2/4] RAG 실행 시작 — 모드: {ec.EVAL_RAG_MODE}")
    if ec.EVAL_RAG_MODE:
        rag_chain.set_mode(ec.EVAL_RAG_MODE)

    dataset = load_qa_dataset()
    print(f"  질문 수: {len(dataset)}")

    results = []
    for i, qa in enumerate(dataset, 1):
        print(f"  [{i}/{len(dataset)}] {qa['id']} ...", end="", flush=True)
        try:
            answer, sources = call_with_retry(rag_chain.ask, qa["question"])
            hit = hit_at_k(sources, qa["source_volume"], qa["source_page"])
            results.append({
                **qa,
                "rag_answer": answer,
                "retrieved": sources,
                "hit_at_k": hit,
            })
            print(f" hit={hit}")
        except Exception as e:
            print(f" 실패: {e}")
            results.append({**qa, "rag_answer": None, "error": str(e)})
    with open(ec.RAG_RESULTS_FILE, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    hits = sum(1 for r in results if r.get("hit_at_k"))
    print(f"\n  완료: {len(results)}개 답변, Hit@{config.TOP_K} = {hits}/{len(results)}")
    print(f"  → {ec.RAG_RESULTS_FILE}")


if __name__ == "__main__":
    main()
