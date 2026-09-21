# -*- coding: utf-8 -*-
"""Scan Typora题库 and attach card leaves to concept nodes; write graph.json."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TY = ROOT / "Typora题库"
HERE = Path(__file__).resolve().parent
BASE = HERE / "graph.base.json"
OUT = HERE / "graph.json"


def collect_cards():
    cards = []
    if not TY.is_dir():
        return cards
    for p in TY.rglob("*.md"):
        if p.name.lower() == "readme.md":
            continue
        if any(part.startswith(".") for part in p.parts):
            continue
        rel = p.relative_to(TY).as_posix()
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        title = p.stem
        for ln in text.splitlines()[:30]:
            if ln.startswith("# "):
                title = ln[2:].strip()
                break
        cards.append({"path": rel, "title": title, "name": p.name, "text": text[:800]})
    return cards


def attach(nodes, cards):
    by_id = {n["id"]: n for n in nodes}
    for n in nodes:
        if n.get("group") != "concept":
            continue
        kws = n.get("keywords") or []
        if not kws:
            continue
        scored = []
        for c in cards:
            blob = (c["title"] + " " + c["name"] + " " + c["path"]).lower()
            score = 0
            for kw in kws:
                if kw.lower() in blob:
                    score += 2
                elif kw.lower() in c["text"].lower():
                    score += 1
            if score:
                scored.append((score, c))
        scored.sort(key=lambda x: (-x[0], x[1]["path"]))
        n["cards"] = [
            {"path": c["path"], "title": c["title"]}
            for _, c in scored[:5]
        ]


def main():
    data = json.loads(BASE.read_text(encoding="utf-8"))
    cards = collect_cards()
    attach(data["nodes"], cards)
    data["meta"] = {
        "card_files": len(cards),
        "nodes": len(data["nodes"]),
        "edges": len(data["edges"]),
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("WROTE", OUT)
    print("meta", data["meta"])
    linked = sum(1 for n in data["nodes"] if n.get("cards"))
    print("concepts_with_cards", linked)


if __name__ == "__main__":
    main()
