"""3단계: LLM-as-a-judge로 RAG 답변 채점 (0~3점)."""
import json
import re
from google import genai
from google.genai import types

import eval_config as ec
import config
from gemini_util import call_with_retry


JUDGE_PROMPT = """당신은 은행회계 시험 채점관입니다. 아래 질문에 대한 모범답안과 응시자 답변을 비교해 0~3점으로 채점하세요.

[질문]
{question}

[모범답안]
{gold_answer}

[응시자 답변]
{rag_answer}

채점 루브릭:
- 3점 (완전정답): 모범답안의 핵심 내용을 모두 포함하고, 사실 오류가 없음.
- 2점 (대체로 정답): 핵심은 맞으나 사소한 누락/표현 차이가 있음.
- 1점 (부분 정답): 핵심 일부만 맞고 중요한 누락이나 오류가 있음.
- 0점 (틀림): 무관한 답, 환각(허위 정보), 완전한 오류.

주의:
- 응시자 답변이 출처 페이지를 정확히 찍었는지는 평가에 반영하지 말 것 (내용 정확성만 본다).
- 모범답안보다 더 풍부해도 **사실 오류가 없으면** 감점하지 말 것.
- 응시자가 "확인되지 않습니다"라고 회피했는데 모범답안에 내용이 있으면 0~1점.

JSON으로만 출력:
{{"score": <0|1|2|3>, "reason": "<짧은 근거 1~2문장>"}}"""


def extract_json_object(text: str) -> dict:
    text = text.strip()
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        raise ValueError(f"JSON을 찾지 못함: {text[:200]}")
    return json.loads(m.group(0))


def judge_one(client, item: dict) -> dict:
    prompt = JUDGE_PROMPT.format(
        question=item["question"],
        gold_answer=item["gold_answer"],
        rag_answer=item.get("rag_answer") or "(답변 없음)",
    )
    response = call_with_retry(
        client.models.generate_content,
        model=ec.JUDGE_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.0,
        ),
    )
    parsed = extract_json_object(response.text)
    return {
        "score": int(parsed.get("score", 0)),
        "reason": parsed.get("reason", "").strip(),
    }


def main():
    if not config.GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY가 설정되지 않음.")

    print(f"[3/4] 채점 시작 — 모델: {ec.JUDGE_MODEL}")

    with open(ec.RAG_RESULTS_FILE, "r", encoding="utf-8") as f:
        items = [json.loads(line) for line in f if line.strip()]

    client = genai.Client(api_key=config.GEMINI_API_KEY)
    judgments = []

    for i, item in enumerate(items, 1):
        print(f"  [{i}/{len(items)}] {item['id']} ...", end="", flush=True)
        if not item.get("rag_answer"):
            judgments.append({**item, "score": 0, "judge_reason": "RAG 답변 없음"})
            print(" 0 (답변없음)")
            continue
        try:
            j = judge_one(client, item)
            judgments.append({**item, "score": j["score"], "judge_reason": j["reason"]})
            print(f" {j['score']}")
        except Exception as e:
            print(f" 실패: {e}")
            judgments.append({**item, "score": None, "judge_reason": f"채점 실패: {e}"})
    with open(ec.JUDGMENTS_FILE, "w", encoding="utf-8") as f:
        for j in judgments:
            f.write(json.dumps(j, ensure_ascii=False) + "\n")

    scored = [j for j in judgments if j.get("score") is not None]
    total = sum(j["score"] for j in scored)
    max_total = len(scored) * 3
    print(f"\n  완료: 평균 {total / len(scored):.2f}/3, 합계 {total}/{max_total}")
    print(f"  → {ec.JUDGMENTS_FILE}")


if __name__ == "__main__":
    main()
