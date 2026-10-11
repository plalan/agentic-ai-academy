"""
engine.py — the Academy's built-in knowledge engine.

A small, dependency-light RAG backend so the Academy runs anywhere Ollama runs:
  • documents: the course itself (content.py) + knowledge/<shelf>/*.md|*.txt
  • chunking: paragraph-aware, ~600 chars with ~100 overlap
  • vectors: Ollama embeddings (cached on disk by content hash)
  • keywords: in-memory BM25
  • hybrid ranking: Reciprocal Rank Fusion, with a keyword boost for
    identifier-like terms (CamelCase, codes with digits, acronyms)
If Ollama is unreachable, search degrades to keyword-only instead of failing.
"""
import os
import re
import json
import math
import hashlib
import threading
from collections import Counter, defaultdict

import httpx
import numpy as np

from content import MODULES, CAPSTONES

CHUNK_SIZE, CHUNK_OVERLAP, MIN_CHUNK = 600, 100, 80
RRF_K, W_VECTOR, W_KEYWORD, W_KEYWORD_IDENT = 60, 1.0, 1.0, 1.3

_STOP = set("""a an the and or but if of to in on at by for with from as is are was were be been being
this that these those it its into than then so such not no do does did can could should would
will shall may might must have has had i you he she we they them his her our your their what which
who whom how why when where there here all any each more most other some own same very just about
over under again further once only also""".split())
_TOKEN = re.compile(r"[a-z0-9][a-z0-9_\-]*")
_IDENT = re.compile(r"\b(?:[\w\-]*\d[\w\-]*|[A-Za-z]*[a-z][A-Z]\w*|[A-Z]{2,}[a-z]?)\b")


def tokenize(text: str) -> list[str]:
    return [t for t in _TOKEN.findall(text.lower()) if len(t) > 1 and t not in _STOP]


