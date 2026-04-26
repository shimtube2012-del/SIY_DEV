"""평가 에이전트 설정 — MVP 기본값."""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# === 샘플링 범위 (MVP: 작게) ===
# 특정 권/페이지 범위 지정. None이면 전체 문서에서 랜덤 샘플링.
TARGET_VOLUME = "상"
TARGET_PAGE_RANGE = (41, 140)  # 제3장 재무상태표 계정과목 초반부

NUM_PAGES_SAMPLE = 5    # 샘플링할 페이지 수 (Free tier 5 RPM 고려한 MVP 크기)
QA_PER_PAGE = 2         # 페이지당 생성할 Q&A 수 → 총 10문제

MIN_PAGE_TEXT_LEN = 300  # 너무 짧은 페이지는 스킵 (목차/표지 등)

# === Q&A 생성 ===
GENERATOR_MODEL = "gemini-2.5-flash"
QA_TYPES = ["factual", "reasoning", "judgment"]
# factual: 책 내용 직접 인용 질문 (정의/수치/규정)
# reasoning: 두 개념 비교나 왜 그런지 설명
# judgment: 특정 상황에서 어떤 회계처리를 해야 하는지

# === 채점 (Judge) ===
JUDGE_MODEL = "gemini-2.5-flash"
# 루브릭 0~3점
# 0: 틀림 / 무관한 답 / 환각
# 1: 부분 일치 (핵심 내용은 맞으나 중요한 누락/오류)
# 2: 대체로 정답 (사소한 누락)
# 3: 완전 정답

# === RAG 실행 ===
# None이면 현재 rag_chain 설정(config.MODE) 사용. "local"/"gemini"/"openai" 강제 가능.
EVAL_RAG_MODE = "gemini"

# === 파일 경로 ===
QA_DATASET_FILE = os.path.join(DATA_DIR, "qa_dataset.jsonl")
RAG_RESULTS_FILE = os.path.join(DATA_DIR, "rag_results.jsonl")
JUDGMENTS_FILE = os.path.join(DATA_DIR, "judgments.jsonl")
REPORT_MD_FILE = os.path.join(DATA_DIR, "report.md")
REPORT_CSV_FILE = os.path.join(DATA_DIR, "report.csv")
