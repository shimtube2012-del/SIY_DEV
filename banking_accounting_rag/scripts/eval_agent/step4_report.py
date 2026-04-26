"""4단계: 채점 결과를 집계해 마크다운/CSV 리포트 생성."""
import csv
import json
from collections import defaultdict
from datetime import datetime

import eval_config as ec


def load_judgments() -> list[dict]:
    with open(ec.JUDGMENTS_FILE, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def aggregate(judgments: list[dict]) -> dict:
    scored = [j for j in judgments if j.get("score") is not None]
    n = len(scored)
    total = sum(j["score"] for j in scored)

    by_type = defaultdict(list)
    for j in scored:
        by_type[j.get("type", "unknown")].append(j["score"])

    hits = sum(1 for j in scored if j.get("hit_at_k"))

    # 정답율 = 2점 이상 비율
    correct = sum(1 for j in scored if j["score"] >= 2)

    return {
        "total_questions": len(judgments),
        "scored": n,
        "avg_score": total / n if n else 0.0,
        "max_score": n * 3,
        "total_score": total,
        "accuracy_ge2": correct / n if n else 0.0,  # 2점 이상
        "hit_at_k_rate": hits / n if n else 0.0,
        "by_type": {
            t: {
                "n": len(scores),
                "avg": sum(scores) / len(scores),
                "accuracy_ge2": sum(1 for s in scores if s >= 2) / len(scores),
            }
            for t, scores in by_type.items()
        },
    }


def render_markdown(agg: dict, judgments: list[dict]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    md = [
        f"# RAG 평가 리포트",
        f"",
        f"- 생성 시각: {now}",
        f"- 평가 모드: `{ec.EVAL_RAG_MODE}`",
        f"- 대상: {ec.TARGET_VOLUME}권 p.{ec.TARGET_PAGE_RANGE}, 페이지 {ec.NUM_PAGES_SAMPLE}개 × Q&A {ec.QA_PER_PAGE}",
        f"",
        f"## 요약",
        f"",
        f"| 지표 | 값 |",
        f"|------|-----|",
        f"| 총 질문 수 | {agg['total_questions']} |",
        f"| 채점 완료 | {agg['scored']} |",
        f"| 평균 점수 | **{agg['avg_score']:.2f} / 3** |",
        f"| 정답율 (2점 이상) | **{agg['accuracy_ge2'] * 100:.1f}%** |",
        f"| Hit@K (검색 정확도) | **{agg['hit_at_k_rate'] * 100:.1f}%** |",
        f"",
        f"## 유형별",
        f"",
        f"| 유형 | 문제 수 | 평균 | 정답율 |",
        f"|------|--------|------|--------|",
    ]
    for t, v in agg["by_type"].items():
        md.append(f"| {t} | {v['n']} | {v['avg']:.2f} | {v['accuracy_ge2'] * 100:.1f}% |")

    md += [
        f"",
        f"## 실패 케이스 (점수 < 2)",
        f"",
    ]
    failures = [j for j in judgments if j.get("score") is not None and j["score"] < 2]
    failures.sort(key=lambda x: (x["score"], x["id"]))
    if not failures:
        md.append("_없음_")
    for j in failures[:15]:
        md += [
            f"### {j['id']} — {j.get('type', '-')} (점수: {j['score']}, Hit: {j.get('hit_at_k')})",
            f"**질문:** {j['question']}",
            f"",
            f"**모범답안:** {j['gold_answer']}",
            f"",
            f"**RAG 답변:** {(j.get('rag_answer') or '(없음)')[:500]}",
            f"",
            f"**채점 근거:** {j.get('judge_reason', '')}",
            f"",
            f"**출처(골드):** {j['source_volume']}권 p.{j['source_page']} / **검색됨:** {j.get('retrieved', [])[:3]}",
            f"",
            f"---",
            f"",
        ]
    return "\n".join(md)


def render_csv(judgments: list[dict]) -> list[dict]:
    rows = []
    for j in judgments:
        rows.append({
            "id": j.get("id"),
            "type": j.get("type"),
            "score": j.get("score"),
            "hit_at_k": j.get("hit_at_k"),
            "source_volume": j.get("source_volume"),
            "source_page": j.get("source_page"),
            "question": j.get("question"),
            "gold_answer": j.get("gold_answer"),
            "rag_answer": (j.get("rag_answer") or "")[:500],
            "judge_reason": j.get("judge_reason"),
        })
    return rows


def main():
    print("[4/4] 리포트 생성")
    judgments = load_judgments()
    agg = aggregate(judgments)

    md = render_markdown(agg, judgments)
    with open(ec.REPORT_MD_FILE, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"  마크다운 → {ec.REPORT_MD_FILE}")

    rows = render_csv(judgments)
    with open(ec.REPORT_CSV_FILE, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"  CSV → {ec.REPORT_CSV_FILE}")

    print(f"\n=== 요약 ===")
    print(f"평균: {agg['avg_score']:.2f}/3")
    print(f"정답율 (2점 이상): {agg['accuracy_ge2'] * 100:.1f}%")
    print(f"Hit@K: {agg['hit_at_k_rate'] * 100:.1f}%")


if __name__ == "__main__":
    main()