def identifiers(query: str) -> set[str]:
    return {t for m in _IDENT.findall(query) for t in tokenize(m)}


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Pack paragraphs into ~size-char chunks; split oversized paragraphs on sentences."""
    pieces = []
    for para in re.split(r"\n\s*\n", text):
        para = para.strip()
        if not para:
            continue
        if len(para) <= size:
            pieces.append(para)
        else:
            pieces += [s.strip() for s in re.split(r"(?<=[.!?])\s+", para) if s.strip()]
    chunks, cur = [], ""
    for p in pieces:
        if cur and len(cur) + len(p) + 1 > size:
            chunks.append(cur)
            cur = cur[-overlap:].split(" ", 1)[-1] + " " + p if overlap else p
        else:
            cur = f"{cur}\n{p}" if cur else p
    if cur:
        chunks.append(cur)
    return [c for c in chunks if len(c.strip()) >= MIN_CHUNK]


# ---------------------------------------------------------------------------
# Course text — the curriculum itself is the first shelf
# ---------------------------------------------------------------------------
def _plain(s: str) -> str:
    return re.sub(r"\*\*(.+?)\*\*", r"\1", s)


def course_documents() -> list[tuple[str, str]]:
    docs = []
    for i, m in enumerate(MODULES):
        out = [f"# Module {i}: {m['title']}", m["tagline"], ""]
        for les in m["lessons"]:
            out += [f"## {les['title']}", ""] + [_plain(p) + "\n" for p in les["body"]]
            if les.get("analogy"):
                out += [f"Analogy: {les['analogy']}", ""]
            if les.get("code"):
                out += ["Example code:", les["code"], ""]
        out += ["## Check your understanding", ""]
        out += [f"Q: {_plain(q['q'])}\nA: {q['options'][q['answer']]}. {q['why']}\n" for q in m["quiz"]]
        docs.append((f"Module {i}: {m['title']}", "\n".join(out)))
    caps = ["# Capstone projects", ""]
    for c in CAPSTONES:
        caps += [f"## {c['title']}", c["goal"], ""] + [f"- {s}" for s in c["steps"]] + [""]
    docs.append(("Capstone projects", "\n".join(caps)))
    return docs


# ---------------------------------------------------------------------------
# The engine
# ---------------------------------------------------------------------------
class KnowledgeEngine:
    def __init__(self, ollama_url: str, embed_model: str, knowledge_dir: str, cache_path: str):
        self.ollama_url, self.embed_model = ollama_url, embed_model
        self.knowledge_dir, self.cache_path = knowledge_dir, cache_path
        self.lock = threading.Lock()
        self.ready, self.error, self.vectors_ok = False, None, False
        self._reset()

    def _reset(self):
        self.chunks: list[dict] = []          # {id, text, source, shelf}
        self.matrix: np.ndarray | None = None  # unit vectors, one row per chunk
        self.postings: dict[str, list[tuple[int, int]]] = defaultdict(list)
        self.doc_len: list[int] = []
        self.avgdl = 1.0

    # --- loading -----------------------------------------------------------
    def _documents(self) -> list[tuple[str, str, str]]:
        docs = [("course", title, text) for title, text in course_documents()]
        if os.path.isdir(self.knowledge_dir):
            for shelf in sorted(os.listdir(self.knowledge_dir)):
                folder = os.path.join(self.knowledge_dir, shelf)
                if not os.path.isdir(folder):
                    continue
                for root, _, files in os.walk(folder):
                    for name in sorted(files):
                        if not name.lower().endswith((".md", ".txt")) or name.lower() == "readme.md":
                            continue
                        try:
                            with open(os.path.join(root, name), encoding="utf-8") as f:
                                docs.append((shelf, name, f.read()))
                        except (OSError, UnicodeDecodeError):
                            continue
        return docs

    def _embed(self, texts: list[str]) -> list[list[float]]:
        out = []
        for k in range(0, len(texts), 64):
            r = httpx.post(f"{self.ollama_url}/api/embed",
                           json={"model": self.embed_model, "input": texts[k:k + 64]}, timeout=120)
            r.raise_for_status()
            out += r.json()["embeddings"]
        return out

    def build(self):
        with self.lock:
            self._reset()
            self.ready, self.error = False, None
            for shelf, source, text in self._documents():
                for j, c in enumerate(chunk_text(text)):
                    cid = hashlib.sha1(f"{source}|{j}|{c}".encode()).hexdigest()
                    self.chunks.append({"id": cid, "text": c, "source": source, "shelf": shelf})

            # keyword index
            for i, ch in enumerate(self.chunks):
                tf = Counter(tokenize(ch["text"]))
                self.doc_len.append(sum(tf.values()))
                for term, n in tf.items():
                    self.postings[term].append((i, n))
            self.avgdl = (sum(self.doc_len) / len(self.doc_len)) if self.doc_len else 1.0

            # vectors (cached by chunk id)
            cache = {}
            try:
                with open(self.cache_path) as f:
                    cache = json.load(f)
                if cache.get("_model") != self.embed_model:
                    cache = {}
            except (OSError, ValueError):
                pass
            try:
                if not self.ollama_url:                  # demo mode: keyword search only, by design
                    raise RuntimeError("embeddings disabled")
                missing = [c for c in self.chunks if c["id"] not in cache]
                if missing:
                    for c, v in zip(missing, self._embed([c["text"] for c in missing])):
                        cache[c["id"]] = v
                    cache["_model"] = self.embed_model
                    os.makedirs(os.path.dirname(os.path.abspath(self.cache_path)), exist_ok=True)
                    with open(self.cache_path, "w") as f:
                        json.dump({k: cache[k] for k in [c["id"] for c in self.chunks] + ["_model"] if k in cache}, f)
                m = np.array([cache[c["id"]] for c in self.chunks], dtype=float)
                self.matrix = m / np.linalg.norm(m, axis=1, keepdims=True)
                self.vectors_ok = True
            except Exception as e:                      # Ollama down → keyword-only
                self.matrix, self.vectors_ok = None, False
                self.error = None if not self.ollama_url else \
                    f"Vector search unavailable ({e.__class__.__name__}); using keyword search only."
            self.ready = True

    def build_async(self):
        threading.Thread(target=self.build, daemon=True).start()

    # --- search ------------------------------------------------------------
    def _bm25(self, query: str, shelf: str | None, n: int) -> list[int]:
        N, scores = len(self.chunks), defaultdict(float)
        for term in set(tokenize(query)):
            plist = self.postings.get(term)
            if not plist:
                continue
            idf = math.log(1 + (N - len(plist) + 0.5) / (len(plist) + 0.5))
            for i, tf in plist:
                if shelf and self.chunks[i]["shelf"] != shelf:
                    continue
                dl = self.doc_len[i]
                scores[i] += idf * tf * 2.5 / (tf + 1.5 * (0.25 + 0.75 * dl / self.avgdl))
        return [i for i, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]]

    def _vector(self, query: str, shelf: str | None, n: int) -> list[int]:
        if not self.vectors_ok or self.matrix is None:
            return []
        try:
            q = np.array(self._embed([query[:1000]])[0], dtype=float)
        except Exception:
            return []
        sims = self.matrix @ (q / np.linalg.norm(q))
        order = np.argsort(-sims)
        return [int(i) for i in order if not shelf or self.chunks[i]["shelf"] == shelf][:n]

    def search(self, query: str, k: int = 8, shelf: str | None = None, pool: int = 30) -> list[dict]:
        if not self.ready:
            return []
        found: dict[int, dict] = {}
        for rank, i in enumerate(self._vector(query, shelf, pool), 1):
            found[i] = {"vector_rank": rank, "keyword_rank": None}
        for rank, i in enumerate(self._bm25(query, shelf, pool), 1):
            found.setdefault(i, {"vector_rank": None, "keyword_rank": None})["keyword_rank"] = rank
        w_kw = W_KEYWORD_IDENT if any(t in self.postings for t in identifiers(query)) else W_KEYWORD
        out = []
        for i, r in found.items():
            score = sum(w / (RRF_K + rank) for w, rank in ((W_VECTOR, r["vector_rank"]), (w_kw, r["keyword_rank"])) if rank)
            ch = self.chunks[i]
            out.append({"id": ch["id"], "text": ch["text"], "source": ch["source"], "domain": ch["shelf"],
                        "score": round(score, 5), **r})
        out.sort(key=lambda x: x["score"], reverse=True)
        return out[:k]

    # --- inventory ---------------------------------------------------------
    def sources(self) -> dict:
        shelves: dict[str, Counter] = defaultdict(Counter)
        for ch in self.chunks:
            shelves[ch["shelf"]][ch["source"]] += 1
        return {
            "ready": self.ready, "vectors": self.vectors_ok, "error": self.error,
            "chunks": len(self.chunks),
            "shelves": {s: [{"source": src, "chunks": n} for src, n in sorted(c.items())] for s, c in shelves.items()},
        }
