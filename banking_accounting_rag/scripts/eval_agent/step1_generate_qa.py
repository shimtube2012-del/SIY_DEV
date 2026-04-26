"""1단계: 문서에서 Q&A 쌍 자동 생성.

docs/md의 페이지를 샘플링해 Gemini로 사실형/추론형/판단형 질문과 정답을 생성한다.
"""
import json
import random
import re
from google import genai
from google.genai import types

import eval_config as ec
import config
import document_loader
from gemini_util import call_with_retry


QA_GEN_PROMPT = """다음은 '은행회계해설' 교재의 한 페이지입니다. 이 페이지를 읽고 **{qa_type}** 유형의 질문과 모범답안을 {n}개 생성하세요.

[페이지 {volume}권 p.{page}]
{page_text}

유형 설명:
- factual: 페이지에 **직접 서술된** 정의/수치/규정을 묻는 단답~간결 질문. (예: "○○의 정의는?", "○○의 한도 비율은?")
- reasoning: 개념 비교, 이유 설명, 원리 도출을 요구하는 질문. 페이지 내용을 종합해야 답변 가능. (예: "○○와 △△의 차이는?", "왜 ○○은 ~하게 처리하는가?")
- judgment: 실무 상황을 가정하고 올바른 회계처리/판단을 묻는 질문. (예: "은행이 ~한 경우 어떻게 회계처리해야 하는가?")

규칙:
- 질문은 페이지 내용만으로 답할 수 있어야 함 (외부 지식 금지).
- 모범답안은 2~4문장으로 핵심을 담되, 페이지 내용에 **근거한** 답만 작성.
- 질문이 너무 표면적이거나 애매하면 생성하지 말 것. 페이지 핵심 개념에 집중.
- 한국어.

JSON 배열로만 출력:
[
  {{"question": "...", "answer": "...", "type": "{qa_type}"}},
  ...
]"""


def load_candidate_pages() -> list[dict]:
    """설정된 권/페이지 범위에서 유효한 페이지들 로딩."""
    all_docs = document_loader.load_all_documents()
    candidates = []
    for doc in all_docs:
        vol = doc.metadata["volume"]
        page = doc.metadata["page"]
        if ec.TARGET_VOLUME and vol != ec.TARGET_VOLUME:
            continue
        if ec.TARGET_PAGE_RANGE:
            lo, hi = ec.TARGET_PAGE_RANGE
            if not (lo <= page <= hi):
                continue
        if len(doc.page_content) < ec.MIN_PAGE_TEXT_LEN:
            continue
        candidates.append({
            "volume": vol,
            "page": page,
            "text": doc.page_content,
        })
    return candidates


def extract_json_array(text: str) -> list:
    """LLM 응답에서 JSON 배열 추출 (markdown 코드블록 등 허용)."""
    text = text.strip()
    m = re.search(r"\[.*\]", text, re.DOTALL)
    if not m:
        raise ValueError(f"JSON 배열을 찾지 못함: {text[:200]}")
    return json.loads(m.group(0))


def generate_qa_for_page(client, page: dict, qa_type: str, n: int) -> list[dict]:
    """한 페이지에서 특정 유형 Q&A 생성."""
    prompt = QA_GEN_PROMPT.format(
        qa_type=qa_type,
        n=n,
        volume=page["volume"],
        page=page["page"],
        page_text=page["text"][:3500],  # 너무 길면 자름
    )
    response = call_with_retry(
        client.models.generate_content,
        model=ec.GENERATOR_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.7,
        ),
    )
    items = extract_json_array(response.text)
    enriched = []
    for item in items:
        if not isinstance(item, dict) or "question" not in item or "answer" not in item:
            continue
        enriched.append({
            "question": item["question"].strip(),
            "gold_answer": item["answer"].strip(),
            "type": qa_type,
            "source_volume": page["volume"],
            "source_page": page["page"],
        })
    return enriched


def main():
    if not config.GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY가 설정되지 않음. .env를 확인하세요.")

    print(f"[1/4] Q&A 생성 시작 — 대상: {ec.TARGET_VOLUME}권 p.{ec.TARGET_PAGE_RANGE}")
    candidates = load_candidate_pages()
    print(f"  후보 페이지: {len(candidates)}개")

    random.seed(42)
    sampled = random.sample(candidates, min(ec.NUM_PAGES_SAMPLE, len(candidates)))
    print(f"  샘플 페이지: {len(sampled)}개")

    client = genai.Client(api_key=config.GEMINI_API_KEY)
    all_qa = []

    for i, page in enumerate(sampled, 1):
        qa_type = ec.QA_TYPES[(i - 1) % len(ec.QA_TYPES)]
        print(f"  [{i}/{len(sampled)}] p.{page['page']} ({qa_type}) ...", end="", flush=True)
        try:
            qas = generate_qa_for_page(client, page, qa_type, ec.QA_PER_PAGE)
            all_qa.extend(qas)
            print(f" {len(qas)}개 생성")
        except Exception as e:
            print(f" 실패: {e}")
        # call_with_retry가 페이싱을 담당하므로 추가 sleep 불필요

    # id 부여
    for idx, qa in enumerate(all_qa, 1):
        qa["id"] = f"q{idx:03d}"

    with open(ec.QA_DATASET_FILE, "w", encoding="utf-8") as f:
        for qa in all_qa:
            f.write(json.dumps(qa, ensure_ascii=False) + "\n")

    print(f"\n  완료: {len(all_qa)}개 Q&A → {ec.QA_DATASET_FILE}")


if __name__ == "__main__":
    main()
