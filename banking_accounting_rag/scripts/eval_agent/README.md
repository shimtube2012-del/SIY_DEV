# RAG 평가 에이전트

은행회계 RAG 시스템의 정답율을 자동으로 측정하는 4단계 파이프라인.

## 구조

```
eval_agent/
├── eval_config.py       # 평가 설정 (샘플 범위, 모델, 경로)
├── step1_generate_qa.py # 문서에서 Q&A 자동 생성
├── step2_run_rag.py     # RAG에 질문 입력 → 답변 수집
├── step3_judge.py       # LLM-as-a-judge 채점 (0~3점)
├── step4_report.py      # 마크다운/CSV 리포트 생성
├── run_all.py           # 전체 파이프라인 실행
└── data/                # 결과물 (gitignore)
```

## 사용법

```bash
# 사전 요구
# - .env에 GEMINI_API_KEY 설정
# - 벡터 DB 구축 완료 (src/build_vectordb.py 실행)
# - 모드가 local이면 Ollama 서버 실행 중

cd scripts/eval_agent

# 전체 실행
python run_all.py

# 단계별 실행 (중단/재실행 가능)
python step1_generate_qa.py
python step2_run_rag.py
python step3_judge.py
python step4_report.py
```

## 기본 설정 (MVP)

`eval_config.py` 참고. 기본값:

- 대상: 상권 p.41~140 (제3장 재무상태표 초반)
- 페이지 10개 × 유형별 Q&A 2개 = 총 20문제
- 유형: factual / reasoning / judgment 순환 배정
- 생성·채점 모델: `gemini-2.5-flash`
- 평가 대상 RAG 모드: `gemini` (변경하려면 `EVAL_RAG_MODE`)

## 출력

- `data/qa_dataset.jsonl` — 생성된 Q&A 쌍 (출처 페이지 포함)
- `data/rag_results.jsonl` — RAG 답변 + 검색된 청크 + Hit@K
- `data/judgments.jsonl` — 채점 결과 (점수 + 근거)
- `data/report.md` — 사람이 읽는 요약 리포트
- `data/report.csv` — 스프레드시트 분석용

## 지표

- **평균 점수**: 0~3점 평균
- **정답율**: 2점 이상 비율 (완전정답 + 대체로 정답)
- **Hit@K**: 검색된 상위 K개 청크에 정답 페이지가 포함된 비율

## MVP 이후 확장 아이디어

- 씨드(사람이 만든) 질문을 `qa_dataset.jsonl`에 수동 병합
- Judge 편향 검증: 전체 중 10~20개를 사람이 재채점해 judge 신뢰도 확인
- 튜닝 실험: `src/config.py`의 `CHUNK_SIZE`, `TOP_K` 변경 전후 `report.md` 비교
- 하이브리드 검색/리랭킹 도입 시 A/B 비교
