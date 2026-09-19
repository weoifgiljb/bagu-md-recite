# -*- coding: utf-8 -*-
"""Rebuild 背诵本/questions.json and patch 背诵本/index.html from Typora题库."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TY = ROOT / "Typora题库"
OUT = ROOT / "背诵本"
QUESTIONS_JSON = OUT / "questions.json"
INDEX_HTML = OUT / "index.html"

SCAN_FOLDERS = [
    "03-AI前端",
    "04-RAG与Agent",
    "05-Flutter",
    "06-Taro小程序",
    "07-浏览器网络补洞",
    "09-项目深挖",
    "10-Vue3",
    "11-CSS与样式",
    "12-BOM-DOM-Ajax",
    "13-前端安全",
    "14-DevTools实操",
    "15-算法Hot100",
]

WEEK_MAP = {
    "03-AI前端": "第1周 · AI前端",
    "04-RAG与Agent": "第2周 · RAG/Agent",
    "05-Flutter": "第3周 · Flutter",
    "06-Taro小程序": "第4周 · Taro",
    "07-浏览器网络补洞": "第4周 · 浏览器",
    "09-项目深挖": "项目深挖 · 秋招准备",
    "10-Vue3": "补洞 · Vue3",
    "11-CSS与样式": "补洞 · CSS样式",
    "12-BOM-DOM-Ajax": "补洞 · BOM/DOM/Ajax",
    "13-前端安全": "补洞 · 前端安全",
    "14-DevTools实操": "补洞 · DevTools",
    "15-算法Hot100": "补洞 · 算法Hot100",
}

WEEK_ORDER = [
    "第1周 · AI前端",
    "第2周 · RAG/Agent",
    "第3周 · Flutter",
    "第4周 · Taro",
    "第4周 · 浏览器",
    "补洞 · DevTools",
    "补洞 · 算法Hot100",
    "补洞 · JavaScript",
    "补洞 · React",
    "计划",
    "其他",
]



def discover_folders() -> list[str]:
    """Scan Typora题库 for theme folders. Prefer SCAN_FOLDERS order, then append unknowns.
    Skip 00/01/02: 00 is plan docs; 01/02 cards are kept from legacy questions.json.
    """
    if not TY.is_dir():
        return list(SCAN_FOLDERS)
    found = [d.name for d in sorted(TY.iterdir()) if d.is_dir() and not d.name.startswith(".")]
    skip = {x for x in found if x.startswith("00-") or x.startswith("01-") or x.startswith("02-")}
    ordered = [x for x in SCAN_FOLDERS if x in found]
    extra = [x for x in found if x not in SCAN_FOLDERS and x not in skip]
    return ordered + extra



def md_inline(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return s


def md_block(s: str) -> str:
    if not s:
        return ""
    out: list[str] = []
    chunks = re.split(r"(```[\w-]*\n[\s\S]*?```)", s)
    for ch in chunks:
        if ch.startswith("```"):
            m = re.match(r"```([\w-]*)\n([\s\S]*?)```", ch)
            if m:
                out.append("<pre><code>" + html.escape(m.group(2).rstrip()) + "</code></pre>")
            continue
        for b in re.split(r"\n\n+", ch.strip()):
            if not b.strip():
                continue
            blines = b.splitlines()
            nonempty = [ln for ln in blines if ln.strip()]
            if nonempty and all(re.match(r"\s*[-*]\s+", ln) for ln in nonempty):
                items = [re.sub(r"^\s*[-*]\s+", "", ln) for ln in nonempty]
                out.append("<ul>" + "".join(f"<li>{md_inline(it)}</li>" for it in items) + "</ul>")
            elif nonempty and all(re.match(r"\s*\d+\.\s+", ln) for ln in nonempty):
                items = [re.sub(r"^\s*\d+\.\s+", "", ln) for ln in nonempty]
                out.append("<ol>" + "".join(f"<li>{md_inline(it)}</li>" for it in items) + "</ol>")
            elif b.startswith("### "):
                out.append("<h4>" + md_inline(b[4:].strip()) + "</h4>")
            else:
                out.append("<p>" + "<br>".join(md_inline(ln) for ln in blines) + "</p>")
    return "\n".join(out)


def split_sections(text: str):
    lines = text.splitlines()
    title = ""
    for ln in lines:
        if ln.startswith("# "):
            title = ln[2:].strip()
            break
    parts = re.split(r"\n(?=##\s+)", "\n".join(lines))
    sections: dict[str, str] = {}
    for i, part in enumerate(parts):
        part = part.strip()
        if not part:
            continue
        if part.startswith("## "):
            first, _, rest = part.partition("\n")
            sections[first[3:].strip()] = rest.strip()
    return title, sections


def pick_section(sections: dict[str, str], predicates) -> str:
    for k, v in sections.items():
        for pred in predicates:
            if pred(k):
                return v
    return ""


def parse_md(path: Path, folder: str) -> dict:
    text = path.read_text(encoding="utf-8")
    title, sections = split_sections(text)
    if not title:
        title = path.stem
    ask = pick_section(
        sections,
        [
            lambda k: "面试官" in k,
            lambda k: "怎么问" in k,
            lambda k: "问法" in k,
        ],
    )
    answer = pick_section(
        sections,
        [
            lambda k: k.startswith("参考答"),
            lambda k: "参考答" in k,
        ],
    )
    follow = pick_section(sections, [lambda k: "追问" in k])
    stem = path.stem
    qid = f"{folder}-{stem}-md"
    ask_md = ask or "先看标题，闭卷口述 90 秒。"
    answer_md = answer or "暂无参考答，以你的四行为准。"
    follow_md = follow or ""
    return {
        "id": qid,
        "title": title,
        "week": WEEK_MAP.get(folder, folder),
        "folder": folder,
        "path": f"{folder}/{path.name}",
        "ask_md": ask_md,
        "answer_md": answer_md,
        "follow_md": follow_md,
        "ask_html": md_block(ask) if ask else "<p>先看标题，闭卷口述 90 秒。</p>",
        "answer_html": md_block(answer) or "<p>暂无参考答，以你的四行为准。</p>",
        "follow_html": md_block(follow),
    }


def load_kept_0102(existing: list) -> list:
    kept = []
    for item in existing:
        folder = str(item.get("folder") or "")
        path = str(item.get("path") or "")
        if folder.startswith("01") or folder.startswith("02") or path.startswith("01") or path.startswith("02"):
            kept.append(item)
    return kept


def sort_questions(items: list) -> list:
    def key(q):
        week = q.get("week") or "其他"
        try:
            wi = WEEK_ORDER.index(week)
        except ValueError:
            wi = 99
        folder = q.get("folder") or ""
        path = q.get("path") or q.get("id") or ""
        return (wi, folder, path)

    return sorted(items, key=key)


def patch_index(questions: list) -> None:
    html_text = INDEX_HTML.read_text(encoding="utf-8")
    marker = "const QUESTIONS = "
    i = html_text.find(marker)
    if i < 0:
        raise SystemExit("const QUESTIONS = not found in index.html")
    start = i + len(marker)
    decoder = json.JSONDecoder()
    _, end = decoder.raw_decode(html_text, start)
    # keep trailing semicolon if present
    new_json = json.dumps(questions, ensure_ascii=False, indent=2)
    # Escape </script> hazards
    new_json = new_json.replace("<", "\\u003c")
    html_text = html_text[:start] + new_json + html_text[end:]
    INDEX_HTML.write_text(html_text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    existing: list = []
    if QUESTIONS_JSON.exists():
        existing = json.loads(QUESTIONS_JSON.read_text(encoding="utf-8"))
        if not isinstance(existing, list):
            existing = []
    kept = load_kept_0102(existing)

    folders = discover_folders()
    scanned: list = []
    for folder in folders:
        d = TY / folder
        if not d.is_dir():
            print("MISSING_FOLDER", folder)
            continue
        for md in sorted(d.glob("*.md")):
            if md.name.lower() == "readme.md":
                continue
            scanned.append(parse_md(md, folder))
        print("SCANNED", folder, sum(1 for q in scanned if q["folder"] == folder))

    # Prefer scanned versions over any old 03-07 leftovers in kept (kept is only 01/02)
    all_q = sort_questions(scanned + kept)
    QUESTIONS_JSON.write_text(
        json.dumps(all_q, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if INDEX_HTML.exists():
        patch_index(all_q)
        print("PATCHED", INDEX_HTML)
    else:
        print("NO_INDEX", INDEX_HTML)
    print("TOTAL", len(all_q))
    print("KEPT_01_02", len(kept))
    print("SCANNED_TOTAL", len(scanned))
    for folder in folders:
        c = sum(1 for q in all_q if q.get("folder") == folder)
        print("COUNT", folder, c)


if __name__ == "__main__":
    main()
