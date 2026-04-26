"""설정값 모듈."""
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 현재 모드 ("local", "gemini", "openai") — LLM만 전환, 임베딩은 항상 로컬
MODE = "local"

# === 임베딩 (모든 모드 공통, Ollama bge-m3) ===
OLLAMA_BASE_URL = "http://localhost:11434"
EMBED_MODEL = "bge-m3"

# === LLM 모드별 설정 ===
LOCAL_LLM_MODEL = "gemma3:12b"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_LLM_MODEL = "gemini-2.5-flash"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_LLM_MODEL = "gpt-4o"

# 문서 경로
DOCS_DIR = os.path.join(BASE_DIR, "docs", "md")

# 청킹
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# 벡터 DB (단일 컬렉션, 임베딩 모델 공통)
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "bank_accounting"
TOP_K = 5
