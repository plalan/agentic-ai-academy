"""
export_kb.py — Write the curriculum as markdown files, one per module,
so any other RAG system can ingest the same material the lessons teach.
(The Academy's built-in knowledge engine reads content.py directly.)

  python export_kb.py <target_dir>
"""
import os
import re
import sys
from content import MODULES, CAPSTONES

def _plain(text: str) -> str:
    return re.sub(r"\*\*(.+?)\*\*", r"\1", text)

def module_md(m: dict) -> str:
    out = [f"# {m['title']}", "", m["tagline"], ""]
    for les in m["lessons"]:
        out += [f"## {les['title']}", ""]
        out += [_plain(p) + "\n" for p in les["body"]]
        if les.get("analogy"):
            out += [f"Analogy: {les['analogy']}", ""]
        if les.get("code"):
            out += ["```python", les["code"], "```", ""]
    out += ["## Check your understanding", ""]
    for q in m["quiz"]:
        out += [f"Q: {_plain(q['q'])}", f"A: {q['options'][q['answer']]}. {q['why']}", ""]
    return "\n".join(out)

def capstones_md() -> str:
    out = ["# Agentic AI capstone projects", ""]
    for c in CAPSTONES:
        out += [f"## {c['title']}", "", c["goal"], ""] + [f"- {s}" for s in c["steps"]] + [""]
    return "\n".join(out)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python export_kb.py <target_dir>")
    target = sys.argv[1]
    os.makedirs(target, exist_ok=True)
    for i, m in enumerate(MODULES, 1):
        with open(os.path.join(target, f"{i:02d}_{m['id']}.md"), "w", encoding="utf-8") as f:
            f.write(module_md(m))
    with open(os.path.join(target, "10_capstones.md"), "w", encoding="utf-8") as f:
        f.write(capstones_md())
    print(f"Wrote {len(MODULES) + 1} files to {os.path.abspath(target)}")
