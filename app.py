"""
app.py — Agentic AI Academy (port 8505)

A playful, hands-on course on agentic AI that runs on your own machine:
  • lessons, labs, quizzes, XP and badges (progress in SQLite)
  • real embeddings from Ollama for the vector lab
  • a built-in hybrid-search knowledge base (course notes + knowledge/<shelf>/ docs)
  • a tutor that answers from that knowledge base with a local LLM

Optional: set EXTERNAL_RAG_URL to also query your own RAG service from the
Retrieval Microscope. It must expose POST /search {query, k, domain} and
GET /sources (see README).

Endpoints:
  GET  /                    → the app
  GET  /api/health          → Ollama + knowledge base status
  GET  /api/content         → curriculum (modules + capstones)
  GET  /api/progress        → saved progress
  POST /api/progress        → record an event (lesson / lab / quiz / capstone step)
  POST /api/progress/reset
  POST /api/embed           → embeddings → similarity matrix + 2-D map
  GET  /api/kb/sources      → what the knowledge base contains (?target=external)
  POST /api/kb/reindex      → re-read knowledge/ (after adding your own docs)
  POST /api/search          → hybrid retrieval (target: builtin | external)
  POST /api/tutor           → RAG answer from the built-in knowledge base
"""
import os
import sqlite3
from datetime import datetime

import httpx
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from content import MODULES, CAPSTONES
from engine import KnowledgeEngine

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
CHAT_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "nomic-embed-text")
EXTERNAL_RAG_URL = (os.environ.get("EXTERNAL_RAG_URL") or os.environ.get("RAG_BOT_URL") or "").rstrip("/")
DB_PATH = os.environ.get("DB_PATH", "./data/academy.db")

HERE = os.path.dirname(os.path.abspath(__file__))
app = FastAPI(title="Agentic AI Academy", version="1.1")
app.mount("/static", StaticFiles(directory=os.path.join(HERE, "static")), name="static")

kb = KnowledgeEngine(OLLAMA_URL, EMBED_MODEL, os.path.join(HERE, "knowledge"),
                     os.path.join(os.path.dirname(os.path.abspath(DB_PATH)), "embeddings_cache.json"))

@app.on_event("startup")
def _startup():
    kb.build_async()

# ---------------------------------------------------------------------------
# XP rules
# ---------------------------------------------------------------------------
XP = {"lesson": 10, "lab": 50, "quiz_correct": 20, "capstone_step": 25}
MODULE_IDS = {m["id"] for m in MODULES}
CAPSTONE_STEPS = {c["id"]: len(c["steps"]) for c in CAPSTONES}

# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------
def _db():
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.execute("""CREATE TABLE IF NOT EXISTS progress (
        kind TEXT, module TEXT, item TEXT, value INTEGER, updated TEXT,
        PRIMARY KEY (kind, module, item))""")
    return con

