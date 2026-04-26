"""RAG 파이프라인 모듈 — 멀티 LLM 백엔드 지원 (임베딩은 로컬 공통)."""
import chromadb
import ollama as ollama_client
import config

SYSTEM_PROMPT = """당신은 은행회계 전문가입니다. 아래 제공된 '은행회계해설' 참고자료를 근거로 답변하세요.

규칙:
- 참고자료에 관련 내용이 있으면 이를 바탕으로 구체적으로 답변하세요.
- 참고자료에 직접적인 내용이 없더라도 관련 내용을 활용하여 최대한 답변하되, 참고자료에서 직접 확인되지 않는 부분은 그 점을 명시하세요.
- 참고자료와 전혀 관련 없는 질문에만 "해당 내용은 은행회계해설에서 확인되지 않습니다"라고 답하세요.
- 답변 마지막에 반드시 출처(상/하권, 페이지)를 표기하세요. 형식: 📖 출처: 은행회계해설(상) p.123
- 회계 용어는 정확하게 사용하세요.
- 한국어로 답변하세요.
"""

# 런타임 모드 (app.py에서 변경)
_current_mode = None


def get_mode() -> str:
    return _current_mode or config.MODE


def set_mode(mode: str):
    global _current_mode
    if mode not in ("local", "gemini", "openai"):
        raise ValueError(f"지원하지 않는 모드: {mode}")
    _current_mode = mode


# ── 벡터 DB (단일 컬렉션, 임베딩 공통) ──

def get_collection():
    """ChromaDB 컬렉션 반환."""
    client = chromadb.PersistentClient(path=config.CHROMA_DIR)
    return client.get_collection(config.COLLECTION_NAME)


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """Ollama bge-m3로 텍스트 임베딩 (모든 모드 공통)."""
    response = ollama_client.embed(model=config.EMBED_MODEL, input=texts)
    return response["embeddings"]


# ── 검색 ──

def retrieve(query: str, top_k: int = None) -> list[dict]:
    """질문과 유사한 문서 청크 검색."""
    if top_k is None:
        top_k = config.TOP_K

    collection = get_collection()
    query_embedding = get_embeddings([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    contexts = []
    for i in range(len(results["ids"][0])):
        contexts.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i] if results.get("distances") else None,
        })
    return contexts


def build_prompt(query: str, contexts: list[dict]) -> str:
    """검색 결과를 포함한 프롬프트 생성."""
    context_text = ""
    for i, ctx in enumerate(contexts, 1):
        meta = ctx["metadata"]
        source = f"은행회계해설({meta['volume']}) p.{meta['page']}"
        context_text += f"\n[참고자료 {i}] ({source})\n{ctx['text']}\n"

    return f"""다음 참고자료를 바탕으로 질문에 답변하세요.

{context_text}

질문: {query}"""


# ── LLM 답변 생성 (모드별 분기) ──

def ask(query: str, history: list[dict] = None) -> tuple:
    """질문에 대한 답변 생성 (비스트리밍)."""
    contexts = retrieve(query)
    prompt = build_prompt(query, contexts)
    messages = _build_messages(prompt, history)
    mode = get_mode()

    if mode == "local":
        answer = _ask_local(messages)
    elif mode == "gemini":
        answer = _ask_gemini(messages)
    elif mode == "openai":
        answer = _ask_openai(messages)

    sources = [
        {"volume": c["metadata"]["volume"], "page": c["metadata"]["page"]}
        for c in contexts
    ]
    return answer, sources


def ask_stream(query: str, history: list[dict] = None):
    """질문에 대한 답변 스트리밍 생성. (generator, sources) 반환."""
    contexts = retrieve(query)
    prompt = build_prompt(query, contexts)
    messages = _build_messages(prompt, history)
    mode = get_mode()

    if mode == "local":
        gen = _stream_local(messages)
    elif mode == "gemini":
        gen = _stream_gemini(messages)
    elif mode == "openai":
        gen = _stream_openai(messages)

    sources = [
        {"volume": c["metadata"]["volume"], "page": c["metadata"]["page"]}
        for c in contexts
    ]
    return gen, sources


def _build_messages(prompt: str, history: list[dict] = None) -> list[dict]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": prompt})
    return messages


# ── 로컬 (Ollama) ──

def _ask_local(messages: list[dict]) -> str:
    response = ollama_client.chat(model=config.LOCAL_LLM_MODEL, messages=messages)
    return response["message"]["content"]


def _stream_local(messages: list[dict]):
    """Ollama 스트리밍."""
    stream = ollama_client.chat(
        model=config.LOCAL_LLM_MODEL, messages=messages, stream=True,
    )
    for chunk in stream:
        yield {"token": chunk["message"]["content"]}


# ── Gemini API ──

def _ask_gemini(messages: list[dict]) -> str:
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    contents = _messages_to_gemini(messages)
    response = client.models.generate_content(
        model=config.GEMINI_LLM_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    return response.text


def _stream_gemini(messages: list[dict]):
    """Gemini 스트리밍."""
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    contents = _messages_to_gemini(messages)
    for chunk in client.models.generate_content_stream(
        model=config.GEMINI_LLM_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    ):
        if chunk.text:
            yield {"token": chunk.text}


def _messages_to_gemini(messages: list[dict]) -> list:
    """OpenAI 형식 메시지를 Gemini contents로 변환."""
    from google.genai import types
    contents = []
    for msg in messages:
        if msg["role"] == "system":
            continue  # system_instruction으로 전달
        role = "user" if msg["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))
    return contents


# ── OpenAI API ──

def _ask_openai(messages: list[dict]) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=config.OPENAI_LLM_MODEL,
        messages=messages,
    )
    return response.choices[0].message.content


def _stream_openai(messages: list[dict]):
    """OpenAI 스트리밍."""
    from openai import OpenAI
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    stream = client.chat.completions.create(
        model=config.OPENAI_LLM_MODEL,
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            yield {"token": delta.content}


if __name__ == "__main__":
    q = "은행회계의 규제체계에 대해 설명해줘"
    print(f"질문: {q}\n")
    answer, sources = ask(q)
    print(f"답변:\n{answer}")
    print(f"\n출처: {sources}")
