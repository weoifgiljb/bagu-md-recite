# -*- coding: utf-8 -*-
import re, pathlib
base = pathlib.Path(__file__).resolve().parent
out_root = base / "Typora题库"
js_out = out_root / "01-JavaScript"
react_out = out_root / "02-React"
for p in (js_out, react_out):
    p.mkdir(parents=True, exist_ok=True)
    for f in p.glob("*.md"):
        f.unlink()

def extract_title(raw: str, fallback: str) -> str:
    # title: "..." or title: '...'
    m = re.search(r'^title:\s*["\'](.+?)["\']\s*$', raw, re.M)
    if m:
        return m.group(1).strip()
    # title: plain
    m = re.search(r'^title:\s*(?!>|[\|"\'])(.+?)\s*$', raw, re.M)
    if m:
        return m.group(1).strip()
    # title: >- or |
    m = re.search(r'^title:\s*[>|][+-]?\s*\n((?:[ \t]+.+\n?)+)', raw, re.M)
    if m:
        lines = [ln.strip() for ln in m.group(1).splitlines() if ln.strip()]
        return " ".join(lines).strip()
    return fallback

def convert(src: pathlib.Path, dest_dir: pathlib.Path):
    raw = src.read_text(encoding="utf-8")
    title = extract_title(raw, src.parent.name)
    body = re.sub(r"```(\w+)\s+live", r"```\1", raw)
    safe = re.sub(r'[\\/:*?"<>|]', "-", title)
    safe = re.sub(r"\s+", " ", safe).strip(" -") or src.parent.name
    if len(safe) > 80:
        safe = safe[:80].rstrip()
    dest = dest_dir / f"{safe}.md"
    i = 2
    while dest.exists():
        dest = dest_dir / f"{safe}-{i}.md"
        i += 1
    dest.write_text(body, encoding="utf-8")
    return title, dest.relative_to(out_root).as_posix()

js_items, react_items = [], []
for d in sorted((base / "top-javascript-interview-questions" / "questions").iterdir()):
    zh = d / "zh-CN.mdx"
    if zh.exists():
        js_items.append(convert(zh, js_out))
for d in sorted((base / "top-reactjs-interview-questions" / "questions").iterdir()):
    zh = d / "zh-CN.mdx"
    if zh.exists():
        react_items.append(convert(zh, react_out))

lines = [
    "# 八股预备 · Typora 目录",
    "",
    "用 Typora：**文件 → 打开文件夹** → 选本目录 `Typora题库`，从本文件点题。",
    "",
    f"## JavaScript（{len(js_items)} 题）",
    "",
]
for title, rel in sorted(js_items, key=lambda x: x[0]):
    lines.append(f"- [{title}]({rel})")
lines += ["", f"## React（{len(react_items)} 题）", ""]
for title, rel in sorted(react_items, key=lambda x: x[0]):
    lines.append(f"- [{title}]({rel})")
(out_root / "目录.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
(base / "我的笔记").mkdir(exist_ok=True)
print(f"JS={len(js_items)} React={len(react_items)}")
bad = [p.name for p in js_out.glob("*.md") if p.name.startswith("-") or len(p.stem) < 3]
print("bad_names_sample", bad[:5])