def _progress() -> dict:
    with _db() as con:
        rows = con.execute("SELECT kind, module, item, value FROM progress").fetchall()
    lessons, labs, quiz, caps = {}, set(), {}, {}
    for kind, module, item, value in rows:
        if kind == "lesson":
            lessons.setdefault(module, []).append(int(item))
        elif kind == "lab":
            labs.add(module)
        elif kind == "quiz":
            quiz[module] = value
        elif kind == "capstone":
            caps.setdefault(module, []).append(int(item))

    xp = sum(len(v) for v in lessons.values()) * XP["lesson"] + len(labs) * XP["lab"] \
        + sum(quiz.values()) * XP["quiz_correct"] + sum(len(v) for v in caps.values()) * XP["capstone_step"]

    badges = [m["id"] for m in MODULES
              if len(lessons.get(m["id"], [])) == len(m["lessons"]) and m["id"] in labs and quiz.get(m["id"], 0) >= 4]
    return {"lessons": lessons, "labs": sorted(labs), "quiz": quiz, "capstones": caps,
            "xp": xp, "badges": badges, "level": 1 + xp // 300}

# ---------------------------------------------------------------------------
# Pages, health & content
# ---------------------------------------------------------------------------
@app.get("/")
def index():
    return FileResponse(os.path.join(HERE, "static", "index.html"))

@app.get("/api/health")
def health():
    try:
        tags = httpx.get(f"{OLLAMA_URL}/api/tags", timeout=3).json().get("models", [])
        names = {t["name"].split(":")[0] for t in tags}
        ollama = {"up": True, "chat_model": CHAT_MODEL in names, "embed_model": EMBED_MODEL in names}
    except Exception:
        ollama = {"up": False, "chat_model": False, "embed_model": False}
    return {"status": "ok", "service": "agentic-academy", "ollama": ollama,
            "models": {"chat": CHAT_MODEL, "embed": EMBED_MODEL},
            "kb": {"ready": kb.ready, "chunks": len(kb.chunks), "vectors": kb.vectors_ok, "error": kb.error},
            "external_rag": bool(EXTERNAL_RAG_URL)}

@app.get("/api/content")
def content():
    return {"modules": MODULES, "capstones": CAPSTONES, "xp_rules": XP}

# ---------------------------------------------------------------------------
# Progress
# ---------------------------------------------------------------------------
class ProgressEvent(BaseModel):
    kind: str            # lesson | lab | quiz | capstone
    module: str          # module id or capstone id
    item: int = 0        # lesson index / capstone step index
    value: int = 1       # quiz: number correct (best score kept)
    done: bool = True    # capstone steps can be unticked

@app.get("/api/progress")
def get_progress():
    return _progress()

@app.post("/api/progress")
def post_progress(ev: ProgressEvent):
    if ev.kind not in ("lesson", "lab", "quiz", "capstone"):
        raise HTTPException(400, "unknown kind")
    if ev.kind in ("lesson", "lab", "quiz") and ev.module not in MODULE_IDS:
        raise HTTPException(400, "unknown module")
    if ev.kind == "capstone" and not (ev.module in CAPSTONE_STEPS and 0 <= ev.item < CAPSTONE_STEPS[ev.module]):
        raise HTTPException(400, "unknown capstone step")

    now = datetime.now().isoformat()
    with _db() as con:
        if ev.kind == "quiz":
            old = con.execute("SELECT value FROM progress WHERE kind='quiz' AND module=? AND item='0'",
                              (ev.module,)).fetchone()
            best = max(min(ev.value, 5), old[0] if old else 0)
            con.execute("INSERT OR REPLACE INTO progress VALUES ('quiz', ?, '0', ?, ?)", (ev.module, best, now))
        elif ev.kind == "capstone" and not ev.done:
            con.execute("DELETE FROM progress WHERE kind='capstone' AND module=? AND item=?",
                        (ev.module, str(ev.item)))
        else:
            con.execute("INSERT OR REPLACE INTO progress VALUES (?, ?, ?, 1, ?)",
                        (ev.kind, ev.module, str(ev.item), now))
    return _progress()

@app.post("/api/progress/reset")
def reset_progress():
    with _db() as con:
        con.execute("DELETE FROM progress")
    return _progress()

# ---------------------------------------------------------------------------
# Embedding lab — real vectors from Ollama
# ---------------------------------------------------------------------------
class EmbedRequest(BaseModel):
    texts: list[str]

@app.post("/api/embed")
def embed(req: EmbedRequest):
    texts = [t.strip()[:500] for t in req.texts if t.strip()][:10]
    if len(texts) < 2:
        raise HTTPException(400, "Give at least two sentences.")
    try:
        r = httpx.post(f"{OLLAMA_URL}/api/embed", json={"model": EMBED_MODEL, "input": texts}, timeout=60)
        r.raise_for_status()
        vecs = np.array(r.json()["embeddings"], dtype=float)
    except Exception as e:
        raise HTTPException(502, f"Embedding model unavailable. Is Ollama running with '{EMBED_MODEL}' pulled? ({e.__class__.__name__})")

    unit = vecs / np.linalg.norm(vecs, axis=1, keepdims=True)
    sim = unit @ unit.T
    centred = unit - unit.mean(axis=0)                 # 2-D map: PCA
    _, _, vt = np.linalg.svd(centred, full_matrices=False)
    xy = centred @ vt[:2].T
    span = np.abs(xy).max() or 1.0
    return {"texts": texts, "dims": int(vecs.shape[1]), "similarity": np.round(sim, 3).tolist(),
            "points": np.round(xy / span, 3).tolist(), "preview": np.round(vecs[0][:12], 3).tolist()}

# ---------------------------------------------------------------------------
# Knowledge base: inventory, search
# ---------------------------------------------------------------------------
@app.get("/api/kb/sources")
def kb_sources(target: str = "builtin"):
    if target == "external":
        if not EXTERNAL_RAG_URL:
            raise HTTPException(404, "No external RAG service configured.")
        try:
            r = httpx.get(f"{EXTERNAL_RAG_URL}/sources", timeout=30)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            raise HTTPException(502, f"External RAG unavailable: {e.__class__.__name__}")
    return kb.sources()

@app.post("/api/kb/reindex")
def kb_reindex():
    kb.build()
    return kb.sources()

class SearchRequest(BaseModel):
    query: str
    domain: str | None = None
    k: int = 8
    target: str = "builtin"

@app.post("/api/search")
def search(req: SearchRequest):
    k = max(1, min(req.k, 20))
    if req.target == "external":
        if not EXTERNAL_RAG_URL:
            raise HTTPException(404, "No external RAG service configured.")
        try:
            r = httpx.post(f"{EXTERNAL_RAG_URL}/search", json={"query": req.query, "domain": req.domain, "k": k}, timeout=60)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            raise HTTPException(502, f"External RAG unavailable: {e.__class__.__name__}")
    if not kb.ready:
        raise HTTPException(503, "The knowledge base is still indexing. Try again in a few seconds.")
    return {"query": req.query, "domain": req.domain, "results": kb.search(req.query, k=k, shelf=req.domain or None),
            "vectors": kb.vectors_ok}

# ---------------------------------------------------------------------------
# Tutor — retrieve from the built-in KB, answer with the local chat model
# ---------------------------------------------------------------------------
class TutorTurn(BaseModel):
    role: str
    content: str

class TutorRequest(BaseModel):
    question: str
    module: str | None = None
    history: list[TutorTurn] = []

TUTOR_SYSTEM = (
    "You are the tutor in a hands-on course on building AI agents. The learner is technical "
    "but new to agents. Explain clearly and concretely, with a short example or code snippet "
    "when it helps. Keep answers under 200 words unless asked for more.\n"
    "Ground your answer in the retrieved context below. If the context does not cover the "
    "question, say so plainly, then answer only what you are confident about. Never invent "
    "library APIs, version numbers or statistics."
)

@app.post("/api/tutor")
def tutor(req: TutorRequest):
    if not kb.ready:
        raise HTTPException(503, "The knowledge base is still indexing. Try again in a few seconds.")
    history = [t.model_dump() for t in req.history[-6:]]
    prev = next((t["content"] for t in reversed(history) if t["role"] == "user"), "")
    chunks = kb.search(f"{prev[-300:]} {req.question}" if prev else req.question, k=6)

    system = TUTOR_SYSTEM
    mod = next((m for m in MODULES if m["id"] == req.module), None)
    if mod:
        system += f"\nThe learner is currently studying the module '{mod['title']}'."
    system += "\n\n--- Retrieved context ---\n" + "\n\n".join(c["text"] for c in chunks) + "\n--- End of context ---"

    messages = [{"role": "system", "content": system}] + \
               [{"role": "assistant" if t["role"] == "assistant" else "user", "content": t["content"]} for t in history] + \
               [{"role": "user", "content": req.question}]
    try:
        r = httpx.post(f"{OLLAMA_URL}/api/chat", timeout=240, json={
            "model": CHAT_MODEL, "messages": messages, "stream": False,
            "options": {"temperature": 0.3, "num_ctx": 8192}})
        r.raise_for_status()
        answer = r.json()["message"]["content"]
    except Exception as e:
        raise HTTPException(502, f"Tutor unavailable. Is Ollama running with '{CHAT_MODEL}' pulled? ({e.__class__.__name__})")
    return {"answer": answer, "sources": list(dict.fromkeys(c["source"] for c in chunks))}
