# -*- coding: utf-8 -*-
"""Copy Hot100 cards into Typora题库/15-算法Hot100."""
from __future__ import annotations
import argparse, shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEST = Path(r"C:\Users\17841\Desktop\八股预备\Typora题库\15-算法Hot100")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--dest", type=Path, default=DEST)
    args = ap.parse_args()
    args.dest.mkdir(parents=True, exist_ok=True)
    n = 0
    for src in sorted(HERE.glob("*.md")):
        dst = args.dest / src.name
        print(("DRY " if args.dry_run else "COPY"), src.name, "->", dst)
        if not args.dry_run:
            shutil.copy2(src, dst)
        n += 1
    print("DONE", n)

if __name__ == "__main__":
    main()
