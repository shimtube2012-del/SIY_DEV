"""Flask 웹 서버 — 멀티 백엔드 지원."""
import json
import os

from flask import Flask, render_template, request, jsonify, Response, stream_with_context

import config
import rag_chain

app = Flask(
    __name__,
    template_folder=os.path.join(config.BASE_DIR, "templates"),
    static_folder=os.path.join(config.BASE_DIR, "static"),
)
app.secret_key = "bank-accounting-rag-2024"


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/get_mode", methods=["GET"])
def get_mode():
    """현재 모드 및 사용 가능 모드 조회."""
    available = ["local"]
    if config.GEMINI_API_KEY:
        available.append("gemini")
    if config.OPENAI_API_KEY:
        available.append("openai")

    # 벡터 DB 컬렉션 존재 여부 확인 (단일 컬렉션)
    import chromadb
    client = chromadb.PersistentClient(path=config.CHROMA_DIR)
    existing = [c.name for c in client.list_collections()]
    has_db = config.COLLECTION_NAME in existing

    modes = {}
    for mode in ["local", "gemini", "openai"]:
        has_key = mode in available
        modes[mode] = {
            "available": has_key and has_db,
            "has_api_key": has_key,
            "has_vectordb": has_db,
        }

    return jsonify({
        "current_mode": rag_chain.get_mode(),
        "modes": modes,
    })


@app.route("/set_mode", methods=["POST"])
def set_mode():
    """모드 변경."""
    data = request.get_json()
    mode = data.get("mode", "").strip()

    try:
        rag_chain.set_mode(mode)
        return jsonify({"mode": mode, "message": f"{mode} 모드로 전환되었습니다."})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/ask", methods=["POST"])
def ask():
    """질문에 대한 답변 반환 (비스트리밍)."""
    data = request.get_json()
    query = data.get("query", "").strip()
    history = data.get("history", [])

    if not query:
        return jsonify({"error": "질문을 입력해주세요."}), 400

    try:
        answer, sources = rag_chain.ask(query, history)
        return jsonify({"answer": answer, "sources": sources})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/stream", methods=["POST"])
def stream():
    """SSE 스트리밍 응답."""
    data = request.get_json()
    query = data.get("query", "").strip()
    history = data.get("history", [])

    if not query:
        return jsonify({"error": "질문을 입력해주세요."}), 400

    def generate():
        try:
            stream_response, sources = rag_chain.ask_stream(query, history)
            for chunk in stream_response:
                yield f"data: {json.dumps({'token': chunk['token']}, ensure_ascii=False)}\n\n"
            yield f"data: {json.dumps({'sources': sources, 'done': True}, ensure_ascii=False)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    print("=" * 50)
    print("은행회계해설 AI 서비스")
    print(f"현재 모드: {rag_chain.get_mode()}")
    print("http://localhost:5000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)
